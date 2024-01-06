"""
Motrack-motion Lightning module training utility.
"""
from dataclasses import dataclass, field
from typing import Tuple, Union, Dict, Optional

import numpy as np
import pytorch_lightning as pl
import torch

from motrack_motion.models.train.meter import MetricMeter
from motrack_motion.utils import torch_helper


def extract_mean_and_var(bboxes_unobs_hat: torch.Tensor, bounded_variance: bool = False, bounded_value: float = 0.01) \
        -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Helper function for Gaussian model postprocess

    Args:
        bboxes_unobs_hat: Prediction
        bounded_variance: Bound minimal variance
        bounded_value: Bounded variance value

    Returns:
        bboxes_hat_mean, bboxes_hat_var
    """
    bboxes_unobs_hat = bboxes_unobs_hat.view(*bboxes_unobs_hat.shape[:-1], -1, 2)
    bboxes_unobs_hat_mean = bboxes_unobs_hat[..., 0]
    bboxes_unobs_hat_log_var = bboxes_unobs_hat[..., 1]

    if not bounded_variance:
        bboxes_unobs_hat_var = torch.exp(bboxes_unobs_hat_log_var)
    else:
        bboxes_unobs_hat_var = bounded_value + (1 - bounded_value) * torch.nn.functional.softplus(bboxes_unobs_hat_log_var)

    return bboxes_unobs_hat_mean, bboxes_unobs_hat_var


def extract_mean_and_std(bboxes_unobs_hat: torch.Tensor, bounded_variance: bool = False, bounded_value: float = 0.01) \
        -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Helper function for Gaussian model postprocess

    Args:
        bboxes_unobs_hat: Prediction
        bounded_variance: Bound minimal variance
        bounded_value: Bounded variance value

    Returns:
        bboxes_hat_mean, bboxes_hat_std
    """
    bboxes_unobs_hat_mean, bboxes_unobs_hat_var = extract_mean_and_var(bboxes_unobs_hat, bounded_variance, bounded_value)
    bboxes_unobs_hat_std = torch.sqrt(bboxes_unobs_hat_var)
    return bboxes_unobs_hat_mean, bboxes_unobs_hat_std


@dataclass
class LightningTrainConfig:
    """
    Training configuration for LightningForecaster.
    """
    loss_name: str = field(default='mse')
    loss_params: dict = field(default_factory=dict)

    learning_rate: float = field(default=1e-3)
    sched_lr_gamma: float = field(default=1.0)
    sched_lr_step: int = field(default=1)
    n_warmup_epochs: int = field(default=0)

    optim_name: str = field(default='default')
    optim_additional_params: dict = field(default_factory=dict)

    weight_decay: float = field(default=0.0)

    n_train_steps: int = field(default=1000)


class LightningModuleBase(pl.LightningModule):
    """
    PytorchLightning module wrapper with some simple default utilities.
    """
    def __init__(self, train_config: LightningTrainConfig):
        """
        Args:
            train_config: Universal training config
        """
        super().__init__()
        self._train_config = train_config
        self._meter = MetricMeter()

    @property
    def n_params(self) -> int:
        """
        Gets number of model parameters.

        Returns:
            Return number of model parameters
        """
        trainable_parameters = filter(lambda p: p.requires_grad, self.parameters())
        return sum(np.prod(p.size()) for p in trainable_parameters)

    def on_validation_epoch_end(self) -> None:
        for name, value in self._meter.get_all():
            show_on_prog_bar = name.endswith('/loss')
            self.log(name, value, prog_bar=show_on_prog_bar)

    def configure_optimizers(self):
        optim_name = self._train_config.optim_name.lower()
        optim_catalog = {
            'default': torch.optim.Adam,
            'sgd': torch.optim.SGD,
            'adam': torch.optim.Adam,
            'adamw': torch.optim.AdamW
        }
        optim_cls = optim_catalog[optim_name]

        optimizer = optim_cls(
            params=self._model.parameters(),
            lr=self._train_config.learning_rate,
            weight_decay=self._train_config.weight_decay
        )

        def warmup_scheduler_func(current_step: int):
            """
            Warmup scheduler learning rate multiplier for warm-up steps.

            Args:
                current_step: Current step

            Returns:
                Learning rate multiplier.
            """
            if self._train_config.n_warmup_epochs == 0:
                return 1.0
            return current_step / (self._train_config.n_warmup_epochs * self._train_config.n_train_steps)

        scheduler_obj = torch.optim.lr_scheduler.SequentialLR(
           optimizer=optimizer,
           schedulers=[
               torch.optim.lr_scheduler.LambdaLR(
                   optimizer=optimizer,
                   lr_lambda=warmup_scheduler_func
               ),
               torch.optim.lr_scheduler.StepLR(
                   optimizer=optimizer,
                   step_size=self._train_config.sched_lr_step * self._train_config.n_train_steps,
                   gamma=self._train_config.sched_lr_gamma
               )
           ],
           milestones=[self._train_config.n_warmup_epochs * self._train_config.n_train_steps]
        )

        scheduler = {
            'scheduler': scheduler_obj,
            'interval': 'step',
            'frequency': 1
        }

        return [optimizer], [scheduler]

    def _log_lr(self) -> None:
        """
        Logs learning rate at the current step.
        """
        # noinspection PyTypeChecker
        optimizer: torch.optim.Optimizer = self.optimizers()
        if isinstance(optimizer, list):
            optimizer = optimizer[0]
        lr = torch_helper.get_optim_lr(optimizer)
        self.log('general/lr', lr)

    def _log_loss(self, loss: Union[torch.Tensor, Dict[str, torch.Tensor]], prefix: str, log_step: bool = True) -> None:
        """
        Helper function to log loss. Options:
        - Single value: logged as "{prefix}/loss"
        - Dictionary: for each key log value as "{prefix}/{key}"

        Args:
            loss: Loss
            prefix: Prefix (train or val)
        """
        assert prefix in ['training', 'val'], f'Invalid prefix value "{prefix}"!'

        if isinstance(loss, dict):
            assert 'loss' in loss, \
                f'When returning loss as dictionary it has to have key "loss". Found: {list(loss.keys())}'
            for name, value in loss.items():
                value = value.detach().cpu()
                assert not torch.isnan(value).any(), f'Got nan value for key "{name}"!'
                self._meter.push(f'{prefix}-epoch/{name}', value)
                if log_step:
                    self.log(f'{prefix}/{name}', value, prog_bar=False)
        else:
            loss = loss.detach().cpu()
            assert not torch.isnan(loss).any(), 'Got nan value!'
            loss = loss.detach().cpu()
            self._meter.push(f'{prefix}-epoch/loss', loss)
            if log_step:
                self.log(f'{prefix}/loss', loss, prog_bar=False)

    def _log_metrics(self, metrics: Optional[Dict[str, float]], prefix: str) -> None:
        """
        Helper function to log metrics. Input format:
        - Dictionary: for each key log value as "{prefix}-epoch/{key}"

        Args:
            prefix: Prefix (train or val)
        """
        if metrics is None:
            return

        assert prefix in ['training', 'val'], f'Invalid prefix value "{prefix}"!'
        for name, value in metrics.items():
            self._meter.push(f'{prefix}-metrics/{name}', value)
