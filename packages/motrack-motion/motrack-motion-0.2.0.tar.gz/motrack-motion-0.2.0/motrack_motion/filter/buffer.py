"""
Filter's observation buffer.
"""
from typing import Tuple, List
from abc import ABC

import torch
from torch import nn

from motrack_motion.datasets import transforms
from motrack_motion.filter.base import StateModelFilter


class ObservationBuffer:
    """
    Buffers trajectory observations.
    """
    def __init__(
        self,
        size: int,
        min_size: int,
        min_history: int = 1,
        dtype: torch.dtype = torch.float32,
    ):
        assert size >= 1, f'Invalid size {size}. Minimum size is 1.'

        self._size = size
        self._min_size = min_size
        self._dtype = dtype
        self._min_history = min_history

        self._buffer: List[Tuple[int, torch.Tensor]] = []
        self._t = 0

    @property
    def last_obs_time(self) -> int:
        return self._buffer[-1][0]

    @property
    def time(self) -> int:
        return self._t

    @property
    def has_input(self) -> bool:
        return len(self._buffer) >= self._min_size

    def push(self, x: torch.Tensor) -> None:
        self._buffer.append((self._t, x))
        self.increment()

    def increment(self) -> None:
        if len(self._buffer) > self._min_history and (self._t - self._buffer[0][0]) >= self._size:
            self._buffer.pop(0)

        self._t += 1

    def get_input(self, n_future_steps: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        n_hist_steps = len(self._buffer)
        ts_obs, x_obs = zip(*self._buffer)
        ts_obs_first = ts_obs[0]

        # Form history trajectory
        x_obs = torch.stack(x_obs).view(n_hist_steps, 1, -1)
        ts_obs = torch.tensor(ts_obs, dtype=self._dtype).view(-1, 1, 1)

        # Form estimation trajectory time interval
        ts_unobs = torch.tensor(list(range(self._t, self._t + n_future_steps)),
                                dtype=self._dtype).view(-1, 1, 1)

        ts_obs = ts_obs - ts_obs_first + 1
        ts_unobs = ts_unobs - ts_obs_first + 1

        return x_obs, ts_obs, ts_unobs

    def clear(self) -> None:
        self._buffer.clear()

    def __len__(self) -> int:
        return len(self._buffer)


class BufferedStateModel(StateModelFilter, ABC):
    """
    Buffered state model
    """
    def __init__(
        self,
        model: nn.Module,
        transform: transforms.InvertibleTransformWithVariance,
        accelerator: str,

        buffer_size: int,
        buffer_min_size: int = 1,
        buffer_min_history: int = 5,
        dtype: torch.dtype = torch.float32,

        recursive_inverse: bool = False,
        uncertainty_multiplier: float = 10.0
    ):
        """
        Args:
            model: Model
            transform: Transform function
            accelerator: cpu/gpu accelerator
            buffer_size: Buffer size
            buffer_min_size: Minimum size to run model (default 1)
            buffer_min_history: Minimum history to save
            dtype: Torch datatype
            recursive_inverse: Apply recursive inverse transform
            uncertainty_multiplier: Uncertainty multiplier in case model does not estimate the uncertainty
        """
        self._model = model
        self._transform = transform
        self._accelerator = accelerator
        self._dtype = dtype

        self._buffer_size = buffer_size
        self._buffer_min_size = buffer_min_size
        self._buffer_min_history = buffer_min_history

        # Model
        self._model.to(self._accelerator)
        self._model.eval()

        self._recursive_inverse = recursive_inverse
        self._uncertainty_multiplier = uncertainty_multiplier

    def _create_buffer(self, measurement: torch.Tensor) -> ObservationBuffer:
        """
        Creates buffer with initial measurement.

        Args:
            measurement: Initial buffer measurement

        Returns:
            Buffer
        """
        buffer = ObservationBuffer(
            size=self._buffer_size,
            min_size=self._buffer_min_size,
            min_history=self._buffer_min_history,
            dtype=self._dtype
        )
        buffer.push(measurement)
        return buffer
