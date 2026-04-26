from __future__ import annotations

import os
import re
from pathlib import Path


SUPPORTED_NOTATION_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".webp"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def detect_notation_file_kind(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        return "pdf"
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    return "unsupported"


def validate_notation_upload(filename: str, file_bytes: bytes, max_mb: int = 15) -> str | None:
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_NOTATION_EXTENSIONS:
        return "Podržani su PDF i slike (.png, .jpg, .jpeg, .webp)."
    if len(file_bytes) > max_mb * 1024 * 1024:
        return f"Fajl prelazi maksimalnih {max_mb} MB."
    return None


def render_pdf_pages_to_png(file_bytes: bytes, max_pages: int = 3) -> list[bytes]:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF nije dostupan za renderovanje PDF notacije.") from exc

    document = fitz.open(stream=file_bytes, filetype="pdf")
    rendered_pages: list[bytes] = []
    for page_index in range(min(len(document), max_pages)):
        page = document.load_page(page_index)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        rendered_pages.append(pixmap.tobytes("png"))
    document.close()
    return rendered_pages


def normalize_progression_text(raw_text: str) -> str:
    text = raw_text.replace("\n", " ")
    text = text.replace("|", " ")
    text = text.replace(":", " ")
    text = text.replace(";", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def default_notation_title(filename: str) -> str:
    stem = Path(filename).stem.replace("_", " ").replace("-", " ").strip()
    return stem.title() if stem else "Uploaded notation"


def store_uploaded_notation(file_bytes: bytes, filename: str) -> str:
    upload_dir = Path(os.getenv("UPLOAD_DIR", "uploads")) / "notation"
    upload_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(filename).name
    output_path = upload_dir / safe_name
    output_path.write_bytes(file_bytes)
    return str(output_path)