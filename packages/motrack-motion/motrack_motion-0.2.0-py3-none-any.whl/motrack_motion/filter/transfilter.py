"""
Implementation of buffered end-to-end filter.
"""
from typing import Tuple

import torch

from motrack_motion.filter.base import State
from motrack_motion.filter.buffer import ObservationBuffer, BufferedStateModel
from motrack_motion.models.architectures.transfilter import TransFilter, pad_sequence


class BufferedTransFilter(BufferedStateModel):
    """
    Implementation of buffered TransFilter.
    """
    def _create_uncertainty_tensor(self, x: torch.Tensor) -> torch.Tensor:
        return self._uncertainty_multiplier * torch.ones_like(x).to(x)

    def initiate(self, measurement: torch.Tensor) -> State:
        buffer = self._create_buffer(measurement)
        return buffer, None, None, None

    @torch.no_grad()
    def multistep_predict(self, state: State, n_steps: int) -> State:
        assert n_steps == 1, 'Multistep prediction is not supported!'

        buffer, _, _, zs = state
        buffer: ObservationBuffer

        if not buffer.has_input:
            raise BufferError('Buffer does not have an input!')

        x_obs, ts_obs, ts_unobs = buffer.get_input(n_steps)
        if ts_obs.shape[0] == 1:
            # Only one bbox in history - using baseline (propagate last bbox) instead of NN model
            x_unobs_mean_hat, x_unobs_var_hat = self._baseline(x_obs, ts_obs, ts_unobs, multistep=True)
            return buffer, x_unobs_mean_hat, x_unobs_var_hat, None

        if self._recursive_inverse:
            t_obs_last_int, t_unobs_last_int = int(ts_obs[-1, 0, 0]), int(ts_unobs[-1, 0, 0])
            ts_unobs = torch.tensor(list(range(t_obs_last_int + 1, t_unobs_last_int + 1)), dtype=torch.float32).view(-1, 1, 1)

        # Preprocess
        t_x_obs, _, t_ts_obs, t_ts_unobs, *_ = self._transform.apply(data=[x_obs, None, ts_obs, ts_unobs, None], shallow=False)
        t_x_obs, t_ts_obs, mask = pad_sequence(t_x_obs, t_ts_obs)

        # Inference
        t_x_obs, t_ts_obs, t_ts_unobs = t_x_obs.to(self._accelerator), t_ts_obs.to(self._accelerator), t_ts_unobs.to(self._accelerator)
        zs, t_obs_last = self._model.encode_trajectory(t_x_obs, t_ts_obs, mask=mask)
        t_x_prior_mean = self._model.predict(zs, t_obs_last, t_ts_unobs)
        t_x_prior_mean = t_x_prior_mean.detach().cpu()

        # Postprocess
        t_x_prior_var = self._create_uncertainty_tensor(t_x_prior_mean)
        _, prior_mean, *_ = self._transform.inverse(data=[x_obs, t_x_prior_mean, None], shallow=False)
        prior_var = self._transform.inverse_var(t_x_prior_var, additional_data=[x_obs, None], shallow=False)
        prior_mean = prior_mean[-1]  # Removing temporal dimension after inverse transform
        prior_var = prior_var[-1]

        return buffer, prior_mean, prior_var, zs

    def predict(self, state: State) -> State:
        buffer, prior_mean, prior_var, zs = self.multistep_predict(state, n_steps=1)
        return buffer, prior_mean[0], prior_var[0], zs

    def singlestep_to_multistep_state(self, state: State) -> State:
        buffer, prior_mean, prior_var, zs = state
        return buffer, prior_mean.unsqueeze(0), prior_var.unsqueeze(0), zs

    @torch.no_grad()
    def update(self, state: State, measurement: torch.Tensor) -> State:
        buffer, x_prior, _, zs = state
        buffer: ObservationBuffer

        x_obs, ts_obs, ts_unobs = buffer.get_input(1)
        buffer.push(measurement)

        if ts_obs.shape[0] == 1:
            # Only one bbox in history - using baseline (propagate last bbox) instead of NN model
            x_unobs_mean_hat, x_unobs_var_hat = self._baseline(x_obs, ts_obs, ts_unobs)
            return buffer, x_unobs_mean_hat, x_unobs_var_hat, None
        assert zs is not None

        # Preprocess
        _, t_measurement, t_ts_obs, t_ts_unobs, _ = self._transform.apply(data=[x_obs, measurement.view(1, 1, -1), ts_obs, ts_unobs, None],
                                                                       shallow=False)
        t_obs_last = t_ts_obs[-1, 0, 0]
        x_prior = x_prior.view(1, 1, -1)

        # Inference
        t_measurement, zs, t_obs_last = t_measurement.to(self._accelerator), zs.to(self._accelerator), t_obs_last.to(self._accelerator)
        t_posterior_mean = self._model.update(zs, t_obs_last, x_prior, t_measurement, t_ts_unobs)
        t_posterior_mean = t_posterior_mean.detach().cpu()

        # Postprocess
        t_posterior_var = self._create_uncertainty_tensor(t_posterior_mean)
        _, posterior_mean, *_ = self._transform.inverse(data=[x_obs, t_posterior_mean.view(1, 1, -1), None], shallow=False)
        posterior_var = self._transform.inverse_var(t_posterior_var, additional_data=[posterior_mean, None], shallow=False)

        posterior_mean = posterior_mean[-1, 0, :]
        posterior_var = posterior_var[-1, 0, :]

        return buffer, posterior_mean, posterior_var, zs

    def missing(self, state: State) -> State:
        buffer, mean, var, z_state = state
        buffer.increment()
        return buffer, mean, var, z_state

    def project(self, state: State) -> Tuple[torch.Tensor, torch.Tensor]:
        _, mean, var, _ = state
        return mean, var

    def _baseline(
        self,
        x_obs: torch.Tensor,
        ts_obs: torch.Tensor,
        ts_unobs: torch.Tensor,
        multistep: bool = False
    ) -> Tuple[torch.Tensor, torch.Tensor]:
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
        x_unobs_var_hat = self._create_uncertainty_tensor(x_unobs_mean_hat)
        x_unobs_mean_hat, x_unobs_var_hat = x_unobs_mean_hat[:, 0, :], x_unobs_var_hat[:, 0, :]  # Remove batch
        if not multistep:
            x_unobs_mean_hat, x_unobs_var_hat = x_unobs_mean_hat[0], x_unobs_var_hat[0]

        return x_unobs_mean_hat, x_unobs_var_hat


def run_test() -> None:
    # pylint: disable=import-outside-toplevel
    from motrack_motion.datasets.transforms.base import IdentityTransform

    smf = BufferedTransFilter(
        model=TransFilter(
            input_dim=4,
            d_model=16,
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
