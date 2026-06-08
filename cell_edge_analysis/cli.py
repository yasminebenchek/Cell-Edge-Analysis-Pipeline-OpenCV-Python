from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .filters import EDGE_METHODS
from .pipeline import run_edge_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run edge detection on microscopy images.")
    parser.add_argument("--input", required=True, help="Path to the input microscopy image.")
    parser.add_argument("--output", default="outputs", help="Directory for generated edge maps.")
    parser.add_argument(
        "--methods",
        nargs="+",
        default=list(EDGE_METHODS.keys()),
        choices=list(EDGE_METHODS.keys()),
        help="Edge detection methods to run.",
    )
    parser.add_argument("--reference", help="Optional binary/reference edge image for metrics.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Contrast multiplier.")
    parser.add_argument("--beta", type=float, default=0.0, help="Brightness offset.")
    parser.add_argument("--gaussian-kernel", type=int, default=5, help="Odd Gaussian kernel size.")
    parser.add_argument("--gaussian-sigma", type=float, default=1.0, help="Gaussian sigma.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_dir = Path(args.output)
    results = run_edge_pipeline(
        input_path=args.input,
        output_dir=output_dir,
        methods=args.methods,
        reference_path=args.reference,
        alpha=args.alpha,
        beta=args.beta,
        gaussian_kernel=args.gaussian_kernel,
        gaussian_sigma=args.gaussian_sigma,
    )

    if args.reference:
        csv_path = output_dir / "metrics.csv"
        with csv_path.open("w", newline="") as f:
            fieldnames = ["method", "mse", "precision", "recall", "f1_score", "dice_coefficient", "iou"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for method, metrics in results.items():
                writer.writerow({"method": method, **metrics})
        print(f"Metrics written to {csv_path}")

    print(f"Edge maps written to {output_dir}")


if __name__ == "__main__":
    main()
