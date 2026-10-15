
from pathlib import Path

import pytest
from PIL import Image

from src.text_detector import TextDetector


def test_missing_image_raises_error():
    detector = TextDetector(language="en")

    with pytest.raises(FileNotFoundError, match="Image not found"):
        detector.detect("missing_image_for_nora_test.jpeg")


def test_detect_returns_expected_structure():
    detector = TextDetector(language="en")
    image_path = Path("/home/usman/Downloads/download.jpeg")

    if not image_path.is_file():
        pytest.skip("Sample image not found")

    detections = detector.detect(image_path)

    assert isinstance(detections, list)

    for item in detections:
        assert isinstance(item["text"], str)
        assert isinstance(item["confidence"], float)
        assert len(item["box"]) == 4
        assert all(isinstance(value, int) for value in item["box"])


def test_detector_rejects_missing_file_before_inference():
    detector = TextDetector(language="en")

    with pytest.raises(FileNotFoundError):
        detector.detect("/tmp/nora_image_that_does_not_exist.jpeg")
