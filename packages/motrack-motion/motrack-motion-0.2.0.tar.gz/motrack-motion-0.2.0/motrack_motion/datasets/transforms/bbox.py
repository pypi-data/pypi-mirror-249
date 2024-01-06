"""
BBox transformations. Contains
- BBox trajectory first order difference transformation
- BBox coordination standardization to N(0, 1)
- BBox trajectory standardized first order difference transformation
- BBox trajectory relative to the last observed point
- BBox trajectory standardized relative to the last observed point transformation
- BBox transform composition
- BBox coordination standardization to N(0, 1) (by category)
"""

from typing import Union, List, Optional

import torch

from motrack_motion.datasets.transforms.base import InvertibleTransformWithVariance, TensorCollection


class BboxFirstOrderDifferenceTransform(InvertibleTransformWithVariance):
    """
    Applies first difference transformation:
    Y[i] = X[i] - X[i-1]
    Y[0] is removed

    If `scale_by_time_diff=True` then:
    Y[i] = X[i] - X[i-1] / (T[i] - T[i-1])
    """
    def __init__(self, scale_by_time_diff: bool = False):
        """
        Args:
            scale_by_time_diff: Scale difference by time difference
                - Useful in case of missing observed points
        """
        super().__init__(name='first_difference')
        self._scale_by_time_diff = scale_by_time_diff

    def apply(self, data: TensorCollection, shallow: bool = True) -> TensorCollection:
        bbox_obs, bbox_unobs, ts_obs, ts_unobs, *other = data
        assert bbox_obs.shape[0] >= 0, f'{self.__name__} requires at least 2 observable points. ' \
                                       f'Found {bbox_obs.shape[0]}'

        assert not shallow
        if not shallow:
            bbox_obs = bbox_obs.clone()
            bbox_unobs = bbox_unobs.clone() if bbox_unobs is not None else None
            ts_obs = ts_obs.clone()

        if bbox_unobs is not None:
            # During live inference, bbox_unobs are not known (this is for training only)
            bbox_unobs[1:, ...] = bbox_unobs[1:, ...] - bbox_unobs[:-1, ...]
            bbox_unobs[0, ...] = bbox_unobs[0, ...] - bbox_obs[-1, ...]

        bbox_obs[1:, ...] = bbox_obs[1:, ...] - bbox_obs[:-1, ...]
        if self._scale_by_time_diff:
            bbox_obs[1:, ...] = bbox_obs[1:, ...] / (ts_obs[1:, ...] - ts_obs[:-1, ...])

        bbox_obs, ts_obs = bbox_obs[1:, ...], ts_obs[1:, ...]  # Dump first

        return bbox_obs, bbox_unobs, ts_obs, ts_unobs, *other

    def inverse(self, data: TensorCollection, shallow: bool = True) -> TensorCollection:
        orig_bbox_obs, bbox_hat, *other = data
        if not shallow:
            bbox_hat = bbox_hat.clone()

        bbox_hat[0, ...] = bbox_hat[0, ...] + orig_bbox_obs[-1, ...]
        bbox_hat = torch.cumsum(bbox_hat, dim=0)

        return orig_bbox_obs, bbox_hat, *other

    def inverse_std(
        self,
        t_std: torch.Tensor,
        additional_data: Optional[TensorCollection] = None,
        shallow: bool = True
    ) -> TensorCollection:
        # Check `inverse_var`
        t_var = torch.square(t_std)
        t_var_cumsum = torch.cumsum(t_var, dim=0)
        t_std_cumsum = torch.sqrt(t_var_cumsum)
        return t_std_cumsum

    def inverse_var(
        self,
        t_var: torch.Tensor,
        additional_data: Optional[TensorCollection] = None,
        shallow: bool = True
    ) -> TensorCollection:
        # In order to estimate std for inverse two assumptions are added
        # 1. Random variables y[i-1] and y[i] are independent
        # 2. Variance of last observed bbox coordinate is 0 (i.e. var(x[-1]) = 0)
        # Let: y - transformed, x - original, 0 - first unobserved time point
        # Transformation: y[i] = x[i] - x[i-1]
        # Inverse transformation: x[i] = y[i] + x[i-1]
        # Known variances: y[i] and x[-1]
        # => var(x[0]) = var(y[0]) + var(x[-1]) = var(y[0])  # from (1) and (2)
        # => var(x[1]) = var(y[1]) + var(x[0]) = var(y[0]) + var(y[1]))  # from (1)
        # ...
        # => var(x[i]) = var(y[i]) + var(x[i-1]) = sum[j=0,i] var(y[j])
        return torch.cumsum(t_var, dim=0)


