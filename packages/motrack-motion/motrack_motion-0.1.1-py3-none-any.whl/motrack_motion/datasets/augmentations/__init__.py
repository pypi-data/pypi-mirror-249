"""
Implementation of training augmentations
"""
from motrack_motion.datasets.augmentations.trajectory import (
    TrajectoryAugmentation,
    IdentityAugmentation,
    GaussianNoiseAugmentation,
    CompositionAugmentation,
    create_identity_augmentation_config
)
