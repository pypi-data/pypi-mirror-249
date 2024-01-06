"""
Model factory method
"""
import enum
from typing import Union, Optional

from motrack_motion.datasets.transforms import InvertibleTransform, InvertibleTransformWithVariance
from motrack_motion.models.architectures.factory import ModelType, model_factory
from motrack_motion.models.train.base import LightningTrainConfig, LightningModuleBase
from motrack_motion.models.train.end_to_end import EndToEndFilterTrainingModule
from motrack_motion.models.train.transfilter import TransFilterTrainingModule


class TrainingModuleType(enum.Enum):
    """
    Enumerated implemented training modules
    """
    END_TO_END = 'end_to_end'
    TRANSFILTER = 'transfilter'


    @classmethod
    def from_str(cls, value: str) -> 'TrainingModuleType':
        for v in cls:
            if v.value.lower() == value.lower():
                return v

        raise ValueError(f'Can\'t create ModelType from "{value}". Possible values: {list(cls)}')


def load_or_create_training_module(
    train_module_type: Union[TrainingModuleType, str],
    train_module_params: dict,
    model_type: Union[ModelType, str],
    model_params: dict,
    checkpoint_path: Optional[str] = None,
    n_train_steps: Optional[int] = None,
    train_params: Optional[dict] = None,
    transform_func: Optional[Union[InvertibleTransform, InvertibleTransformWithVariance]] = None
) -> LightningModuleBase:
    """
    Loads trained (if given checkpoint path) or creates new model given name and parameters.
    If model is trainable (check ModelType) then it can use train config. Otherwise, it can be loaded from checkpoint.
    Parameters combinations:
    - checkpoint_path is None and train_params is None - not allowed
    - checkpoint_path is None and train_params is not None - model is used for training from scratch
    - checkpoint_path is not None and train_params is None - model is used for inference
    - checkpoint_path is None and train_params is None - model is used for training from checkpoint (continue training)
    Args:
        train_module_type: Module type
        train_module_params: Module parameters
        model_type: Model type
        model_params: Model parameters
        checkpoint_path: Load pretrained model
        n_train_steps: Number of train steps
        train_params: Parameters for model training
        transform_func: Transform function (applied before loss)
    Returns:
        Model
    """
    if isinstance(train_module_type, str):
        train_module_type = TrainingModuleType.from_str(train_module_type)

    catalog = {
        TrainingModuleType.END_TO_END: EndToEndFilterTrainingModule,
        TrainingModuleType.TRANSFILTER: TransFilterTrainingModule
    }

    # Load model
    model = model_factory(model_type, model_params)

    if n_train_steps is not None:
        # Override train steps
        train_params['n_train_steps'] = n_train_steps

    # Create training config
    train_config = LightningTrainConfig(**train_params) if train_params is not None else None
    if checkpoint_path is None and train_config is None:
        raise ValueError('Train config and checkpoint path can\'t be both None!')

    # Create training module
    module_cls = catalog[train_module_type]
    if checkpoint_path is not None:
        return module_cls.load_from_checkpoint(
            **train_module_params,
            model=model,
            checkpoint_path=checkpoint_path,
            train_config=train_config,
            transform_func=transform_func
        )

    # noinspection PyTypeChecker
    return module_cls(
        **train_module_params,
        model=model,
        train_config=train_config,
        transform_func=transform_func
    )