class BBoxStandardizationTransform(InvertibleTransformWithVariance):
    """
    Applies standardization transformation:
    Y[i] = (X[i] - mean(X)) / std(X)
    """
    def __init__(self, mean: Union[float, List[float]], std: Union[float, List[float]]):
        super().__init__(name='standardization')
        self._mean = mean
        self._std = std

        if isinstance(self._mean, float):
            # Convert to list
            self._mean = [self._mean] * 4

        if isinstance(self._std, float):
            # Convert to list
            self._std = [self._std] * 4

        self._mean = torch.tensor(self._mean, dtype=torch.float32)
        self._std = torch.tensor(self._std, dtype=torch.float32)

    def apply(self, data: TensorCollection, shallow: bool = True) -> TensorCollection:
        bbox_obs, bbox_unobs, *other = data
        mean = self._mean.to(bbox_obs)
        std = self._std.to(bbox_obs)

        bbox_obs = (bbox_obs - mean) / std
        # During live inference, bbox_unobs are not known (this is for training only)
        bbox_unobs = (bbox_unobs - mean) / std if bbox_unobs is not None else None

        return bbox_obs, bbox_unobs, *other

    def inverse(self, data: TensorCollection, shallow: bool = True, n_samples: int = 1) -> TensorCollection:
        bbox_obs, bbox_unobs, *other = data
        mean = self._mean.to(bbox_obs)
        std = self._std.to(bbox_obs)

        if n_samples == 1:
            # Note: inverse transform is not applied to `bbox_obs`
            bbox_unobs = bbox_unobs * std + mean
        else:
            # Support (Improvisation) for VAE monte carlo sampling for mean and std estimation
            mean_repeated = mean.repeat(n_samples)
            std_repeated = std.repeat(n_samples)
            bbox_unobs = bbox_unobs * std_repeated + mean_repeated

        return bbox_obs, bbox_unobs, *other

    def inverse_std(
        self,
        t_std: torch.Tensor,
        additional_data: Optional[TensorCollection] = None,
        shallow: bool = True
    ) -> TensorCollection:
        # Std of inverse transformation in this case is trivial to calculate
        # y - transformed, x - original
        # y[i] = (x[i] - m) / s
        # => x[i] = y[i] * s + m
        # => std(x) = std(y) * s
        std = self._std.to(t_std)
        return t_std * std

    def inverse_var(
        self,
        t_var: torch.Tensor,
        additional_data: Optional[TensorCollection] = None,
        shallow: bool = True
    ) -> TensorCollection:
        # Similar to `inverse_std`
        std = self._std.to(t_var)
        return t_var * torch.square(std)


class BBoxCompositeTransform(InvertibleTransformWithVariance):
    """
    Compose multiple transform functions.
    """
    def __init__(self, transforms: List[InvertibleTransformWithVariance]):
        """
        Args:
            transforms: List of transform functions to compose
        """
        super().__init__(name='composite')
        self._transforms = transforms

    def apply(self, data: TensorCollection, shallow: bool = True) -> TensorCollection:
        for t in self._transforms:
            data = t.apply(data, shallow=shallow)
        return data

    def inverse(self, data: TensorCollection, shallow: bool = True) -> TensorCollection:
        for t in self._transforms[::-1]:
            data = t.inverse(data, shallow=shallow)
        return data

    def inverse_std(
        self,
        t_std: torch.Tensor,
        additional_data: Optional[TensorCollection] = None,
        shallow: bool = True
    ) -> TensorCollection:
        for t in self._transforms[::-1]:
            t_std = t.inverse_std(t_std, additional_data=additional_data, shallow=shallow)
        return t_std

    def inverse_var(
        self,
        t_var: torch.Tensor,
        additional_data: Optional[TensorCollection] = None,
        shallow: bool = True
    ) -> TensorCollection:
        for t in self._transforms[::-1]:
            t_var = t.inverse_var(t_var, additional_data=additional_data, shallow=shallow)
        return t_var


