from harmonix.core.harmony import HarmonyParseError, analyze_progression, parse_chord, parse_progression
from harmonix.core.progression_presets import build_progression_catalog, build_progression_from_pattern, build_song_example_catalog


def test_parse_chord_handles_extensions_and_alterations() -> None:
    chord = parse_chord("A7b9")
    assert chord.root == "A"
    assert chord.quality == "dom"
    assert chord.extension == 7
    assert chord.alterations == ["b9"]


def test_parse_progression_reports_invalid_token_position() -> None:
    try:
        parse_progression("Dm7 H#dim Cmaj7")
    except HarmonyParseError as exc:
        assert "poziciji 2" in str(exc)
        assert "H#dim" in str(exc)
    else:
        raise AssertionError("Expected HarmonyParseError for invalid chord token")


def test_analyze_progression_returns_labels_and_tension() -> None:
    sequence = parse_progression("Dm7 G7 Cmaj7")
    analysis = analyze_progression(sequence)
    assert analysis.chord_labels == ["Dm7", "G7", "Cmaj7"]
    assert analysis.roots == ["D", "G", "C"]
    assert 0.0 <= analysis.tension_score <= 1.0


def test_build_progression_from_pattern_transposes_major_ii_v_i() -> None:
    assert build_progression_from_pattern("ii_v_i_major", "C") == "Dm7 G7 Cmaj7"
    assert build_progression_from_pattern("ii_v_i_major", "Eb") == "Fm7 Bb7 Ebmaj7"


def test_build_progression_from_pattern_supports_minor_and_turnaround() -> None:
    assert build_progression_from_pattern("ii_v_i_minor", "A") == "Bm7b5 E7 Am7"
    assert build_progression_from_pattern("turnaround_major", "C") == "Cmaj7 A7 Dm7 G7"


def test_build_progression_from_pattern_supports_common_theory_sequences() -> None:
    assert build_progression_from_pattern("circle_of_fifths", "C") == "Em7 A7 Dm7 G7 Cmaj7"
    assert build_progression_from_pattern("doo_wop", "C") == "Cmaj7 Am7 Fmaj7 G7"
    assert build_progression_from_pattern("andalusian", "A") == "Am7 Gmaj7 Fmaj7 E7"


def test_build_progression_from_pattern_supports_blues_forms() -> None:
    assert build_progression_from_pattern("jazz_blues", "C") == "C7 F7 C7 C7 F7 F7 C7 A7 Dm7 G7 C7 G7"
    assert build_progression_from_pattern("minor_blues", "A") == "Am7 Dm7 Am7 Am7 Dm7 Ebdim7 Am7 F7 Bm7b5 E7 Am7 E7"


def test_build_progression_catalog_groups_patterns_by_category() -> None:
    catalog = build_progression_catalog()

    assert catalog[0][0] == "Jazz Cadences"
    assert any(entry[1] == "ii-V-I" for entry in catalog[0][1])
    assert any(category == "Blues Forms" for category, _entries in catalog)


def test_build_song_example_catalog_groups_examples_and_preserves_metadata() -> None:
    catalog = build_song_example_catalog()

    assert any(category == "Jazz Cadences" for category, _entries in catalog)
    jazz_entries = dict(catalog)["Jazz Cadences"]
    autumn_leaves = next(entry for entry in dict(catalog)["Turnarounds & Standards"] if entry[0] == "Autumn Leaves")
    assert any(entry[0] == "There Will Never Be Another You" for entry in jazz_entries)
    assert autumn_leaves[2] == "Circle of fifths"
    assert "ii-V" in autumn_leaves[4]
