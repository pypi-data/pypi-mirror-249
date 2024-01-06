"""
End-to-end filter training module.
"""
from typing import Optional, Union, Tuple, Dict

import torch

from motrack_motion.datasets.transforms import InvertibleTransform, InvertibleTransformWithVariance
from motrack_motion.models.architectures.transfilter import TransFilter, pad_sequence
from motrack_motion.models.losses import factory_loss_function
from motrack_motion.models.train.base import LightningModuleBase, LightningTrainConfig
from motrack_motion.models.train.metrics import metrics_func


class TransFilterTrainingModule(LightningModuleBase):
    """
    PytorchLightning wrapper for TransFilter model.
    """
    def __init__(
        self,
        model: TransFilter,

        transform_func: Optional[Union[InvertibleTransform, InvertibleTransformWithVariance]] = None,

        prior_loss_weight: float = 1.0,
        posterior_loss_weight: float = 1.0,

        train_config: Optional[LightningTrainConfig] = None
    ):
        super().__init__(train_config=train_config)

        assert isinstance(model, TransFilter), f'Expected FilterModule but found {type(model)}'
        self._model = model

        # Loss weights
        self._prior_loss_weight = prior_loss_weight
        self._posterior_loss_weight = posterior_loss_weight

        self._loss_func = factory_loss_function(train_config.loss_name, train_config.loss_params) \
            if train_config is not None else None
        if transform_func is not None:
            assert isinstance(transform_func, InvertibleTransformWithVariance), \
                f'Expected transform function to be of type "InvertibleTransformWithStd" ' \
                f'but got "{type(transform_func)}"'
        self._transform_func = transform_func

    @property
    def core(self) -> TransFilter:
        """
        Get core model (without the training module).

        Returns:
            Core model
        """
        return self._model

    def forward(self, x_obs: torch.Tensor, t_obs: torch.Tensor, x_unobs: torch.Tensor, t_unobs: torch.Tensor, mask: Optional[torch.Tensor] = None) \
            -> Dict[str, torch.Tensor]:
        return self._model(x_obs, t_obs, x_unobs, t_unobs, mask=mask)

    def inference(self, x_obs: torch.Tensor, t_obs: torch.Tensor, x_unobs: torch.Tensor, t_unobs: torch.Tensor, mask: Optional[torch.Tensor] = None) \
            -> Dict[str, torch.Tensor]:
        """
        Inference (alias for forward)

        Args:
            x_obs: Observed data
            t_obs: Observed time points
            x_unobs: Unobserved data
            t_unobs: Unobserved time points
            mask: Transformer mask

        Returns:
            Prior and posterior estimation for future trajectory
        """
        return self._model(x_obs, t_obs, x_unobs, t_unobs, mask=mask)

    def _calc_loss_and_metrics(
        self,
        orig_bboxes_obs: torch.Tensor,
        orig_bboxes_unobs_prior: torch.Tensor,
        orig_bboxes_unobs_posterior: torch.Tensor,
        transformed_bboxes_unobs: torch.Tensor,
        bboxes_unobs_prior_mean: torch.Tensor,
        bboxes_unobs_posterior_mean: torch.Tensor,
        metadata: dict
    ) -> Tuple[Union[torch.Tensor, Dict[str, torch.Tensor]], Optional[Dict[str, float]]]:
        prior_loss = self._loss_func(bboxes_unobs_prior_mean, transformed_bboxes_unobs)
        posterior_loss = self._loss_func(bboxes_unobs_posterior_mean, transformed_bboxes_unobs)

        if isinstance(prior_loss, dict) and isinstance(posterior_loss, dict):
            prior_loss, posterior_loss = prior_loss['loss'], posterior_loss['loss']
        loss = {
            'prior_loss': prior_loss,
            'posterior_loss': posterior_loss,
            'loss': self._prior_loss_weight * prior_loss + self._posterior_loss_weight * posterior_loss
        }

        if self._transform_func is not None:
            # Invert mean
            _, bboxes_unobs_prior_mean, *_ = self._transform_func.inverse([orig_bboxes_obs, bboxes_unobs_prior_mean, metadata, None],
                                                                          shallow=False)
            _, bboxes_unobs_posterior_mean, *_ = self._transform_func.inverse([orig_bboxes_obs, bboxes_unobs_posterior_mean, metadata, None],
                                                                              shallow=False)

        gt_traj = orig_bboxes_unobs_prior.detach().cpu().numpy()
        prior_traj = bboxes_unobs_prior_mean.detach().cpu().numpy()
        prior_metrics = metrics_func(gt_traj, prior_traj)
        prior_metrics = {f'prior_{name}': value for name, value in prior_metrics.items()}

        gt_traj = orig_bboxes_unobs_posterior.detach().cpu().numpy()
        posterior_traj = bboxes_unobs_posterior_mean.detach().cpu().numpy()
        posterior_metrics = metrics_func(gt_traj, posterior_traj)
        posterior_metrics = {f'posterior_{name}': value for name, value in posterior_metrics.items()}
        metrics = dict(list(prior_metrics.items()) + list(posterior_metrics.items()))

        return loss, metrics

    def _step(self, batch: Dict[str, Union[dict, torch.Tensor]], prefix: str) -> torch.Tensor:
        bboxes_obs, bboxes_aug_unobs, ts_obs, ts_unobs, orig_bboxes_obs, orig_bboxes_unobs, bboxes_unobs, metadata = batch.values()

        with torch.no_grad():
            bboxes_obs, ts_obs, mask = pad_sequence(bboxes_obs, ts_obs)

        outputs = self.forward(bboxes_obs, ts_obs, bboxes_aug_unobs, ts_unobs, mask=mask)

        loss, metrics = self._calc_loss_and_metrics(
            orig_bboxes_obs=orig_bboxes_obs,
            orig_bboxes_unobs_prior=orig_bboxes_unobs,
            orig_bboxes_unobs_posterior=orig_bboxes_unobs,
            transformed_bboxes_unobs=bboxes_unobs,
            bboxes_unobs_prior_mean=outputs['x_prior'],
            bboxes_unobs_posterior_mean=outputs['x_posterior'],
            metadata=metadata
        )
        self._log_loss(loss, prefix=prefix, log_step=True)
        self._log_metrics(metrics, prefix=prefix)

        return loss

    def training_step(self, batch: Dict[str, Union[dict, torch.Tensor]], *args, **kwargs) -> torch.Tensor:
        loss = self._step(batch, prefix='training')
        self._log_lr()
        return loss

    def validation_step(self, batch: Dict[str, Union[dict, torch.Tensor]], *args, **kwargs) -> torch.Tensor:
        loss = self._step(batch, prefix='val')
        return loss
