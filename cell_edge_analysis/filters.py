from __future__ import annotations

import cv2
import numpy as np

from .preprocess import normalize_uint8, otsu_threshold


def sobel_edges(image: np.ndarray, kernel_size: int = 3, binary: bool = True) -> np.ndarray:
    """Detect edges using the Sobel gradient operator."""
    gx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=kernel_size)
    gy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=kernel_size)
    magnitude = cv2.magnitude(gx, gy)
    edges = normalize_uint8(magnitude)
    return otsu_threshold(edges) if binary else edges


def scharr_edges(image: np.ndarray, binary: bool = True) -> np.ndarray:
    """Detect edges using the Scharr operator."""
    gx = cv2.Scharr(image, cv2.CV_64F, 1, 0)
    gy = cv2.Scharr(image, cv2.CV_64F, 0, 1)
    magnitude = cv2.magnitude(gx, gy)
    edges = normalize_uint8(magnitude)
    return otsu_threshold(edges) if binary else edges


def prewitt_edges(image: np.ndarray, binary: bool = True) -> np.ndarray:
    """Detect edges using a Prewitt kernel implemented with filter2D."""
    kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
    gx = cv2.filter2D(image, cv2.CV_32F, kernel_x)
    gy = cv2.filter2D(image, cv2.CV_32F, kernel_y)
    magnitude = cv2.magnitude(gx, gy)
    edges = normalize_uint8(magnitude)
    return otsu_threshold(edges) if binary else edges


def roberts_edges(image: np.ndarray, binary: bool = True) -> np.ndarray:
    """Detect edges using the Roberts cross operator."""
    kernel_x = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernel_y = np.array([[0, 1], [-1, 0]], dtype=np.float32)
    gx = cv2.filter2D(image, cv2.CV_32F, kernel_x)
    gy = cv2.filter2D(image, cv2.CV_32F, kernel_y)
    magnitude = cv2.magnitude(gx, gy)
    edges = normalize_uint8(magnitude)
    return otsu_threshold(edges) if binary else edges


def laplacian_edges(image: np.ndarray, binary: bool = True) -> np.ndarray:
    """Detect edges using a Laplacian operator."""
    lap = cv2.Laplacian(image, cv2.CV_64F)
    edges = normalize_uint8(np.abs(lap))
    return otsu_threshold(edges) if binary else edges


def canny_edges(image: np.ndarray, low_threshold: int = 50, high_threshold: int = 150) -> np.ndarray:
    """Detect edges using the Canny detector."""
    return cv2.Canny(normalize_uint8(image), low_threshold, high_threshold)


EDGE_METHODS = {
    "sobel": sobel_edges,
    "scharr": scharr_edges,
    "prewitt": prewitt_edges,
    "roberts": roberts_edges,
    "laplacian": laplacian_edges,
    "canny": canny_edges,
}
