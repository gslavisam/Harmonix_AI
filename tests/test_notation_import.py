from harmonix.services.notation_import import detect_notation_file_kind, normalize_progression_text, validate_notation_upload


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