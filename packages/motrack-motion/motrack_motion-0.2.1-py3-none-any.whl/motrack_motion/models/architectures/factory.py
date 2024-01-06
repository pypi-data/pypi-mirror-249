"""
Model factory method
"""
import enum
from typing import Union

from torch import nn

from motrack_motion.models.architectures.rnn_filter import RNNFilterModel
from motrack_motion.models.architectures.transfilter import TransFilter


class ModelType(enum.Enum):
    """
    Enumerated implemented architectures
    """
    # RNN
    RNN_FILTER = 'rnn_filter'
    TRANSFILTER = 'transfilter'

    @classmethod
    def from_str(cls, value: str) -> 'ModelType':
        for v in cls:
            if v.value.lower() == value.lower():
                return v

        raise ValueError(f'Can\'t create ModelType from "{value}". Possible values: {list(cls)}')


def model_factory(
    model_type: Union[ModelType, str],
    params: dict,
) -> nn.Module:
    """
    Model factory method.

    Args:
        model_type: Model type
        params: Model parameters'

    Returns:
        Model
    """
    if isinstance(model_type, str):
        model_type = ModelType.from_str(model_type)

    catalog = {
        ModelType.RNN_FILTER: RNNFilterModel,
        ModelType.TRANSFILTER: TransFilter
    }

    return catalog[model_type](**params)

