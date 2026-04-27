from pathlib import Path
import tempfile

from harmonix.services.notation_import import (
    detect_notation_file_kind,
    normalize_progression_text,
    resolve_notation_upload_dir,
    store_uploaded_notation,
    validate_notation_upload,
)


def test_detect_notation_file_kind_supports_pdf_and_images() -> None:
    assert detect_notation_file_kind("chart.pdf") == "pdf"
    assert detect_notation_file_kind("lead-sheet.png") == "image"
    assert detect_notation_file_kind("notes.webp") == "image"
    assert detect_notation_file_kind("demo.txt") == "unsupported"


def test_validate_notation_upload_rejects_unknown_extension() -> None:
    error = validate_notation_upload("progression.docx", b"test")

    assert error is not None
    assert "Podržani" in error


def test_normalize_progression_text_flattens_chart_delimiters() -> None:
    normalized = normalize_progression_text("| Dm7 | G7 |\nCmaj7 : A7 ;")

    assert normalized == "Dm7 G7 Cmaj7 A7"


def test_normalize_progression_text_strips_llm_separator_noise() -> None:
    normalized = normalize_progression_text("; Em - B7 - Em - B7 ;")

    assert normalized == "Em B7 Em B7"


def test_resolve_notation_upload_dir_defaults_outside_repo_watch_tree(monkeypatch) -> None:
    monkeypatch.delenv("UPLOAD_DIR", raising=False)

    upload_dir = resolve_notation_upload_dir()

    assert upload_dir == Path(tempfile.gettempdir()) / "harmonix_ai_uploads"


def test_resolve_notation_upload_dir_moves_relative_override_outside_repo(monkeypatch) -> None:
    monkeypatch.setenv("UPLOAD_DIR", "uploads")

    upload_dir = resolve_notation_upload_dir()

    assert upload_dir == Path(tempfile.gettempdir()) / "uploads"


def test_store_uploaded_notation_uses_configured_directory(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path))

    stored_path = Path(store_uploaded_notation(b"pdf-bytes", "chart.pdf"))

    assert stored_path == tmp_path / "notation" / "chart.pdf"
    assert stored_path.read_bytes() == b"pdf-bytes"