
from pathlib import Path
from typing import Any

from paddleocr import PaddleOCR


class TextDetector:
    """Detect text and its location in an image using PaddleOCR."""

    def __init__(self, language: str = "en") -> None:
        self.ocr = PaddleOCR(
            lang=language,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )

    def detect(self, image_path: str | Path) -> list[dict[str, Any]]:
        """Return detected text, confidence, and bounding boxes."""

        path = Path(image_path).expanduser()

        if not path.is_file():
            raise FileNotFoundError(f"Image not found: {path}")

        results = self.ocr.predict(str(path))
        detections: list[dict[str, Any]] = []

        for page in results:
            data = page.json
            if callable(data):
                data = data()

            data = data.get("res", data)

            texts = data.get("rec_texts", [])
            scores = data.get("rec_scores", [])
            boxes = data.get("rec_boxes", [])

            for text, score, box in zip(texts, scores, boxes):
                detections.append(
                    {
                        "text": str(text),
                        "confidence": float(score),
                        "box": [int(value) for value in box],
                    }
                )

        return detections
