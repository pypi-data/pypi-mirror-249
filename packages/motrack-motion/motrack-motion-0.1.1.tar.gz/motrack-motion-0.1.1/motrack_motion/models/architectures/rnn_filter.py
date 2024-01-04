"""
Implementation of the RNNFilter.
"""
from typing import Tuple, Union

import torch
from torch import nn

from motrack_motion.library.building_blocks.mlp import MLP
from motrack_motion.models.architectures.end_to_end import FilterModule


class RNNMultiStepModule(nn.Module):
    """
    RNNMultiStepModule
    """
    def __init__(
        self,
        latent_dim: int,
        n_rnn_layers: int = 1,
    ):
        """
        Args:
            latent_dim: "latent" (hidden-2) trajectory dimension
            n_rnn_layers: Number of stacked RNN (GRU) layers
        """
        super().__init__()

        self._latent_dim = latent_dim
        self._n_rnn_layers = n_rnn_layers

        self._rnn = nn.GRU(
            input_size=1,
            hidden_size=latent_dim,
            num_layers=n_rnn_layers,
            batch_first=False
        )

    def forward(self, z: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        n_steps = round(float(t[0, 0, 0]))

        z = z.unsqueeze(0)
        for t_i in range(1, n_steps + 1):
            t_i = torch.tensor([t_i], dtype=torch.float32).view(1, 1, 1).repeat(1, z.shape[1], 1).to(z)
            _, z = self._rnn(t_i, z)

        return z[-1]


class RNNFilterModel(FilterModule):
    """
    RNNFilterModel
    """
    def __init__(
        self,
        observable_dim: int,
        latent_dim: int,
        output_dim: int,

        bounded_variance: bool = False,
        bounded_value: float = 0.01,

        n_rnn_layers: int = 1,
        n_update_layers: int = 1,
        n_head_mlp_layers: int = 2,
        n_obs2latent_mlp_layers: int = 1,
        t_scale: float = 30.0
    ):
        super().__init__(
            bounded_variance=bounded_variance,
            bounded_value=bounded_value,
            t_scale=t_scale
        )
        self._bounded_variance = bounded_variance

        self._observable_dim = observable_dim
        self._latent_dim = latent_dim
        self._output_dim = output_dim

        self._rnn = RNNMultiStepModule(
            latent_dim=latent_dim,
            n_rnn_layers=n_rnn_layers
        )

        self._prior_head_mean = nn.Sequential(
            MLP(latent_dim, latent_dim, n_layers=n_head_mlp_layers),
            nn.Linear(latent_dim, output_dim, bias=True)
        )
        self._prior_head_log_var = nn.Sequential(
            MLP(latent_dim, latent_dim, n_layers=n_head_mlp_layers),
            nn.Linear(latent_dim, output_dim, bias=True)
        )
        self._posterior_head_mean = nn.Sequential(
            MLP(latent_dim, latent_dim, n_layers=n_head_mlp_layers),
            nn.Linear(latent_dim, output_dim, bias=True)
        )
        self._posterior_head_log_var = nn.Sequential(
            MLP(latent_dim, latent_dim, n_layers=n_head_mlp_layers),
            nn.Linear(latent_dim, output_dim, bias=True)
        )

        self._obs2latent = MLP(
            input_dim=observable_dim,
            hidden_dim=latent_dim,
            output_dim=latent_dim,
            n_layers=n_obs2latent_mlp_layers
        )

        self._unobs2latent = MLP(
            input_dim=output_dim,
            hidden_dim=latent_dim,
            output_dim=latent_dim,
            n_layers=n_obs2latent_mlp_layers
        )

        self._n_update_layers = n_update_layers
        self._update_layer = nn.GRU(
            input_size=latent_dim,
            hidden_size=latent_dim,
            num_layers=n_update_layers,
            batch_first=False
        )

    def initialize(self, batch_size: int, device: Union[str, torch.device]) -> Tuple[torch.Tensor, torch.Tensor]:
        z0 = torch.zeros(batch_size, self._latent_dim, dtype=torch.float32).to(device)
        t0 = torch.zeros(batch_size, 1, dtype=torch.float32).to(device)
        return z0, t0

    def estimate_prior(self, z0: torch.Tensor, t0: torch.Tensor, t1: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        t = (t1 - t0).unsqueeze(0)
        z1_prior = self._rnn(z0, t)
        x1_prior_mean = self._prior_head_mean(z1_prior)
        x1_prior_log_var = self._prior_head_log_var(z1_prior)
        return x1_prior_mean, x1_prior_log_var, z1_prior

    def estimate_posterior(self, z1_prior: torch.Tensor, z1_evidence: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        z1_prior = z1_prior.unsqueeze(0).repeat(self._n_update_layers, 1, 1)
        z1_evidence = z1_evidence.unsqueeze(0)
        z1_posterior, _ = self._update_layer(z1_evidence, z1_prior)
        z1_posterior = z1_posterior[0]

        x1_posterior_mean = self._posterior_head_mean(z1_posterior)
        x1_posterior_log_var = self._posterior_head_log_var(z1_posterior)
        return x1_posterior_mean, x1_posterior_log_var, z1_posterior

    def encode_obs(self, x: torch.Tensor) -> torch.Tensor:
        return self._obs2latent(x)

    def encode_unobs(self, x: torch.Tensor) -> torch.Tensor:
        return self._unobs2latent(x)


def run_test() -> None:
    rfm = RNNFilterModel(
        observable_dim=4,
        latent_dim=3,
        output_dim=4,

        n_rnn_layers=2
    )

    x_obs = torch.randn(4, 3, 4)
    x_unobs = torch.randn(2, 3, 4)
    t_obs = torch.tensor([0, 1, 2, 4], dtype=torch.float32).view(-1, 1, 1).repeat(1, 3, 1)
    t_unobs = torch.tensor([6, 9], dtype=torch.float32).view(-1, 1, 1).repeat(1, 3, 1)

    priors_mean, priors_log_var, posteriors_mean, posteriors_log_var = rfm(x_obs, t_obs, x_unobs, t_unobs)
    print(priors_mean.shape, priors_log_var.shape, posteriors_mean.shape, posteriors_log_var.shape)


if __name__ == '__main__':
    run_test()
