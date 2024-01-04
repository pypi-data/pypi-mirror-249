"""
End-to-End filter interface.
"""
from abc import ABC, abstractmethod
from typing import Union, Tuple, List, Dict

import torch
from torch import nn


class FilterModule(nn.Module, ABC):
    """
    Interface for the filter module.
    """
    def __init__(
        self,
        t_scale: float = 30.0,
        bounded_variance: bool = False,
        bounded_value: float = 0.01
    ):
        """
        Args:
            bounded_variance: Use soft-plus instead exp for variance post-process and bound it with `bounded_value` as lower value
            bounded_value: Bounded variance value
        """
        super().__init__()
        self._t_scale = t_scale
        self._bounded_variance = bounded_variance
        self._bounded_value = bounded_value

    @abstractmethod
    def initialize(self, batch_size: int, device: Union[str, torch.device]) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Creates initial filter state before any value is observed.

        Args:
            batch_size: Batch size
            device: Device to place initial state

        Returns:
            Initial state (hidden, time)
        """

    @abstractmethod
    def estimate_prior(self, z0: torch.Tensor, t0: torch.Tensor, t1: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Estimates the next prior state at time t1 given the posterior (z0, t0)
        Args:
            z0: Previous posterior latent state
            t0: Previous posterior time
            t1: Next prior time

        Returns:
            - Estimated prior mean
            - Estimated prior variance
            - Prior latent state
        """

    @abstractmethod
    def estimate_posterior(self, z1_prior: torch.Tensor, z1_evidence: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Estimates the next posterior state given the current prior state (z1_prior)
        and the observed latent evidence (z1_evidence)

        Args:
            z1_prior: Latent prior state
            z1_evidence: Latent evidence

        Returns:
            - Estimated posterior mean
            - Estimated posterior variance
            - Posterior latent state
        """

    @abstractmethod
    def encode_obs(self, x: torch.Tensor) -> torch.Tensor:
        """
        Encodes observation into latent state.

        Args:
            x: Raw observation

        Returns:
            Latent observation
        """

    @abstractmethod
    def encode_unobs(self, x: torch.Tensor) -> torch.Tensor:
        """
        Encodes "unobserved" observation into latent state.

        Args:
            x: Raw "unobserved" observation

        Returns:
            Latent "unobserved" observation
        """

    def next(self, z0: torch.Tensor, z1_evidence: torch.Tensor, t0: torch.Tensor, t1: torch.Tensor) \
            -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Combines `estimate_prior` and `estimate_posterior` into a single function. Convention for training.

        Args:
            z0: Previous posterior latent state
            z1_evidence: Latent evidence
            t0: Previous posterior time
            t1: Next prior time

        Returns:
            - Estimated prior mean
            - Estimated prior variance
            - Estimated posterior mean
            - Estimated posterior variance
            - Posterior latent state
        """
        x1_prior_mean, x1_prior_log_var, z1_prior = self.estimate_prior(z0, t0, t1)
        x1_posterior_mean, x1_posterior_log_var, z1_posterior = self.estimate_posterior(z1_prior, z1_evidence)
        return x1_prior_mean, x1_prior_log_var, x1_posterior_mean, x1_posterior_log_var, z1_posterior

    def encode_obs_trajectory(self, x_obs: torch.Tensor, t_obs: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Encoded full observed trajectory into latent state.

        Args:
            x_obs: Trajectory features
            t_obs: Trajectory time points

        Returns:
            - Trajectory latent summarization
            - Last time point
        """
        n_warmup_steps, batch_size, _ = t_obs.shape

        z0, t0 = self.initialize(batch_size, t_obs.device)
        z1_obs = self.encode_obs(x_obs)
        for i in range(n_warmup_steps):
            t1 = t_obs[i]
            z1 = z1_obs[i]
            _, _, _, _, z0 = self.next(z0, z1, t0, t1)
            t0 = t1

        return z0, t0

    def filter(
        self,
        z0: torch.Tensor,
        t0: torch.Tensor,
        t_obs_last: torch.Tensor,
        x_unobs: torch.Tensor,
        t_unobs: torch.Tensor,
        mask: Union[List[bool], bool] = True
    ) -> Dict[str, torch.Tensor]:
        """
        Performs unobserved trajectory filtering.

        Args:
            z0: Encoded trajectory
            t0: Last observed time point
            t_obs_last: Last raw time observed time point
            x_unobs: Unobserved trajectory (to be filtered)
            t_unobs: Unobserved trajectory time points
            mask: Simulates missing "unobserved" points

        Returns:
            - prior mean
            - prior log-var
            - posterior mean
            - posterior log-var
            - prior latent state - `z_prior`
        """
        if isinstance(mask, bool):
            mask = [mask for _ in range(t_unobs.shape[0])]
        assert len(mask) == t_unobs.shape[0], f'Invalid mask length {len(mask)}. Expected: {t_unobs.shape[0]}.'

        n_estimation_steps, _, _ = t_unobs.shape
        assert n_estimation_steps >= 1, f'Invalid n_estimation_steps {n_estimation_steps}!'

        with torch.no_grad():
            # Scale time points relative to the last observation
            t_unobs = (t_unobs - t_obs_last) / self._t_scale

        priors_mean, priors_log_var, posteriors_mean, posteriors_log_var = [], [], [], []
        z1_unobs = self.encode_unobs(x_unobs)
        i_lag = 0  # measurement index lags in case of missing points
        for i in range(n_estimation_steps):
            t1 = t_unobs[i]
            if mask[i]:
                # Data is present - Estimate the prior and the posterior
                z1 = z1_unobs[i - i_lag]
                x1_prior_mean, x1_prior_log_var, x1_posterior_mean, x1_posterior_log_var, z0 = self.next(z0, z1, t0, t1)
                posteriors_mean.append(x1_posterior_mean)
                posteriors_log_var.append(x1_posterior_log_var)
            else:
                # Data is not present - Just estimate the prior
                x1_prior_mean, x1_prior_log_var, z0 = self.estimate_prior(z0, t0, t1)
                i_lag += 1

            t0 = t1

            priors_mean.append(x1_prior_mean)
            priors_log_var.append(x1_prior_log_var)

        priors_mean, priors_log_var, posteriors_mean, posteriors_log_var = \
            [(torch.stack(v) if len(v) > 0 else torch.empty(0, dtype=torch.float32))
             for v in [priors_mean, priors_log_var, posteriors_mean, posteriors_log_var]]

        return {
            'prior_mean': priors_mean,
            'prior_logvar': priors_log_var,
            'posterior_mean': posteriors_mean,
            'posterior_logvar': posteriors_log_var,
            'z_prior': z0
        }


    def forward(self, x_obs: torch.Tensor, t_obs: torch.Tensor, x_unobs: torch.Tensor, t_unobs: torch.Tensor, mask: Union[List[bool], bool] = True) \
            -> Dict[str, torch.Tensor]:
        """
        Performs full forward step:
        - Encodes full observed (warm-up) trajectory into latent state
        - Filters full trajectory (including observed and unobserved)

        Args:
            x_obs: Observed trajectory (warm-up)
            t_obs: Observed trajectory time-points
            x_unobs: Unobserved trajectory (to be filtered)
            t_unobs: Unobserved trajectory time points
            mask: Simulates missing "unobserved" tr

        Returns:
            - prior mean
            - prior log-var
            - posterior mean
            - posterior log-var
            - prior latent state - `z_prior`
            - encoded observed trajectory latent state - `z_traj`
        """
        with torch.no_grad():
            t_obs_last = t_obs[-1, 0, 0]
            t_obs = (t_obs - t_obs_last) / self._t_scale

        z0_traj, t0 = self.encode_obs_trajectory(x_obs, t_obs)
        outputs = self.filter(z0_traj, t0, t_obs_last, x_unobs, t_unobs, mask=mask)
        outputs['z_traj'] = z0_traj
        return outputs


    def postprocess_log_var(self, var: torch.Tensor) -> torch.Tensor:
        """
        Post-processes variance output.

        Args:
            var: Variance

        Returns:
            Post-processes variance output
        """
        if not self._bounded_variance:
            return torch.exp(var)
        else:
            return 0.1 + 0.9 * torch.nn.functional.softplus(var)  # Bounded variance
