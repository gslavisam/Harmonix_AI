from harmonix.core.harmony import parse_progression
from harmonix.core.bass import build_bass_bar_overview, generate_walking_bass
from harmonix.core.song_analysis import build_bass_harmonic_summary, build_form_overview, detect_key_cadences, infer_tonal_center


def test_build_form_overview_handles_known_patterns():
    assert build_form_overview("Jazz blues", 12) == "12-bar blues form"
    assert build_form_overview("ii-V-I", 3) == "Cadential cell (3 bars)"


def test_infer_tonal_center_uses_last_chord_quality():
    assert infer_tonal_center(parse_progression("Dm7 G7 Cmaj7")) == "C major"
    assert infer_tonal_center(parse_progression("Bm7b5 E7 Am7")) == "A minor"


def test_detect_key_cadences_finds_common_moves():
    cadences = detect_key_cadences(parse_progression("Dm7 G7 Cmaj7 A7"), "Turnaround")

    assert "ii-V-I ka Cmaj7" in cadences
    assert any("Turnaround:" in item for item in cadences)


def test_build_bass_harmonic_summary_connects_bass_to_progression_function():
    sequence = parse_progression("Dm7 G7 Cmaj7")
    bass_overview = build_bass_bar_overview(generate_walking_bass(sequence, tempo=120))
    summary = build_bass_harmonic_summary(
        bass_overview,
        "C major",
        ["ii-V-I ka Cmaj7"],
        contains_turnaround=False,
    )

    assert "tonalni centar C major" in summary
    assert "guide tone" in summary
    assert "ii-V-I ka Cmaj7" in summary