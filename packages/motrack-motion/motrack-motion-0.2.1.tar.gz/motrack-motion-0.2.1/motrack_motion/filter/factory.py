"""
Filter factory.
"""
from torch import nn

from motrack_motion.datasets import transforms
from motrack_motion.filter.end_to_end_filter import BufferedE2EFilter
from motrack_motion.filter.transfilter import TransFilter
from motrack_motion.filter.base import StateModelFilter

FILTER_CATALOG = {
    'end_to_end': BufferedE2EFilter,
    'transfilter': TransFilter
}


def filter_factory(
    name: str,
    params: dict,
    model: nn.Module,
    transform: transforms.InvertibleTransformWithVariance,
) -> StateModelFilter:
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

    cls = FILTER_CATALOG[name]
    return cls(
        name=name,
        params=params,
        model=model,
        transform=transform
    )