class BBoxStandardizedFirstOrderDifferenceTransform(BBoxCompositeTransform):
    """
    This is still here for back-compatibility...

    Step 1: Applies first difference transformation:
    Y[i] = X[i] - X[i-1]
    Y[0] is removed

    Step 2: Applies standardization transformation:
    Z[i] = (Y[i] - mean(Y)) / std(Y)
    """
    def __init__(self, mean: Union[float, List[float]], std: Union[float, List[float]], scale_by_time_diff: bool = False):
        transforms = [
            BboxFirstOrderDifferenceTransform(scale_by_time_diff=scale_by_time_diff),
            BBoxStandardizationTransform(mean=mean, std=std)
        ]
        super().__init__(transforms=transforms)


class BBoxRelativeToLastObsTransform(InvertibleTransformWithVariance):
    """
    * For all observed coordinates:
    Y[i] = X[-1] - X[i]
    Y[-1] is removed

    * For all unobserved coordinates:
    Y[i] = X[i] - X[-1]
    """
    def __init__(self):
        super().__init__(name='relative_to_last_obs')

    def apply(self, data: TensorCollection, shallow: bool = True) -> TensorCollection:
        bbox_obs, bbox_unobs, ts_obs, ts_unobs, *other = data
        last_obs = bbox_obs[-1:]

        if not shallow:
            bbox_obs = bbox_obs.clone()
            bbox_unobs = bbox_unobs.clone() if bbox_unobs is not None else None

        bbox_obs, ts_obs = bbox_obs[:-1], ts_obs[:-1]  # Last element becomes redundant
        ts_unobs = ts_unobs - 1  # Shifting back since the last time point is deleted
        bbox_obs = last_obs.expand_as(bbox_obs) - bbox_obs
        bbox_unobs = bbox_unobs - last_obs.expand_as(bbox_unobs) if bbox_unobs is not None else None

        return bbox_obs, bbox_unobs, ts_obs, ts_unobs, *other

    def inverse(self, data: TensorCollection, shallow: bool = True) -> TensorCollection:
        orig_bbox_obs, bbox_hat, *other = data
        last_obs = orig_bbox_obs[-1:]

        if not shallow:
            bbox_hat = bbox_hat.clone()

        bbox_hat = bbox_hat + last_obs.expand_as(bbox_hat)

        return orig_bbox_obs, bbox_hat, *other

    def inverse_std(
        self,
        t_std: torch.Tensor,
        additional_data: Optional[TensorCollection] = None,
        shallow: bool = True
    ) -> TensorCollection:
        return t_std  # It's assumed that last observed element has variance equal to 0

    def inverse_var(
        self,
        t_var: torch.Tensor,
        additional_data: Optional[TensorCollection] = None,
        shallow: bool = True
    ) -> TensorCollection:
        return t_var  # It's assumed that last observed element has variance equal to 0


class BBoxStandardizedRelativeToLastObsTransform(BBoxCompositeTransform):
    """
    This is still here for back-compatibility...

    Step 1: Applies first difference transformation:
    * For all observed coordinates:
    Y[i] = X[-1] - X[i]
    Y[-1] is removed

    * For all unobserved coordinates:
    Y[i] = X[i] - X[-1]

    Step 2: Applies standardization transformation:
    Z[i] = (Y[i] - mean(Y)) / std(Y)
    """
    def __init__(self, mean: float, std: float):
        transforms = [
            BBoxRelativeToLastObsTransform(),
            BBoxStandardizationTransform(mean=mean, std=std)
        ]

        super().__init__(transforms=transforms)


