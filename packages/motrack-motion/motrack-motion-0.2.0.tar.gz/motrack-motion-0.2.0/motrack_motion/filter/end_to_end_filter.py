"""
Implementation of buffered end-to-end filter.
"""
from typing import Tuple

import torch

from motrack_motion.filter.base import State
from motrack_motion.filter.buffer import ObservationBuffer, BufferedStateModel


class BufferedE2EFilter(BufferedStateModel):
    """
    Implementation of buffered end-to-end
    """

    def _get_ts(self) -> Tuple[torch.Tensor, torch.Tensor]:
        t_obs = torch.tensor([0], dtype=self._dtype).view(1, 1)
        t_unobs = torch.tensor([1], dtype=self._dtype).view(1, 1)
        return t_obs, t_unobs

    def initiate(self, measurement: torch.Tensor) -> State:
        buffer = self._create_buffer(measurement)
        return buffer, None, None, None, (None, None)

    @torch.no_grad()
    def multistep_predict(self, state: State, n_steps: int) -> State:
        assert n_steps == 1, 'Multistep prediction is not supported!'

        buffer, _, _, _, (t_cache, z_cache) = state
        buffer: ObservationBuffer

        if not buffer.has_input:
            raise BufferError('Buffer does not have an input!')

        x_obs, ts_obs, ts_unobs = buffer.get_input(n_steps)
        if ts_obs.shape[0] == 1:
            # Only one bbox in history - using baseline (propagate last bbox) instead of NN model
            x_unobs_mean_hat, x_unobs_std_hat, z1_prior = self._baseline(x_obs, ts_obs, ts_unobs, multistep=True)
            return buffer, x_unobs_mean_hat, x_unobs_std_hat, z1_prior, (t_cache, z_cache)

        use_cache = t_cache is not None and buffer.last_obs_time == t_cache
        ts_first = ts_obs[0, 0, 0]
        ts_obs = ts_obs - ts_first + 1
        ts_unobs = ts_unobs - ts_first + 1
        t_obs_last, t_unobs_last = int(ts_obs[-1, 0, 0]), int(ts_unobs[-1, 0, 0])
        if self._recursive_inverse:
            ts_unobs = torch.tensor(list(range(t_obs_last + 1, t_unobs_last + 1)), dtype=torch.float32).view(-1, 1, 1)

        t_x_obs, _, t_ts_obs, t_ts_unobs, *_ = self._transform.apply(data=[x_obs, None, ts_obs, ts_unobs, None], shallow=False)
        t_x_obs, t_ts_obs, t_ts_unobs = t_x_obs.to(self._accelerator), t_ts_obs.to(self._accelerator), t_ts_unobs.to(
            self._accelerator)
        x_unobs_dummy = torch.zeros(1, 1, 4).to(self._accelerator)
        if use_cache:
            # No need to encode trajectory if it is already cached
            t_obs_last = torch.tensor(t_obs_last, dtype=self._dtype)
            t_cache = torch.tensor([t_cache], dtype=self._dtype).view(1, 1)
            z_cache, t_cache = z_cache.to(self._accelerator), t_cache.to(self._accelerator)
            outputs = self._model.filter(z_cache, t_cache, t_obs_last, x_unobs_dummy, t_ts_unobs, mask=False)
            z_cache, t_cache = z_cache.detach().cpu(), t_cache.detach().cpu()
            outputs['z_traj'] = z_cache
        else:
            outputs = self._model.forward(t_x_obs, t_ts_obs, x_unobs_dummy, t_ts_unobs, mask=False)
        outputs = {k: v.detach().cpu() for k, v in outputs.items()}
        x_unobs_dummy.detach().cpu()

        t_x_prior_mean = outputs['prior_mean']
        t_x_prior_var = outputs['prior_logvar']
        z_prior = outputs['z_prior']
        z_traj = outputs['z_traj']

        _, prior_mean, *_ = self._transform.inverse(data=[x_obs, t_x_prior_mean, None], shallow=False)

        prior_mean = prior_mean[-1]  # Removing temporal dimension after inverse transform
        prior_var = self._transform.inverse_var(t_x_prior_var, additional_data=[x_obs, None], shallow=False)
        prior_std = torch.sqrt(prior_var)[-1]

        return buffer, prior_mean, prior_std, z_prior, (buffer.last_obs_time, z_traj)

    def predict(self, state: State) -> State:
        buffer, prior_mean, prior_std, z1_prior, cache = self.multistep_predict(state, n_steps=1)
        return buffer, prior_mean[0], prior_std[0], z1_prior, cache

    def singlestep_to_multistep_state(self, state: State) -> State:
        buffer, prior_mean, prior_std, z1_prior = state
        return buffer, prior_mean.unsqueeze(0), prior_std.unsqueeze(0), z1_prior

    @torch.no_grad()
    def update(self, state: State, measurement: torch.Tensor) -> State:
        buffer, _, _, z_prior, cache = state
        buffer: ObservationBuffer

        x_obs, ts_obs, ts_unobs = buffer.get_input(1)
        buffer.push(measurement)

        if ts_obs.shape[0] == 1:
            # Only one bbox in history - using baseline (propagate last bbox) instead of NN model
            x_unobs_mean_hat, x_unobs_std_hat, z1_prior = self._baseline(x_obs, ts_obs, ts_unobs)
            return buffer, x_unobs_mean_hat, x_unobs_std_hat, z1_prior, cache

        _, t_measurement, *_ = self._transform.apply(data=[x_obs, measurement.view(1, 1, -1), ts_obs, ts_unobs, None], shallow=False)
        t_measurement, z_prior = t_measurement[0].to(self._accelerator), z_prior.to(self._accelerator)
        z_evidence = self._model.encode_unobs(t_measurement)
        t_posterior_mean, t_posterior_log_var, z_posterior = self._model.estimate_posterior(z_prior, z_evidence)
        t_posterior_mean, t_posterior_log_var, z_posterior = \
            t_posterior_mean.detach().cpu(), t_posterior_log_var.detach().cpu(), z_posterior.detach().cpu()
        t_posterior_var = self._model.postprocess_log_var(t_posterior_log_var)
        _, posterior_mean, *_ = self._transform.inverse(data=[x_obs, t_posterior_mean.view(1, 1, -1), None], shallow=False)
        posterior_var = self._transform.inverse_var(t_posterior_var, additional_data=[posterior_mean, None], shallow=False)
        posterior_std = torch.sqrt(posterior_var)

        posterior_mean = posterior_mean[-1, 0, :]
        posterior_std = posterior_std[-1, :]

        return buffer, posterior_mean, posterior_std, z_posterior, cache

    def missing(self, state: State) -> State:
        buffer, mean, std, z_state, cache = state
        buffer.increment()
        return buffer, mean, std, z_state, cache

    def project(self, state: State) -> Tuple[torch.Tensor, torch.Tensor]:
        _, mean, std, _, _ = state
        var = torch.square(std)
        return mean, var

    def _baseline(
        self,
        x_obs: torch.Tensor,
        ts_obs: torch.Tensor,
        ts_unobs: torch.Tensor,
        multistep: bool = False
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        In case there are not enough measurements (e.g. only one measurement is present),
        `baseline` is used instead of a NN model. Baseline just copies last observation.

        Args:
            x_obs: Observations
            ts_obs: Observations' time points
            ts_unobs: Unobserved (prediction) time points
            multistep: Multistep

        Returns:
            - Mean prediction
            - Standard deviation prediction
            - latent state
        """
        x_unobs_mean_hat = torch.stack([x_obs[-1].clone() for _ in range(ts_unobs.shape[0])]).to(ts_obs)
        x_unobs_std_hat = 10 * torch.ones_like(x_unobs_mean_hat).to(ts_obs)

        z0, _ = self._model.initialize(batch_size=1, device=self._accelerator)
        t_obs, t_unobs = self._get_ts()
        t_obs, t_unobs = t_obs.to(self._accelerator), t_unobs.to(self._accelerator)
        _, _, z1_prior = self._model.estimate_prior(z0, t_obs, t_unobs)
        z1_prior = z1_prior.detach().cpu()

        x_unobs_mean_hat, x_unobs_std_hat = x_unobs_mean_hat[:, 0, :], x_unobs_std_hat[:, 0, :]  # Remove batch
        if not multistep:
            x_unobs_mean_hat, x_unobs_std_hat = x_unobs_mean_hat[0], x_unobs_std_hat[0]

        return x_unobs_mean_hat, x_unobs_std_hat, z1_prior


def run_test() -> None:
    # pylint: disable=import-outside-toplevel
    from motrack_motion.datasets.transforms.base import IdentityTransform
    from motrack_motion.models.architectures.rnn_filter import RNNFilterModel

    smf = BufferedE2EFilter(
        model=RNNFilterModel(
            observable_dim=4,
            latent_dim=4,
            output_dim=4,
            t_scale=5.0
        ),
        buffer_size=5,
        accelerator='cpu',
        transform=IdentityTransform()
    )

    measurements = torch.randn(5, 4, dtype=torch.float32)

    # Initiate test
    state = smf.initiate(measurements[0])

    for i in range(1, 5):
        # Predict test
        state = smf.predict(state)
        mean_hat, cov_hat = smf.project(state)
        assert mean_hat.shape == (4,) and cov_hat.shape == (4,)

        # Update test
        state = smf.update(state, measurements[i])
        mean_updated, cov_updated = smf.project(state)
        assert mean_updated.shape == (4,) and cov_updated.shape == (4,)

    for i in range(5, 10):
        # Predict test
        state = smf.predict(state)
        mean_hat, cov_hat = smf.project(state)
        assert mean_hat.shape == (4,) and cov_hat.shape == (4,)

        # Missing test
        state = smf.missing(state)
        mean_updated, cov_updated = smf.project(state)
        assert mean_updated.shape == (4,) and cov_updated.shape == (4,)


if __name__ == '__main__':
    run_test()
