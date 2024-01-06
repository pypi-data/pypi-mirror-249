"""
Filter factory.
"""
from torch import nn

from motrack_motion.datasets import transforms
from motrack_motion.datasets.torch import TrajectoryDataset
from motrack_motion.filter.end_to_end_filter import BufferedE2EFilter
from motrack_motion.filter.transfilter import TransFilter

FILTER_CATALOG = {
    'end_to_end': BufferedE2EFilter,
    'transfilter': TransFilter
}


def filter_factory(
    name: str,
    params: dict,
    model: nn.Module,
    transform: transforms.InvertibleTransformWithVariance,
) -> TrajectoryDataset:
    """
    Creates filter by given name.

    Args:
        name: Dataset name
        params: Filter parameters
        model: Filter core model
        transform: Filter preprocess - postprocess

    Returns:
        Initialized filter
    """
    name = name.lower()

    cls = DATASET_CATALOG[name]
    return cls(
        name=name,
        params=params,
        model=model,
        transform=transform
    )
