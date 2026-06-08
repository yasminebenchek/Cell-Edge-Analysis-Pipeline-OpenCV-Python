from __future__ import annotations

import cv2
import numpy as np


def mean_squared_error(image_a: np.ndarray, image_b: np.ndarray) -> float:
    """Calculate mean squared error between two images."""
    a, b = _align_images(image_a, image_b)
    return float(np.mean((a.astype(np.float32) - b.astype(np.float32)) ** 2))


def segmentation_scores(predicted: np.ndarray, reference: np.ndarray) -> dict[str, float]:
    """Calculate precision, recall, F1, Dice, and IoU for binary edge maps."""
    pred, ref = _align_images(predicted, reference)
    pred_bin = pred > 0
    ref_bin = ref > 0

    tp = np.logical_and(pred_bin, ref_bin).sum()
    fp = np.logical_and(pred_bin, ~ref_bin).sum()
    fn = np.logical_and(~pred_bin, ref_bin).sum()

    precision = _safe_div(tp, tp + fp)
    recall = _safe_div(tp, tp + fn)
    f1 = _safe_div(2 * precision * recall, precision + recall)
    iou = _safe_div(tp, tp + fp + fn)

    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "dice_coefficient": f1,
        "iou": iou,
    }


def _align_images(image_a: np.ndarray, image_b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if image_a.shape == image_b.shape:
        return image_a, image_b
    resized_b = cv2.resize(image_b, (image_a.shape[1], image_a.shape[0]), interpolation=cv2.INTER_NEAREST)
    return image_a, resized_b


def _safe_div(numerator: float, denominator: float) -> float:
    return float(numerator / denominator) if denominator else 0.0
