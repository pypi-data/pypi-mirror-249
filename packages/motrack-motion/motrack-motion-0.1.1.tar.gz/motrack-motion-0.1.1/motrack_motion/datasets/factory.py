"""
Dataset factory.
"""
from typing import Dict, Any, Optional, List

from motrack_motion.datasets.mot.core import MOTDataset
from motrack_motion.datasets.torch import TrajectoryDataset

DATASET_CATALOG = {
    'mot': MOTDataset
}


def dataset_factory(
    name: str,
    path: str,
    history_len: int,
    future_len: int,
    sequence_list: Optional[List[str]] = None,
    additional_params: Optional[Dict[str, Any]] = None
) -> TrajectoryDataset:
    """
    Creates dataset by given name.

    Args:
        name: Dataset name
        path: Dataset path
        history_len: Observed trajectory length
        future_len: Unobserved trajectory length
        sequence_list: Dataset split sequence list
        additional_params: Additional dataset parameters

    Returns:
        Initialized dataset
    """
    name = name.lower()

    additional_params = {} if additional_params is None else additional_params

    cls = DATASET_CATALOG[name]
    return cls(
        path=path,
        history_len=history_len,
        future_len=future_len,
        sequence_list=sequence_list,
        **additional_params
    )
