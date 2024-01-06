"""
Implementation of SOT (single-object-tracking) metrics.
"""
from typing import List, Union, Dict

import numpy as np

ThresholdType = Union[float, List[float], np.ndarray]


def traj_bbox_xywh_to_xyxy(bbox: np.ndarray, eps=1e-9) -> np.ndarray:
    """
    Converts bbox format xywh to xyxy.

    Args:
        bbox: BBox in xywh format.
        eps: minimum width and height

    Returns:
        Bbox in xyxy format
    """
    bbox = bbox.copy()
    bbox[..., 2] = np.maximum(bbox[..., 0] + bbox[..., 2], bbox[..., 0] + eps)
    bbox[..., 3] = np.maximum(bbox[..., 1] + bbox[..., 3], bbox[..., 1] + eps)
    return bbox


def point_to_point_distance(lhs: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    """
    Calculates point to point distance.

    Args:
        lhs: Left hand side point
        rhs: Right hand side point

    Returns:
        Distance (Array)
    """
    return np.sqrt((lhs[..., 0] - rhs[..., 0]) ** 2 + (lhs[..., 1] - rhs[..., 1]) ** 2)


def mse(gt_traj: np.ndarray, pred_traj: np.ndarray) -> float:
    """
    Mean Squared Error.

    Args:
        gt_traj: Ground Truth Trajectory
        pred_traj: Prediction Trajectory

    Returns:
        MSE metric.
    """
    return float(((gt_traj - pred_traj) ** 2).mean())


def iou(bboxes1: np.ndarray, bboxes2: np.ndarray, is_xywh_format: bool = True) -> np.ndarray:
    """
    Calculates iou between each bbox (for each time point and each batch).
    Used as helper function to calculate other IOU based metrics.

    Args:
        bboxes1: lhs bboxes
        bboxes2: rhs bboxes
        is_xywh_format: If true then it is required to be converted to xyxy first

    Returns:
        iou score for each bbox
    """
    if bboxes1.shape != bboxes2.shape:
        raise AttributeError(f'BBoxes do not have the same shape: {bboxes1.shape} != {bboxes2.shape}')

    if bboxes1.size == 0:
        return np.array([], dtype=np.float32)

    if is_xywh_format:
        bboxes1 = traj_bbox_xywh_to_xyxy(bboxes1, eps=0.0)
        bboxes2 = traj_bbox_xywh_to_xyxy(bboxes2, eps=0.0)

    bboxes1_area = (bboxes1[..., 2] - bboxes1[..., 0]) * (bboxes1[..., 3] - bboxes1[..., 1])
    bboxes2_area = (bboxes2[..., 2] - bboxes2[..., 0]) * (bboxes2[..., 3] - bboxes2[..., 1])

    # Calculate the coordinates of the intersection rectangles
    left = np.maximum(bboxes1[..., 0], bboxes2[..., 0])
    up = np.maximum(bboxes1[..., 1], bboxes2[..., 1])
    right = np.minimum(bboxes1[..., 2], bboxes2[..., 2])
    down = np.minimum(bboxes1[..., 3], bboxes2[..., 3])

    # Calculate the area of intersection rectangles
    width = np.maximum(right - left, 0)
    height = np.maximum(down - up, 0)
    intersection_area = width * height

    # Calculate the IoU
    union_area = bboxes1_area + bboxes2_area - intersection_area
    iou_scores = np.divide(intersection_area, union_area, out=np.zeros_like(union_area), where=union_area != 0)

    return iou_scores


def accuracy(gt_traj: np.ndarray, pred_traj: np.ndarray) -> float:
    """
    Calculates average IOU between GT and PRED bbox.

    Args:
        gt_traj: Ground Truth Trajectory
        pred_traj: Prediction Trajectory

    Returns:
        Accuracy metric.
    """
    return iou(gt_traj, pred_traj).mean()


def metrics_func(gt_traj: np.ndarray, pred_traj: np.ndarray) -> Dict[str, float]:
    """
    Calculates Accuracy, Success and NormPrecision. Supports only default metric parameters.

    Args:
        gt_traj: Ground Truth Trajectory
        pred_traj: Prediction Trajectory

    Returns:
        Mappings for each metric
    """
    return {
        'Accuracy': accuracy(gt_traj, pred_traj),
        'MSE': mse(gt_traj, pred_traj)
    }
