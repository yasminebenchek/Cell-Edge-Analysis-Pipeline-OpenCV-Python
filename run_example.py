from pathlib import Path

from cell_edge_analysis.pipeline import run_edge_pipeline

ROOT = Path(__file__).resolve().parents[1]

results = run_edge_pipeline(
    input_path=ROOT / "data" / "sample_images" / "cell_median_z10.tif",
    reference_path=ROOT / "data" / "sample_images" / "reference_prewitt_filter.tif",
    output_dir=ROOT / "outputs" / "example_run",
    methods=["sobel", "scharr", "prewitt", "roberts", "canny"],
    alpha=1.2,
    beta=0,
)

print(results)
