from __future__ import annotations

from pathlib import Path

from .filters import EDGE_METHODS
from .io import read_image, save_image
from .metrics import mean_squared_error, segmentation_scores
from .preprocess import enhance_contrast_brightness, gaussian_smooth


def run_edge_pipeline(
    input_path: str | Path,
    output_dir: str | Path,
    methods: list[str] | None = None,
    reference_path: str | Path | None = None,
    alpha: float = 1.0,
    beta: float = 0,
    gaussian_kernel: int = 5,
    gaussian_sigma: float = 1.0,
) -> dict[str, dict[str, float]]:
    """Run preprocessing and selected edge detectors on a microscopy image."""
    output_dir = Path(output_dir)
    image = read_image(input_path, grayscale=True)
    enhanced = enhance_contrast_brightness(image, alpha=alpha, beta=beta)
    smoothed = gaussian_smooth(enhanced, kernel_size=gaussian_kernel, sigma=gaussian_sigma)

    save_image(output_dir / "01_enhanced.png", enhanced)
    save_image(output_dir / "02_gaussian_smoothed.png", smoothed)

    selected_methods = methods or list(EDGE_METHODS.keys())
    reference = read_image(reference_path, grayscale=True) if reference_path else None
    results: dict[str, dict[str, float]] = {}

    for method in selected_methods:
        if method not in EDGE_METHODS:
            raise ValueError(f"Unknown method '{method}'. Choose from: {', '.join(EDGE_METHODS)}")
        edge_map = EDGE_METHODS[method](smoothed)
        save_image(output_dir / f"edge_{method}.png", edge_map)
        results[method] = {}
        if reference is not None:
            results[method]["mse"] = mean_squared_error(edge_map, reference)
            results[method].update(segmentation_scores(edge_map, reference))

    return results