class BBoxJackOfAllTradesTransform(InvertibleTransformWithVariance):
    """
    This transformation uses benefits of both relative and diff coordinates.
    Also takes into consideration the absolute object coordinates.
    """
    def __init__(
        self,
        rel_mean: float,
        rel_std: float,
        diff_mean: float,
        diff_std: float,
        rel_unobs: bool = True,
        diff_scale_by_ts_diff: bool = False
    ):
        """
        Args:
            rel_mean: Relative coordinates mean
            rel_std: Relative coordinates std
            diff_mean: Diff coordinates mean
            diff_std: Diff coordinate std
            rel_unobs: If true then Use relative coordinates for prediction
                else use diff coordinates for prediction
            diff_scale_by_ts_diff: Scale feature difference by time difference
        """
        super().__init__(name='jack_of_all_trades')
        self._rel_transform = BBoxStandardizedRelativeToLastObsTransform(mean=rel_mean, std=rel_std)
        self._diff_transform = BBoxStandardizedFirstOrderDifferenceTransform(mean=diff_mean, std=diff_std, scale_by_time_diff=diff_scale_by_ts_diff)
        self._rel_unobs = rel_unobs

    def apply(self, data: TensorCollection, shallow: bool = True) -> TensorCollection:
        bbox_obs, bbox_unobs, ts_obs, ts_unobs, *other = data
        rel_bbox_obs, rel_bbox_unobs, rel_ts_obs, rel_ts_unobs, *_ = \
            self._rel_transform([bbox_obs, bbox_unobs, ts_obs, ts_unobs, None], shallow=False)
        diff_bbox_obs, diff_bbox_unobs, *_ = self._diff_transform([bbox_obs, bbox_unobs, ts_obs, None], shallow=False)
        bbox_obs = bbox_obs[1:]
        bbox_features = torch.cat([rel_bbox_obs, diff_bbox_obs, bbox_obs], dim=-1)

        bbox_unobs = rel_bbox_unobs if self._rel_unobs else diff_bbox_unobs
        return bbox_features, bbox_unobs, rel_ts_obs, rel_ts_unobs, *other

    def inverse(self, data: TensorCollection, shallow: bool = True) -> TensorCollection:
        if self._rel_unobs:
            return self._rel_transform.inverse(data, shallow=shallow)
        return self._diff_transform.inverse(data, shallow=shallow)

    def inverse_std(self, t_std: torch.Tensor, additional_data: Optional[TensorCollection] = None, shallow: bool = True) -> TensorCollection:
        if self._rel_unobs:
            return self._rel_transform.inverse_std(t_std, additional_data=additional_data, shallow=shallow)
        return self._diff_transform.inverse_std(t_std, additional_data=additional_data, shallow=shallow)

    def inverse_var(self, t_var: torch.Tensor, additional_data: Optional[TensorCollection] = None, shallow: bool = True) -> TensorCollection:
        if self._rel_unobs:
            return self._rel_transform.inverse_var(t_var, additional_data=additional_data, shallow=shallow)
        return self._diff_transform.inverse_var(t_var, additional_data=additional_data, shallow=shallow)


# noinspection DuplicatedCode
def run_test_first_difference() -> None:
    bbox_obs = torch.randn(2, 2, 4)
    bbox_unobs = torch.randn(3, 2, 4)
    ts_obs = torch.tensor([1, 3], dtype=torch.float32).view(-1, 1, 1).repeat(1, 2, 1)
    ts_unobs = torch.tensor([4, 5, 6], dtype=torch.float32).view(-1, 1, 1).repeat(1, 2, 1)

    for scale_by_time_diff in [False, True]:
        first_diff = BboxFirstOrderDifferenceTransform(scale_by_time_diff=scale_by_time_diff)

        transformed_bbox_obs, transformed_bbox_unobs, *_ = \
            first_diff.apply([bbox_obs, bbox_unobs, ts_obs, ts_unobs, None], shallow=False)
        print(transformed_bbox_obs)
        assert transformed_bbox_obs.shape == (1, 2, 4)
        assert transformed_bbox_unobs.shape == (3, 2, 4)

        _, inv_transformed_bbox_unobs, *_ = first_diff.inverse([bbox_obs, transformed_bbox_unobs, None])
        assert torch.abs(inv_transformed_bbox_unobs - bbox_unobs).sum().item() < 1e-3


def run_test_standardization() -> None:
    bbox_obs = torch.randn(2, 2, 4)
    bbox_unobs = torch.randn(3, 2, 4)
    ts_obs = torch.randn(2, 2, 1)
    ts_unobs = torch.randn(3, 2, 1)
    first_diff = BBoxStandardizationTransform(1, 2.0)

    _, transformed_bbox_unobs, *_ = \
        first_diff.apply([bbox_obs, bbox_unobs, ts_obs, ts_unobs, None], shallow=False)

    _, inv_transformed_bbox_unobs, *_ = first_diff.inverse([bbox_obs, transformed_bbox_unobs, None])
    assert torch.abs(inv_transformed_bbox_unobs - bbox_unobs).sum().item() < 1e-3


