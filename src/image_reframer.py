
from pathlib import Path

from PIL import Image, ImageOps


TARGET_SIZES = {
    "1:1": (1080, 1080),
    "9:16": (1080, 1920),
    "16:9": (1920, 1080),
}


def reframe_image(
    input_path,
    output_path,
    target_ratio,
    background_color=(245, 245, 245),
):
    """Fit the complete source image inside a standard-size canvas."""
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.is_file():
        raise FileNotFoundError(f"Image not found: {input_path}")

    if target_ratio not in TARGET_SIZES:
        raise ValueError(f"Unsupported target ratio: {target_ratio}")

    if input_path.resolve() == output_path.resolve():
        raise ValueError("Input and output paths must be different.")

    canvas_width, canvas_height = TARGET_SIZES[target_ratio]

    with Image.open(input_path) as original:
        original = ImageOps.exif_transpose(original).convert("RGB")

        if original.width <= 0 or original.height <= 0:
            raise ValueError("Image dimensions must be positive.")

        original.thumbnail(
            (canvas_width, canvas_height),
            Image.Resampling.LANCZOS,
        )

        canvas = Image.new(
            "RGB",
            (canvas_width, canvas_height),
            background_color,
        )

        x = (canvas_width - original.width) // 2
        y = (canvas_height - original.height) // 2

        canvas.paste(original, (x, y))

        output_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(output_path, format="PNG")

    return {
        "output_path": str(output_path),
        "width": canvas_width,
        "height": canvas_height,
        "target_ratio": target_ratio,
    }