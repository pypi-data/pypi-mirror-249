from typing import Callable
import jax
import jax.numpy as jnp
from jax.scipy.stats import multivariate_normal
from tqdm import tqdm
from flowMC.sampler.Proposal_Base import ProposalBase
from functools import partialmethod
from jaxtyping import PyTree, Array, Float, Int, PRNGKeyArray


class MALA(ProposalBase):
    """
    Metropolis-adjusted Langevin algorithm sampler class builiding the mala_sampler method

    Args:
        logpdf: target logpdf function
        jit: whether to jit the sampler
        params: dictionary of parameters for the sampler
    """

    def __init__(
        self, logpdf: Callable, jit: bool, params: dict, use_autotune=False
    ):
        super().__init__(logpdf, jit, params)
        self.params = params
        self.logpdf = logpdf
        self.use_autotune = use_autotune

    def body(self, carry, this_key):
        print("Compiling MALA body")
        this_position, dt, data = carry
        dt2 = dt * dt
        this_log_prob, this_d_log = jax.value_and_grad(self.logpdf)(this_position, data)
        proposal = this_position + jnp.dot(dt2, this_d_log) / 2
        proposal += jnp.dot(dt, jax.random.normal(this_key, shape=this_position.shape))
        return (proposal, dt, data), (proposal, this_log_prob, this_d_log)

    def kernel(
        self,
        rng_key: PRNGKeyArray,
        position: Float[Array, "ndim"],
        log_prob: Float[Array, "1"],
        data: PyTree,
    ) -> tuple[
        Float[Array, "ndim"], Float[Array, "1"], Int[Array, "1"]
    ]:
        """
        Metropolis-adjusted Langevin algorithm kernel.
        This is a kernel that only evolve a single chain.

        Args:
            rng_key (PRNGKeyArray): Jax PRNGKey
            position (Float[Array, "ndim"]): current position of the chain
            log_prob (Float[Array, "1"]): current log-probability of the chain
            data (PyTree): data to be passed to the logpdf function

        Returns:
            position (Float[Array, "ndim"]): new position of the chain
            log_prob (Float[Array, "1"]): new log-probability of the chain
            do_accept (Int[Array, "1"]): whether the new position is accepted
        """

        key1, key2 = jax.random.split(rng_key)

        dt = self.params["step_size"]
        dt2 = dt * dt

        _, (proposal, logprob, d_logprob) = jax.lax.scan(
            self.body, (position, dt, data), jnp.array([key1, key1])
        )

        ratio = logprob[1] - logprob[0]
        ratio -= multivariate_normal.logpdf(
            proposal[0], position + jnp.dot(dt2, d_logprob[0]) / 2, dt2
        )
        ratio += multivariate_normal.logpdf(
            position, proposal[0] + jnp.dot(dt2, d_logprob[1]) / 2, dt2
        )

        log_uniform = jnp.log(jax.random.uniform(key2))
        do_accept = log_uniform < ratio

        position = jnp.where(do_accept, proposal[0], position)
        log_prob = jnp.where(do_accept, logprob[1], logprob[0])

        return position, log_prob, do_accept

    def update(
        self, i, state
    ) -> tuple[
        PRNGKeyArray,
        Float[Array, "nstep ndim"],
        Float[Array, "nstep 1"],
        Int[Array, "n_step 1"],
        PyTree,
    ]:
        """
        Update function for the MALA sampler

        Args:
            i (int): current step
            state (tuple): state array storing the kernel information

        Returns:
            state (tuple): updated state array
        """
        key, positions, log_p, acceptance, data = state
        _, key = jax.random.split(key)
        new_position, new_log_p, do_accept = self.kernel(
            key, positions[i - 1], log_p[i - 1], data
        )
        positions = positions.at[i].set(new_position)
        log_p = log_p.at[i].set(new_log_p)
        acceptance = acceptance.at[i].set(do_accept)
        return (key, positions, log_p, acceptance, data)

    def sample(self,
        rng_key: PRNGKeyArray,
        n_steps: int,
        initial_position: Float[Array, "n_chains ndim"],
        data: PyTree,
        verbose: bool = False,
    ) -> tuple[
        Float[Array, "n_chains n_steps ndim"],
        Float[Array, "n_chains n_steps 1"],
        Int[Array, "n_chains n_steps 1"],
    ]:
        logp = self.logpdf_vmap(initial_position, data)
        n_chains = rng_key.shape[0]
        acceptance = jnp.zeros((n_chains, n_steps))
        all_positions = (
            jnp.zeros((n_chains, n_steps) + initial_position.shape[-1:])
        ) + initial_position[:, None]
        all_logp = jnp.zeros((n_chains, n_steps)) + logp[:, None]
        state = (rng_key, all_positions, all_logp, acceptance, data)
        if verbose:
            iterator_loop = tqdm(
                range(1, n_steps),
                desc="Sampling Locally",
                miniters=int(n_steps / 10),
            )
        else:
            iterator_loop = range(1, n_steps)
        for i in iterator_loop:
            state = self.update_vmap(i, state)
        return state[:-1]


    def mala_sampler_autotune(
        self, rng_key, initial_position, log_prob, data, params, max_iter=30
    ):
        """
        Tune the step size of the MALA kernel using the acceptance rate.

        Args:
            mala_kernel_vmap (Callable): A MALA kernel
            rng_key: Jax PRNGKey
            initial_position (n_chains, n_dim): initial position of the chains
            log_prob (n_chains, ): log-probability of the initial position
            params (dict): parameters of the MALA kernel
            max_iter (int): maximal number of iterations to tune the step size
        """

        tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)

        counter = 0
        position, log_prob, do_accept = self.kernel_vmap(
            rng_key, initial_position, log_prob, data
        )
        acceptance_rate = jnp.mean(do_accept)
        while (acceptance_rate <= 0.3) or (acceptance_rate >= 0.5):
            if counter > max_iter:
                print(
                    "Maximal number of iterations reached. Existing tuning with current parameters."
                )
                break
            if acceptance_rate <= 0.3:
                params["step_size"] *= 0.8
            elif acceptance_rate >= 0.5:
                params["step_size"] *= 1.25
            counter += 1
            position, log_prob, do_accept = self.kernel_vmap(
                rng_key, initial_position, log_prob, data
            )
            acceptance_rate = jnp.mean(do_accept)
        tqdm.__init__ = partialmethod(tqdm.__init__, disable=False)
        return params
