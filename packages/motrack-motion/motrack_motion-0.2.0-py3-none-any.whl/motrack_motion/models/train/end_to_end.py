"""
End-to-end filter training module.
"""
import random
from typing import Optional, Union, List, Tuple, Dict

import torch

from motrack_motion.datasets.augmentations.trajectory import remove_points
from motrack_motion.datasets.transforms import InvertibleTransform, InvertibleTransformWithVariance
from motrack_motion.models.architectures.end_to_end import FilterModule
from motrack_motion.models.losses import factory_loss_function
from motrack_motion.models.train.base import LightningModuleBase, LightningTrainConfig
from motrack_motion.models.train.metrics import metrics_func


class EndToEndFilterTrainingModule(LightningModuleBase):
    """
    PytorchLightning wrapper for FilterModule model.
    """
    def __init__(
        self,
        model: FilterModule,

        transform_func: Optional[Union[InvertibleTransform, InvertibleTransformWithVariance]] = None,

        augmentation_remove_points_enable: bool = False,
        augmentation_remove_random_points_proba: float = 0.15,
        augmentation_remove_sequence_proba: float = 0.15,

        prior_loss_weight: float = 1.0,
        posterior_loss_weight: float = 1.0,

        train_config: Optional[LightningTrainConfig] = None,
        log_epoch_metrics: bool = True
    ):
        super().__init__(train_config=train_config)

        assert isinstance(model, FilterModule), f'Expected FilterModule but found {type(model)}'
        self._model = model

        # Augmentations
        self._augmentation_remove_points_enable = augmentation_remove_points_enable
        self._augmentation_remove_random_points_proba = augmentation_remove_random_points_proba
        self._augmentation_remove_sequence_proba = augmentation_remove_sequence_proba

        # Loss weights
        self._prior_loss_weight = prior_loss_weight
        self._posterior_loss_weight = posterior_loss_weight

        self._loss_func = factory_loss_function(train_config.loss_name, train_config.loss_params) \
            if train_config is not None else None
        if train_config is not None:
            assert 'gaussian_nllloss' in train_config.loss_name, \
                'Failed to find "gaussian_nllloss" in loss function name!'
        if transform_func is not None:
            assert isinstance(transform_func, InvertibleTransformWithVariance), \
                f'Expected transform function to be of type "InvertibleTransformWithStd" ' \
                f'but got "{type(transform_func)}"'
        self._transform_func = transform_func
        self._log_epoch_metrics = log_epoch_metrics

    @property
    def core(self) -> FilterModule:
        """
        Get core model (without training module).
        Returns:
            Core model
        """
        return self._model

    def forward(self, x_obs: torch.Tensor, t_obs: torch.Tensor, x_unobs: torch.Tensor, t_unobs: torch.Tensor,
                mask: Union[bool, List[bool]] = True, *args, **kwargs) \
            -> Dict[str, torch.Tensor]:
        return self._model(x_obs, t_obs, x_unobs, t_unobs, mask=mask, *args, **kwargs)

    def inference(self, x_obs: torch.Tensor, t_obs: torch.Tensor, x_unobs: torch.Tensor, t_unobs: torch.Tensor,
                  mask: Union[bool, List[bool]] = True, *args, **kwargs) \
            -> Dict[str, torch.Tensor]:
        """
        Inference (alias for forward)

        Args:
            x_obs: Observed data
            t_obs: Observed time points
            x_unobs: Unobserved data
            t_unobs: Unobserved time points
            mask: Mask unobserved

        Returns:
            Prior and posterior estimation for future trajectory
        """
        return self._model(x_obs, t_obs, x_unobs, t_unobs, mask=mask, *args, **kwargs)

    def _calc_loss_and_metrics(
        self,
        orig_bboxes_obs: torch.Tensor,
        orig_bboxes_unobs_prior: torch.Tensor,
        orig_bboxes_unobs_posterior: torch.Tensor,
        transformed_bboxes_unobs_prior: torch.Tensor,
        transformed_bboxes_unobs_posterior: torch.Tensor,
        bboxes_unobs_prior_mean: torch.Tensor,
        bboxes_unobs_prior_log_var: torch.Tensor,
        bboxes_unobs_posterior_mean: torch.Tensor,
        bboxes_unobs_posterior_log_var: torch.Tensor,
        metadata: dict
    ) -> Tuple[Union[torch.Tensor, Dict[str, torch.Tensor]], Optional[Dict[str, float]]]:
        bboxes_unobs_prior_var = self._model.postprocess_log_var(bboxes_unobs_prior_log_var)
        bboxes_unobs_posterior_var = self._model.postprocess_log_var(bboxes_unobs_posterior_log_var)

        prior_loss = self._loss_func(bboxes_unobs_prior_mean, transformed_bboxes_unobs_prior, bboxes_unobs_prior_var)
        posterior_loss = self._loss_func(bboxes_unobs_posterior_mean, transformed_bboxes_unobs_posterior, bboxes_unobs_posterior_var)
        loss = {
            'prior_loss': prior_loss,
            'posterior_loss': posterior_loss,
            'loss': self._prior_loss_weight * prior_loss + self._posterior_loss_weight * posterior_loss
        }

        if self._transform_func is not None:
            # Invert mean
            _, bboxes_unobs_prior_mean, *_ = self._transform_func.inverse([orig_bboxes_obs, bboxes_unobs_prior_mean, metadata, None], shallow=False)
            _, bboxes_unobs_posterior_mean, *_ = self._transform_func.inverse([orig_bboxes_obs, bboxes_unobs_posterior_mean, metadata, None],
                                                                              shallow=False)

        if not self._log_epoch_metrics:
            return loss, None

        gt_traj = orig_bboxes_unobs_prior.detach().cpu().numpy()
        prior_traj = bboxes_unobs_prior_mean.detach().cpu().numpy()
        prior_metrics = metrics_func(gt_traj, prior_traj)
        prior_metrics = {f'prior_{name}': value for name, value in prior_metrics.items()}

        gt_traj = orig_bboxes_unobs_posterior.detach().cpu().numpy()
        posterior_traj = bboxes_unobs_posterior_mean.detach().cpu().numpy()
        posterior_metrics = metrics_func(gt_traj, posterior_traj) if self._log_epoch_metrics else None
        posterior_metrics = {f'posterior_{name}': value for name, value in posterior_metrics.items()}
        metrics = dict(list(prior_metrics.items()) + list(posterior_metrics.items()))

        return loss, metrics

    def training_step(self, batch: Dict[str, Union[dict, torch.Tensor]], *args, **kwargs) -> torch.Tensor:
        bboxes_obs, bboxes_aug_unobs, ts_obs, ts_unobs, orig_bboxes_obs, orig_bboxes_unobs, bboxes_unobs, metadata = batch.values()

        bboxes_unobs_posterior = bboxes_unobs
        orig_bboxes_unobs_posterior = orig_bboxes_unobs
        mask = [True for _ in range(ts_unobs.shape[0])]
        if self._augmentation_remove_points_enable:
            with torch.no_grad():
                assert bboxes_aug_unobs.shape[0] >= 3, 'Minimum length of trajectory is 3 in order to perform special augmentations!'

                r = random.random()
                if r < self._augmentation_remove_random_points_proba:
                    (bboxes_aug_unobs,), removed_indices, kept_indices = remove_points([bboxes_aug_unobs], min_length=1)
                    for i in removed_indices:
                        mask[i] = False
                    bboxes_unobs_posterior = bboxes_unobs_posterior[kept_indices, :, :]
                    orig_bboxes_unobs_posterior = orig_bboxes_unobs_posterior[kept_indices, :, :]

                elif r < self._augmentation_remove_random_points_proba + self._augmentation_remove_sequence_proba:
                    # Remove random sequence (connected points)
                    n = bboxes_aug_unobs.shape[0]
                    start = random.randint(1, n - 1)  # s ~ U[1, n-1]
                    end = random.randint(start, n)  # e ~ U[s, n]
                    bboxes_aug_unobs = torch.cat([bboxes_aug_unobs[:start, :, :], bboxes_aug_unobs[end:n, :, :]], dim=0)
                    for i in range(start, end):
                        mask[i] = False
                    bboxes_unobs_posterior = torch.cat([bboxes_unobs_posterior[:start, :, :], bboxes_unobs_posterior[end:n, :, :]], dim=0)
                    orig_bboxes_unobs_posterior = \
                        torch.cat([orig_bboxes_unobs_posterior[:start, :, :], orig_bboxes_unobs_posterior[end:n, :, :]], dim=0)

        outputs = self.forward(bboxes_obs, ts_obs, bboxes_aug_unobs, ts_unobs, mask=mask)

        # noinspection PyTypeChecker
        loss, metrics = self._calc_loss_and_metrics(
            orig_bboxes_obs=orig_bboxes_obs,
            orig_bboxes_unobs_prior=orig_bboxes_unobs,
            orig_bboxes_unobs_posterior=orig_bboxes_unobs_posterior,
            transformed_bboxes_unobs_prior=bboxes_unobs,
            transformed_bboxes_unobs_posterior=bboxes_unobs_posterior,
            bboxes_unobs_prior_mean=outputs['prior_mean'],
            bboxes_unobs_prior_log_var=outputs['prior_logvar'],
            bboxes_unobs_posterior_mean=outputs['posterior_mean'],
            bboxes_unobs_posterior_log_var=outputs['posterior_logvar'],
            metadata=metadata
        )
        self._log_loss(loss, prefix='training', log_step=True)
        self._log_metrics(metrics, prefix='training')
        self._log_lr()

        return loss

    def validation_step(self, batch: Dict[str, Union[dict, torch.Tensor]], *args, **kwargs) -> torch.Tensor:
        bboxes_obs, bboxes_aug_unobs, ts_obs, ts_unobs, orig_bboxes_obs, orig_bboxes_unobs, bboxes_unobs, metadata = batch.values()
        outputs_posterior = self.forward(bboxes_obs, ts_obs, bboxes_aug_unobs, ts_unobs)
        outputs_prior = self.forward(bboxes_obs, ts_obs, bboxes_aug_unobs, ts_unobs, mask=False)

        # noinspection PyTypeChecker
        loss, metrics = self._calc_loss_and_metrics(
            orig_bboxes_obs=orig_bboxes_obs,
            orig_bboxes_unobs_prior=orig_bboxes_unobs,
            orig_bboxes_unobs_posterior=orig_bboxes_unobs,
            transformed_bboxes_unobs_prior=bboxes_unobs,
            transformed_bboxes_unobs_posterior=bboxes_unobs,
            bboxes_unobs_prior_mean=outputs_prior['prior_mean'],
            bboxes_unobs_prior_log_var=outputs_prior['prior_logvar'],
            bboxes_unobs_posterior_mean=outputs_posterior['posterior_mean'],
            bboxes_unobs_posterior_log_var=outputs_posterior['posterior_logvar'],
            metadata=metadata
        )
        self._log_loss(loss, prefix='val', log_step=False)
        self._log_metrics(metrics, prefix='val')

        return loss
