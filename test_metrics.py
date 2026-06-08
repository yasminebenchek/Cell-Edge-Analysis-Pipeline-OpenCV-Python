import numpy as np

from cell_edge_analysis.metrics import mean_squared_error, segmentation_scores


def test_mean_squared_error_identical_images_is_zero():
    image = np.array([[0, 255], [255, 0]], dtype=np.uint8)
    assert mean_squared_error(image, image) == 0.0


def test_segmentation_scores_perfect_overlap():
    image = np.array([[0, 255], [255, 0]], dtype=np.uint8)
    scores = segmentation_scores(image, image)
    assert scores["precision"] == 1.0
    assert scores["recall"] == 1.0
    assert scores["f1_score"] == 1.0
