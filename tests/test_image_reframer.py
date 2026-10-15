
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from src.image_reframer import reframe_image


class TestImageReframer(unittest.TestCase):
    def test_reframes_image_to_square(self):
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.png"
            output_path = Path(directory) / "output.png"

            Image.new("RGB", (800, 400), "blue").save(input_path)

            result = reframe_image(
                input_path,
                output_path,
                "1:1",
            )

            self.assertTrue(output_path.is_file())
            self.assertEqual(result["width"], 1080)
            self.assertEqual(result["height"], 1080)

            with Image.open(output_path) as output:
                self.assertEqual(output.size, (1080, 1080))

    def test_reframes_image_to_vertical(self):
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.png"
            output_path = Path(directory) / "output.png"

            Image.new("RGB", (800, 400), "red").save(input_path)

            result = reframe_image(
                input_path,
                output_path,
                "9:16",
            )

            self.assertEqual(result["target_ratio"], "9:16")
            self.assertEqual(result["width"], 1080)
            self.assertEqual(result["height"], 1920)

            with Image.open(output_path) as output:
                self.assertEqual(output.size, (1080, 1920))

    def test_missing_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "output.png"

            with self.assertRaises(FileNotFoundError):
                reframe_image(
                    Path(directory) / "missing.png",
                    output_path,
                    "1:1",
                )

    def test_unsupported_ratio_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.png"
            output_path = Path(directory) / "output.png"

            Image.new("RGB", (100, 100), "white").save(input_path)

            with self.assertRaises(ValueError):
                reframe_image(input_path, output_path, "4:3")


if __name__ == "__main__":
    unittest.main()