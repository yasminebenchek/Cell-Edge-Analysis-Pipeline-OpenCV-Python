## Project Background

This project is based on my third-year BSc Biochemistry dissertation at the University of Manchester, carried out in Dr. Woolner’s lab. The project focused on applying published computational methods for the automated identification of cellular structural features in optical microscopy images.

The aim was to evaluate whether classical edge detection filters could support cell-boundary detection in confocal microscopy images, particularly for distinguishing individual cell boundaries at the interface between tumour and healthy tissue.

The biological image data came from confocal microscopy of *Xenopus laevis* embryos.

DISCLAIMER: The original confocal microscopy images used are not included in this repository because they were generated as part of academic research and may not be publicly shareable.

This repository instead provides a reproducible implementation of the image-analysis workflow using example images/synthetic sample data. The code can be applied to suitable microscopy images where the user has appropriate permission to analyse and share the data.

## Research Objectives

The main objectives of the project were to:

- evaluate the performance of different edge detection filters for cell-boundary detection
- determine which filter most accurately delineates individual cell boundaries
- compare different z-projection strategies for converting 3D hyperstacks into 2D images
- assess how image preprocessing affects noise reduction and information preservation
- identify a workflow suitable for quantitative analysis of time-lapse confocal microscopy data

## Methods

The image-analysis workflow included:

1. **Z-projection of confocal hyperstacks**  
   Average and median intensity z-projection methods were used to convert 3D image stacks into 2D images. Different z-depths were tested, including 1, 10, 15, and 20 slices.

2. **Image preprocessing**  
   Gaussian smoothing was applied to reduce image noise before feature extraction.

3. **Edge detection and feature extraction**  
   Classical edge detection filters were implemented in Python, including Sobel, Roberts, Prewitt, and Scharr filters.

4. **Post-processing**  
   Normalisation and thresholding were applied to separate foreground regions of interest from the background.

5. **Manual reference annotation**  
   Cell boundaries were manually traced using ImageJ to provide reference outlines for comparison.

6. **Quantitative evaluation**  
   Filter performance was assessed using metrics including PSNR, MSE, positive predictive value, and F1-score.

## Key Findings

The study found that the Sobel filter provided the most accurate and precise edge detection performance for the confocal microscopy images analysed.

Average intensity z-projection performed better than median projection for this dataset, producing clearer outputs for edge detection. Increasing the number of z-slices generally improved PSNR values, suggesting better image quality for downstream edge detection.

Overall, the results suggested that classical edge detection filters can help reduce the impact of noise and support cell-boundary detection in confocal microscopy workflows.

For this GitHub version, the project has been reorganised into a reproducible Python package with modular preprocessing, filtering, metric evaluation, and command-line execution. I am still very interested in image analysis and microscopy-based computational workflows. Any suggestions, feedback, or ideas for improving the project are welcomed. 

## Why this project is relevant

Microscopy image analysis is a common task in bioinformatics and computational biology. This repository demonstrates practical uses of:

- OpenCV-based image preprocessing
- Gaussian noise reduction
- Edge detection using Sobel, Scharr, Prewitt, Roberts, Laplacian, and Canny filters
- Binary thresholding with Otsu's method
- Quantitative comparison of generated edge maps using MSE, precision, recall, F1/Dice, and IoU
- Structuring image-analysis code as a reusable Python package with a command-line interface

## Repository structure

```text
.
├── src/cell_edge_analysis/    # Reusable Python package
├── examples/                  # Example script showing how to run the pipeline
├── tests/                     # Basic unit tests
├── outputs/                   # Generated outputs are ignored by Git
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Architecture

The project is organised around one reusable package rather than scattered scripts:

```text
src/cell_edge_analysis/
├── io.py           # Image loading and saving helpers
├── preprocess.py   # Contrast enhancement, smoothing, and thresholding
├── filters.py      # Edge-detection algorithms
├── metrics.py      # Quantitative comparison metrics
├── pipeline.py     # End-to-end analysis workflow
└── cli.py          # Command-line interface
```

This keeps the repository professional: reusable logic lives in `src/`, small runnable demos live in `examples/`, tests live in `tests/`, and generated files go to `outputs/`.

## Installation

```bash
git clone https://github.com/yasbenchek/cell-edge-analysis.git
cd cell-edge-analysis
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .[dev]
```

Alternatively:

```bash
pip install -r requirements.txt
```

## Quick start

Run the full example pipeline:

```bash
python examples/run_example.py
```

Or use the command-line interface:

```bash
cell-edge-analysis \
  --input data/sample_images/cell_median_z10.tif \
  --reference data/sample_images/reference_prewitt_filter.tif \
  --output outputs/example_run \
  --methods sobel scharr prewitt roberts canny
```

The pipeline writes processed images and edge maps to the output folder. If a reference edge image is provided, it also creates `metrics.csv`.


## Methods included

| Method | Purpose |
|---|---|
| Gaussian smoothing | Reduces noise before edge detection |
| Sobel | Gradient-based edge detection in x/y directions |
| Scharr | Similar to Sobel but more sensitive to gradient changes |
| Prewitt | Simple directional gradient filter |
| Roberts | Small-kernel edge detector useful for sharp transitions |
| Laplacian | Second-derivative edge detection |
| Canny | Multi-stage edge detection algorithm |
| Otsu thresholding | Converts intensity maps into binary edge maps |

## Running tests

```bash
pytest
```

## Future improvements

- Add annotated ground-truth masks for stronger validation
- Add notebooks explaining each filter visually
- Extend the pipeline to support batch processing of full microscopy folders
- Add segmentation metrics against manually labelled cell boundaries
- Add plots comparing each method across multiple images


