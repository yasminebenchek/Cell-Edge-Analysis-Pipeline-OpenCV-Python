from __future__ import annotations

import cv2
import numpy as np


def normalize_uint8(image: np.ndarray) -> np.ndarray:
    """Normalize any numeric image to 8-bit intensity range."""
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def enhance_contrast_brightness(image: np.ndarray, alpha: float = 1.5, beta: float = 0) -> np.ndarray:
    """Adjust contrast and brightness using OpenCV's convertScaleAbs."""
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def gaussian_smooth(image: np.ndarray, kernel_size: int = 5, sigma: float = 1.0) -> np.ndarray:
    """Apply Gaussian smoothing to reduce microscopy image noise."""
    if kernel_size % 2 == 0:
        raise ValueError("kernel_size must be odd")
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)


def otsu_threshold(image: np.ndarray) -> np.ndarray:
    """Return a binary image using Otsu thresholding."""
    image_u8 = normalize_uint8(image)
    _, binary = cv2.threshold(image_u8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary
