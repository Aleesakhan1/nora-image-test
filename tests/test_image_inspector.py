
import unittest
import tempfile
from pathlib import Path

from PIL import Image

from src.image_inspector import (
    inspect_image,
    classify_aspect_ratio,
    get_target_dimensions,
)


class TestImageInspector(unittest.TestCase):
    def test_inspects_png_image(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.png"
            Image.new("RGB", (1080, 1080)).save(path)

            result = inspect_image(path)

            self.assertEqual(result["format"], "PNG")
            self.assertEqual(result["width"], 1080)
            self.assertEqual(result["height"], 1080)
            self.assertEqual(result["aspect_ratio_label"], "1:1")

    def test_classifies_vertical_image(self):
        self.assertEqual(
            classify_aspect_ratio(1080, 1920),
            "9:16",
        )

    def test_classifies_wide_image(self):
        self.assertEqual(
            classify_aspect_ratio(1920, 1080),
            "16:9",
        )

    def test_missing_image_is_rejected(self):
        with self.assertRaises(FileNotFoundError):
            inspect_image("this_image_does_not_exist.png")

    def test_square_target_dimensions(self):
        self.assertEqual(
            get_target_dimensions(1920, 1080, "1:1"),
            (1080, 1080),
        )

    def test_vertical_target_dimensions(self):
        self.assertEqual(
            get_target_dimensions(1920, 1080, "9:16"),
            (608, 1080),
        )

    def test_unsupported_target_ratio_is_rejected(self):
        with self.assertRaises(ValueError):
            get_target_dimensions(1920, 1080, "4:3")


if __name__ == "__main__":
    unittest.main()