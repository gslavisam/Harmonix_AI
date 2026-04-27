from harmonix.ai.lmstudio import LMStudioClient


def test_coerce_progression_candidate_normalizes_llm_output() -> None:
    client = LMStudioClient()

    progression = client._coerce_progression_candidate("; Em - B7 - Em - B7 - Em - B7 - Em - B7")

    assert progression == "Em B7 Em B7 Em B7 Em B7"


def test_extract_document_progression_prefers_cleaned_progression_field() -> None:
    client = LMStudioClient()

    progression = client._extract_document_progression(
        {
            "progression": "; Em - B7 - Em - B7",
            "source_excerpt": "Verse: Em - B7 - Em - B7",
        }
    )

    assert progression == "Em B7 Em B7"