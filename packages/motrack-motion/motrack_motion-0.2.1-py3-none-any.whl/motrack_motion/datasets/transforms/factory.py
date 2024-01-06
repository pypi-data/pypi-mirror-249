"""
Transform factory method.
"""
from motrack_motion.datasets.transforms import (
    InvertibleTransform,
    InvertibleTransformWithVariance,
    IdentityTransform,
    BboxFirstOrderDifferenceTransform,
    BBoxStandardizationTransform,
    BBoxStandardizedFirstOrderDifferenceTransform,
    BBoxRelativeToLastObsTransform,
    BBoxStandardizedRelativeToLastObsTransform,
    BBoxCompositeTransform,
    BBoxJackOfAllTradesTransform,
)
from typing import Union


def transform_factory(name: str, params: dict) -> Union[InvertibleTransform, InvertibleTransformWithVariance]:
    """
    Create transform object based on given name and constructor parameters.

    Args:
        name: Transform name
        params: Transform parameters

    Returns:
        Transform object
    """
    catalog = {
        'identity': IdentityTransform,
        'composite': BBoxCompositeTransform,
        'first_difference': BboxFirstOrderDifferenceTransform,
        'standardization': BBoxStandardizationTransform,
        'standardized_first_difference': BBoxStandardizedFirstOrderDifferenceTransform,
        'relative_to_last_obs': BBoxRelativeToLastObsTransform,
        'standardized_relative_to_last_obs': BBoxStandardizedRelativeToLastObsTransform,
        'jack_of_all_trades': BBoxJackOfAllTradesTransform
    }

    cls = catalog[name]

    if name == 'composite':
        params['transforms'] = [transform_factory(child['name'], child['params']) for child in params['transforms']]

    return cls(**params)
