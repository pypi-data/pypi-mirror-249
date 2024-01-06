"""
Config structure. Config should be loaded as dictionary and parsed into GlobalConfig Python object. Benefits:
- Structure and type validation (using dacite library)
- Custom validations
- Python IDE autocomplete
"""
import logging
import os
from dataclasses import field
from typing import Optional, Dict, Any

from hydra.core.config_store import ConfigStore
from hydra.utils import instantiate
from omegaconf import OmegaConf
from pydantic.dataclasses import dataclass

from motrack_motion.common import project, conventions
from motrack_motion.datasets.augmentations import create_identity_augmentation_config

logger = logging.getLogger('ConfigParser')


@dataclass
class DatasetConfig:
    """
    Dataset config.
    - name: Dataset name
    - path: Path to the dataset
    - history_len: Number of observable input values
    - future_len: Number of unobservable output values (values that are being predicted)
    """
    name: str
    path: str
    history_len: int
    future_len: int

    additional_params: Optional[Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Postprocess and validation.
        """
        self.fullpath = None

    def get_dataset_split_path(self, split: str) -> str:
        """
        Gets dataset split path with MOT conventions.

        Args:
            split: Split name

        Returns:
            Dataset split path
        """
        assert split in ['train', 'val', 'test'], f'Invalid split name: {split}!'
        return os.path.join(self.fullpath, split)


@dataclass
class TransformConfig:
    """
    Features transform config. Used to transform input features. Optionally performs inverse operation to output values.
    - name: Name of transform class (type).
    - params: Transform parameters
    """
    name: str
    params: dict


@dataclass
class AugmentationsConfig:
    """
    Augmentations applied before or after transform:
    - before_transform: Composition of augmentations applied before transform function.
    - after_transform: Composition of augmentations applied after transform function.
    """
    before_transform_config: Optional[dict]
    after_transform_config: Optional[dict]
    after_batch_collate_config: Optional[dict]

    def __post_init__(self):
        """
        Validation: Check augmentation object instantiation
        """
        self.before_transform_config, self.after_transform_config, self.after_batch_collate_config = \
            [create_identity_augmentation_config() if cfg is None else cfg
             for cfg in [self.before_transform_config, self.after_transform_config, self.after_batch_collate_config]]

        self.before_transform = instantiate(OmegaConf.create(self.before_transform_config))
        self.after_transform = instantiate(OmegaConf.create(self.after_transform_config))
        self.after_batch_collate = instantiate(OmegaConf.create(self.after_batch_collate_config))

    @classmethod
    def default(cls) -> 'AugmentationsConfig':
        """
        Default augmentations (none) in case it is not defined.

        Returns:
            Default augmentations
        """
        # noinspection PyArgumentList
        return cls(
            before_transform_config=create_identity_augmentation_config(),
            after_transform_config=create_identity_augmentation_config(),
            after_batch_collate_config=create_identity_augmentation_config()
        )


@dataclass
class ModelConfig:
    """
    Model config:
    - type: Model (architecture) type
    - params: Model creation parameters
    """
    type: str
    params: dict


@dataclass
class ResourcesConfig:
    """
    Resources config (cpu/gpu, number of cpu cores, ...)
    - gpus: Number of gpus
    - accelerator: gpu/cpu
    - num_workers: cpu workers
    """
    devices: int
    accelerator: str
    num_workers: int


@dataclass
class TrainLoggingConfig:
    """
    Configs for script logging during model training (not important for inference).
    - path: TB logs path (deprecated)
    - log_every_n_steps: TB log frequency
    """
    path: str  # Deprecated (predefined by conventions)
    log_every_n_steps: int


@dataclass
class TrainCheckpointConfig:
    """
    Model checkpoint saving config.
    - metric_monitor: Chooses the best checkpoint based on metric name
    - resume_from: Start from chosen checkpoint (fine-tuning)
    """
    metric_monitor: str
    resume_from: Optional[str]


@dataclass
class TrainConfig:
    """
    Train configuration.
    - experiment: Name of the training experiment
    - batch_size: Training batch size
    - max_epochs: Number of epochs to train model

    - logging_cfg: TrainLoggingConfig
    - checkpoint_cfg: TrainCheckpointConfig

    - train_params: Training architecture specific parameters
    """
    type: str
    params: dict

    batch_size: int
    max_epochs: int

    logging_cfg: TrainLoggingConfig
    checkpoint_cfg: TrainCheckpointConfig

    inverse_transform_before_loss: bool = field(default=False)
    train_params: Optional[dict] = field(default_factory=dict)  # Model train params

    gradient_clip_val: Optional[float] = field(default=None)
    gradient_clip_algorithm: Optional[str] = field(default=None)


@dataclass
class EvalConfig:
    """
    Inference + Evaluation config
    - batch_size: inference batch size
    - inference_name: inference run name
    - split: what split to use for evaluation (train/val/test)
    - checkpoint: what checkpoint to use for evaluation

    - autoregressive: use autoregressive decorator
    - autoregressive_keep_history: requires `autoregressive` - keeps all history when predicting (not dropping last)
    """
    batch_size: int
    inference_name: str
    split: str
    checkpoint: Optional[str]

    # Autoregressive configs
    autoregressive: bool = field(default=False)
    autoregressive_keep_history: bool = field(default=False)

    # Override dataset configs
    dataset_future_len: Optional[int] = field(default=None)

    # Custom evaluation
    fps_multiplier: float = field(default=1.0)


@dataclass
class PathConfig:
    """
    Path configs
    - master: location where all final and intermediate results are stored
    - assets: location where datasets can be found
    """
    master: str
    assets: str

    @classmethod
    def default(cls) -> 'PathConfig':
        """
        Default path configuration is used if it is not defined in configs.

        Returns: Path configuration.
        """
        # noinspection PyArgumentList
        return cls(
            master=project.OUTPUTS_PATH,
            assets=project.ASSETS_PATH
        )


@dataclass
class GlobalConfig:
    """
    Scripts GlobalConfig
    """
    experiment: str
    resources: ResourcesConfig
    dataset: DatasetConfig
    transform: TransformConfig
    train: TrainConfig
    eval: EvalConfig
    model: ModelConfig

    augmentations: AugmentationsConfig = field(default_factory=AugmentationsConfig.default)
    path: PathConfig = field(default_factory=PathConfig.default)

    def __post_init__(self) -> None:
        """
        Postprocessing.
        """
        self.dataset.fullpath = os.path.join(self.path.assets, self.dataset.path)

    @property
    def experiment_path(self) -> str:
        """
        Get experiment path.

        Returns:
            Experiments path
        """
        return conventions.get_experiment_path(self.path.master, self.dataset.path, self.experiment)

# Configuring hydra config store
# If config has `- global_config` in defaults then
# full config is recursively instantiated
cs = ConfigStore.instance()
cs.store(name='global_config', node=GlobalConfig)