# noinspection DuplicatedCode
def run_test_standardized_first_difference() -> None:
    bbox_obs = torch.randn(2, 2, 4)
    bbox_unobs = torch.randn(3, 2, 4)
    ts_obs = torch.randn(2, 2, 1)
    ts_unobs = torch.randn(3, 2, 1)
    first_diff = BBoxStandardizedFirstOrderDifferenceTransform(1, 2.0)

    transformed_bbox_obs, transformed_bbox_unobs, *_ = \
        first_diff.apply([bbox_obs, bbox_unobs, ts_obs, ts_unobs, None], shallow=False)
    assert transformed_bbox_obs.shape == (1, 2, 4)
    assert transformed_bbox_unobs.shape == (3, 2, 4)

    _, inv_transformed_bbox_unobs, *_ = first_diff.inverse([bbox_obs, transformed_bbox_unobs, None])
    assert torch.abs(inv_transformed_bbox_unobs - bbox_unobs).sum().item() < 1e-3


# noinspection DuplicatedCode
def run_test_relative_to_last_obs() -> None:
    bbox_obs = torch.randn(2, 2, 4)
    bbox_unobs = torch.randn(3, 2, 4)
    ts_obs = torch.randn(2, 2, 1)
    ts_unobs = torch.randn(3, 2, 1)
    first_diff = BBoxRelativeToLastObsTransform()

    transformed_bbox_obs, transformed_bbox_unobs, *_ = \
        first_diff.apply([bbox_obs, bbox_unobs, ts_obs, ts_unobs, None], shallow=False)
    assert transformed_bbox_obs.shape == (1, 2, 4)
    assert transformed_bbox_unobs.shape == (3, 2, 4)

    _, inv_transformed_bbox_unobs, *_ = first_diff.inverse([bbox_obs, transformed_bbox_unobs, None])
    assert torch.abs(inv_transformed_bbox_unobs - bbox_unobs).sum().item() < 1e-3


# noinspection DuplicatedCode
def run_test_standardized_relative_to_last_obs() -> None:
    bbox_obs = torch.randn(2, 2, 4)
    bbox_unobs = torch.randn(3, 2, 4)
    ts_obs = torch.randn(2, 2, 1)
    ts_unobs = torch.randn(3, 2, 1)
    first_diff = BBoxStandardizedRelativeToLastObsTransform(1, 2.0)

    transformed_bbox_obs, transformed_bbox_unobs, *_ = \
        first_diff.apply([bbox_obs, bbox_unobs, ts_obs, ts_unobs, None], shallow=False)
    assert transformed_bbox_obs.shape == (1, 2, 4)
    assert transformed_bbox_unobs.shape == (3, 2, 4)

    _, inv_transformed_bbox_unobs, *_ = first_diff.inverse([bbox_obs, transformed_bbox_unobs, None])
    assert torch.abs(inv_transformed_bbox_unobs - bbox_unobs).sum().item() < 1e-3


def run_test_jack_of_all_trades() -> None:
    for use_rel_unobs in [True, False]:
        bbox_obs = torch.randn(2, 2, 4)
        bbox_unobs = torch.randn(3, 2, 4)
        ts_obs = torch.randn(2, 2, 1)
        ts_unobs = torch.randn(3, 2, 1)
        jack_of_all_trades = BBoxJackOfAllTradesTransform(1.0, 2.0, 1.0, 2.0, rel_unobs=use_rel_unobs)

        transformed_bbox_obs, transformed_bbox_unobs, *_ = \
            jack_of_all_trades.apply([bbox_obs, bbox_unobs, ts_obs, ts_unobs, None], shallow=False)
        assert transformed_bbox_obs.shape == (1, 2, 12)
        assert transformed_bbox_unobs.shape == (3, 2, 4)

        _, inv_transformed_bbox_unobs, *_ = jack_of_all_trades.inverse([bbox_obs, transformed_bbox_unobs, None])
        assert torch.abs(inv_transformed_bbox_unobs - bbox_unobs).sum().item() < 1e-3


if __name__ == '__main__':
    run_test_first_difference()
    run_test_standardization()
    run_test_standardized_first_difference()
    run_test_relative_to_last_obs()
    run_test_standardized_relative_to_last_obs()
    run_test_jack_of_all_trades()

    # TODO: Move to tests
