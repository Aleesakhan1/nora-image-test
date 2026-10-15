
from pathlib import Path
from PIL import Image, UnidentifiedImageError


SUPPORTED_FORMATS = {"JPEG", "PNG", "WEBP"}


def inspect_image(image_path):
    """Inspect an image and return basic metadata."""
    path = Path(image_path)

    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")

    try:
        with Image.open(path) as image:
            image_format = image.format
            width, height = image.size

            if image_format not in SUPPORTED_FORMATS:
                raise ValueError(
                    f"Unsupported image format: {image_format}"
                )

            if width <= 0 or height <= 0:
                raise ValueError("Image dimensions must be positive.")

            return {
                "filename": path.name,
                "format": image_format,
                "width": width,
                "height": height,
                "aspect_ratio": round(width / height, 4),
                "aspect_ratio_label": classify_aspect_ratio(
                    width, height
                ),
            }

    except UnidentifiedImageError as error:
        raise ValueError("The file is not a valid supported image.") from error


def classify_aspect_ratio(width, height):
    """Classify an image by its closest standard target ratio."""
    ratio = width / height

    targets = {
        "1:1": 1 / 1,
        "9:16": 9 / 16,
        "16:9": 16 / 9,
    }

    return min(
        targets,
        key=lambda label: abs(ratio - targets[label]),
    )

def get_target_dimensions(width, height, target_ratio):
    """Calculate the largest target-ratio rectangle inside the image."""
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive.")

    target_ratios = {
        "1:1": (1, 1),
        "9:16": (9, 16),
        "16:9": (16, 9),
    }

    if target_ratio not in target_ratios:
        raise ValueError(f"Unsupported target ratio: {target_ratio}")

    ratio_width, ratio_height = target_ratios[target_ratio]

    if width / height > ratio_width / ratio_height:
        output_width = round(height * ratio_width / ratio_height)
        output_height = height
    else:
        output_width = width
        output_height = round(width * ratio_height / ratio_width)

    return output_width, output_height