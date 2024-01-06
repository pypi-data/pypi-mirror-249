"""
Building block: MultiLayerPerceptron
"""
from typing import Optional, List

import torch
from torch import nn


class MLP(nn.Module):
    """
    MultiLayerPerceptron where each linear layer contains:
    - Linear layer
    - LayerNorm
    - SiLU
    """
    def __init__(
        self,
        input_dim: int,
        hidden_dim: Optional[int] = None,
        output_dim: Optional[int] = None,
        n_layers: int = 1,
        activation: Optional[nn.Module] = nn.SiLU,
        residual: bool = False
    ):
        """
        Args:
            input_dim: Model Input dimension
            hidden_dim: Model hidden dimension
                - tensor dimension between layers
                - equal to `input_dim` if not defined
                - not relevant in case `n_layers` is equal to `1`
            output_dim: Model output dimension
                - equal to `input_dim` if not defined
            n_layers: Number of Perceptron layers
            residual: Use skip connections
        """
        super().__init__()
        self._residual = residual

        assert n_layers >= 1, f'Minimum number of layers is 1 but found {n_layers}'
        if output_dim is None:
            output_dim = input_dim
        if hidden_dim is None:
            hidden_dim = output_dim

        assert not residual or (input_dim == hidden_dim == output_dim)

        layers_args = [[hidden_dim, hidden_dim] for _ in range(n_layers)]
        layers_args[0][0] = input_dim
        layers_args[-1][1] = output_dim
        self._model = nn.Sequential(*[self._create_mlp_layer(*args, activation=activation) for args in layers_args])

    @staticmethod
    def _create_mlp_layer(input_dim: int, output_dim: int, activation: Optional[nn.Module]) -> nn.Module:
        """
        Constructs previously defined MLP layer

        Args:
            input_dim: Input dimension
            output_dim: Output dimension
            activation: Activation function

        Returns:
            Perceptron
        """
        layers: List[nn.Module] = [
            nn.Linear(input_dim, output_dim),
            nn.LayerNorm(output_dim)
        ]


        if activation is not None:
            layers.append(activation())

        return nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if not self._residual:
            return self._model(x)

        return x + self._model(x)


def main() -> None:
    mlp = MLP(
        input_dim=5,
        hidden_dim=10,
        n_layers=2
    )

    x = torch.randn(32, 5)  # (batch_size, dim)
    expected_shape = (32, 5)

    output = mlp(x)
    assert output.shape == expected_shape, f'Expected shape {expected_shape} but found {output.shape}!'


if __name__ == '__main__':
    main()
