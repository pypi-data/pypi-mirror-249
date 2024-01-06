import math
from typing import Optional, Union, Dict, Tuple, List

import torch
from torch import nn

from motrack_motion.library.building_blocks.attention import TemporalFirstMultiHeadCrossAttention
from motrack_motion.library.building_blocks.mlp import MLP


class ReversedPositionalEncoding(nn.Module):

    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        # Generate positions in reverse order
        position = torch.arange(max_len - 1, -1, -1).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    @property
    def encoding(self) -> torch.Tensor:
        return self.pe

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Arguments:
            x: Tensor, shape ``[seq_len, batch_size, embedding_dim]``
        """
        x = x + self.pe[-x.size(0):]
        return self.dropout(x)


def pad_sequence(x: torch.Tensor, t: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    batch_size = t.shape[1]
    t_first, t_last = int(t[0, 0, 0]), int(t[-1, 0, 0])
    length = (t_last - t_first) + 1
    t_padded = torch.tensor(list(range(t_first, t_first + length)), dtype=torch.float32) \
        .view(-1, 1, 1) \
        .repeat(1, batch_size, 1)

    x_padded = torch.zeros(length, batch_size, x.shape[-1])
    indices = [int(t[i, 0, 0]) - t_first for i in range(t.shape[0])]
    for i_orig, i_pad in enumerate(indices):
        x_padded[i_pad] = x[i_orig]

    padded_indices = [i for i in range(length) if i not in indices]
    mask = nn.Transformer.generate_square_subsequent_mask(length)
    mask[:, padded_indices] = -torch.inf

    x_padded, t_padded, mask = x_padded.to(x), t_padded.to(t), mask.to(x)
    return x_padded, t_padded, mask


class TransFilterUpdateDecoder(nn.Module):
    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        n_heads: int,
        dropout: float = 0.1,
        n_layers: int = 2
    ):
        super().__init__()

        self._mhca = TemporalFirstMultiHeadCrossAttention(n_heads=n_heads)
        self._norm = nn.LayerNorm(input_dim)
        self._activation = nn.SiLU()
        self._dropout = nn.Dropout(p=dropout)
        self._head = nn.Sequential(
            MLP(input_dim=input_dim, output_dim=input_dim, n_layers=n_layers - 1),
            nn.Linear(input_dim, output_dim)
        )

    def forward(self, x_target: torch.Tensor, x_input: torch.Tensor) -> torch.Tensor:
        # MHCA
        x = self._mhca(q=x_target, k=x_input, v=x_input)
        x = self._norm(x)
        x = self._activation(x)
        x = self._dropout(x)
        x = x_target + x

        # FFN
        return self._head(x)


class TransFilter(nn.Module):
    def __init__(
        self,
        input_dim: int,
        output_dim: int,

        # Model (global)
        d_model: int,
        activation: Union[nn.Module, str] = nn.SiLU,
        t_scale: float = 30.0,
        pooling: str = 'mean',

        # Positional encoding
        pe_dropout: float = 0.1,
        pe_max_len: int = 120,

        # Encoder
        enc_n_layers: int = 6,
        enc_n_heads: int = 8,
        enc_d_model: Optional[int] = None,
        enc_dropout: float = 0.1,

        # Prediction head
        pred_steps: int = 30,
        pred_n_layers: int = 2,

        # Decoder
        dec_n_heads: int = 8,
        dec_dropout: float = 0.1,
        dec_n_layers: int = 2
    ):
        super().__init__()

        # Defaults
        enc_d_model = d_model if enc_d_model is None else enc_d_model
        activation = activation() if not isinstance(activation, str) else activation

        self._t_scale = t_scale
        self._output_dim = output_dim
        self._steps = pred_steps

        # Architecture
        assert pooling in ['mean', 'max', 'last'], f'Invalid pooling option "{pooling}"!'
        self._pooling = pooling
        self._input_embedding = MLP(
            input_dim=input_dim + 1,  # includes time
            hidden_dim=d_model,
            output_dim=d_model
        )
        self._pos_encoding = ReversedPositionalEncoding(
            d_model=d_model,
            dropout=pe_dropout,
            max_len=pe_max_len
        )
        self._encoder = nn.TransformerEncoder(
            encoder_layer=nn.TransformerEncoderLayer(
                d_model=d_model,
                nhead=enc_n_heads,
                dim_feedforward=enc_d_model,
                dropout=enc_dropout,
                activation=activation
            ),
            num_layers=enc_n_layers
        )

        self._predict_head = nn.Sequential(
            MLP(input_dim=d_model, output_dim=d_model, n_layers=pred_n_layers - 1),
            nn.Linear(d_model, pred_steps * output_dim)
        )

        self._target_embedding = MLP(
            input_dim=2 * output_dim + 1,  # Innovation (4) + time (1)
            hidden_dim=d_model,
            output_dim=d_model
        )
        self._decoder = TransFilterUpdateDecoder(
            input_dim=d_model,
            output_dim=output_dim,
            n_heads=dec_n_heads,
            dropout=dec_dropout,
            n_layers=dec_n_layers
        )

    def encode_trajectory(self, x_obs: torch.Tensor, t_obs: torch.Tensor, mask: Optional[torch.Tensor] = None) \
            -> Tuple[torch.Tensor, torch.Tensor]:
        t_obs_last = t_obs[-1, 0, 0]

        with torch.no_grad():
            t_obs = (t_obs - t_obs_last) / self._t_scale

        xt_input = torch.cat([x_obs, t_obs], dim=-1)
        z_input = self._input_embedding(xt_input)
        z_input = z_input + self._pos_encoding(z_input)

        if mask is None:
            # Create causal mask
            mask = nn.Transformer.generate_square_subsequent_mask(z_input.shape[0]).to(z_input)

        zs = self._encoder(z_input, mask)
        return zs, t_obs_last

    def _pool(self, zs: torch.Tensor) -> torch.Tensor:
        if self._pooling == 'mean':
            return torch.mean(zs, dim=0)
        if self._pooling == 'max':
            return torch.max(zs, dim=0)[0]
        if self._pooling == 'last':
            return zs[-1, :, :]

        raise AssertionError('Invalid Program State!')

    @staticmethod
    def get_prediction_indices(t_obs_last: torch.Tensor, t_unobs: torch.Tensor) -> List[int]:
        t_unobs_first = int(t_obs_last) + 1
        return [int(t) - t_unobs_first for t in t_unobs[:, 0, 0].detach()]

    def predict(self, zs: torch.Tensor, t_obs_last: torch.Tensor, t_unobs: torch.Tensor) -> torch.Tensor:
        z_agg = self._pool(zs)
        x_prior = self._predict_head(z_agg) # (B, steps * output_dim)
        x_prior = x_prior.view(-1, self._steps, self._output_dim) # (B, steps, output_dim)
        x_prior = torch.transpose(x_prior, 0, 1)

        if t_unobs.shape[0] < self._steps:
            indices = self.get_prediction_indices(t_obs_last, t_unobs)
            x_prior = x_prior[indices]
        return x_prior

    def update(self, zs: torch.Tensor, t_obs_last: torch.Tensor, x_prior: torch.Tensor, x_unobs: torch.Tensor, t_unobs: torch.Tensor) -> torch.Tensor:
        with torch.no_grad():
            innovation = x_unobs - x_prior
            t_unobs = (t_unobs - t_obs_last) / self._t_scale

        # Update step
        xti_target = torch.cat([x_unobs, t_unobs, innovation], dim=-1)
        z_target = self._target_embedding(xti_target)
        return self._decoder(z_target, zs)

    def forward(self, x_obs: torch.Tensor, t_obs: torch.Tensor, x_unobs: torch.Tensor, t_unobs: torch.Tensor, mask: Optional[torch.Tensor] = None) \
            -> Dict[str, torch.Tensor]:
        assert torch.abs(t_obs[1:, 0, 0] - t_obs[:-1, 0, 0] - 1).sum() < 1e-6, f'Sequence is not padded! {t_obs[:, 0, 0]=}'

        zs, t_obs_last = self.encode_trajectory(x_obs, t_obs, mask=mask)
        x_prior = self.predict(zs, t_obs_last, t_unobs)
        x_posterior = self.update(zs, t_obs_last, x_prior, x_unobs, t_unobs)

        return {
            'z_traj': zs,
            'x_prior': x_prior,
            'x_posterior': x_posterior
        }


def run_test() -> None:
    # Test model
    model = TransFilter(
        input_dim=4,
        output_dim=4,
        d_model=8
    )

    x_obs = torch.randn(10, 2, 4)
    t_obs = torch.tensor(list(range(1, 11)), dtype=torch.float32).view(-1, 1, 1).repeat(1, 2, 1)
    x_unobs = torch.randn(5, 2, 4)
    t_unobs = torch.tensor(list(range(16, 21)), dtype=torch.float32).view(-1, 1, 1).repeat(1, 2, 1)

    outputs = model(x_obs, t_obs, x_unobs, t_unobs)
    z_traj = outputs['z_traj']
    x_prior = outputs['x_prior']
    x_posterior = outputs['x_posterior']

    assert z_traj.shape == (10, 2, 8), f'{z_traj.shape=}'
    assert x_prior.shape == (5, 2, 4), f'{x_prior.shape=}'
    assert x_posterior.shape == (5, 2, 4), f'{x_posterior.shape=}'

    # Test padding
    x = torch.randn(3, 2, 4)
    t = torch.tensor([3, 4, 7], dtype=torch.float32).view(-1, 1, 1).repeat(1, 2, 1)
    t_expected = torch.tensor([3, 4, 5, 6, 7], dtype=torch.float32).view(-1, 1, 1).repeat(1, 2, 1)
    x_padded, t_padded, mask = pad_sequence(x, t)

    assert x_padded.shape == (5, 2, 4), f'{x.shape=}'
    assert t_padded.shape == (5, 2, 1), f'{t.shape}'
    assert torch.abs(t_padded - t_expected).sum() < 1e-6, f'{t=}'

    outputs = model(x_padded, t_padded, x_unobs, t_unobs, mask=mask)
    z_traj = outputs['z_traj']
    x_prior = outputs['x_prior']
    x_posterior = outputs['x_posterior']

    assert z_traj.shape == (5, 2, 8), f'{z_traj.shape=}'
    assert x_prior.shape == (5, 2, 4), f'{x_prior.shape=}'
    assert x_posterior.shape == (5, 2, 4), f'{x_posterior.shape=}'


if __name__ == '__main__':
    run_test()
