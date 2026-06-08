from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


def read_image(path: str | Path, grayscale: bool = True) -> np.ndarray:
    """Read an image from disk and fail clearly if OpenCV cannot load it."""
    path = Path(path)
    flag = cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_UNCHANGED
    image = cv2.imread(str(path), flag)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return image


def save_image(path: str | Path, image: np.ndarray) -> None:
    """Save an image, creating the output directory if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ok = cv2.imwrite(str(path), image)
    if not ok:
        raise OSError(f"Could not save image to: {path}")
