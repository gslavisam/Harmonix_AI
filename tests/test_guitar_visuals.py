from harmonix.core.bass import generate_walking_bass
from harmonix.core.guitar import build_chord_tablature, build_notation_display, build_progression_voicings, get_voicing
from harmonix.core.harmony import parse_progression


def test_get_voicing_returns_playable_jazz_shells_for_basic_ii_v_i():
    sequence = parse_progression("Dm7 G7 Cmaj7")

    grips = [get_voicing(chord) for chord in sequence.chords]

    assert grips[0].strings == ("A", "D", "G", "B")
    assert grips[0].frets == (5, 7, 5, 6)
    assert grips[1].strings == ("E", "A", "D", "G")
    assert grips[1].frets == (3, 5, 3, 4)
    assert grips[2].strings == ("A", "D", "G", "B")
    assert grips[2].frets == (3, 5, 4, 5)


def test_build_progression_voicings_returns_visual_metadata():
    sequence = parse_progression("Dm7 G7 Cmaj7")

    voicings = build_progression_voicings(sequence)

    assert len(voicings) == 3
    assert voicings[0]["chord"] == "Dm7"
    assert voicings[0]["shape"] == "Jazz Shell"
    assert voicings[0]["fret_range"] == "Frets 5-7"
    assert len(voicings[0]["strings"]) == 6
    assert len(voicings[0]["tab_lines"]) == 6

    neck_lines = str(voicings[0]["neck_text"]).splitlines()
    assert neck_lines[0].strip().startswith("4")
    assert any(line.strip() == "A |---| o |---|---|" for line in neck_lines)
    assert any(line.strip() == "B |---|---| o |---|" for line in neck_lines)
    assert any(line.strip() == "D |---|---|---| o |" for line in neck_lines)


def test_build_chord_tablature_creates_six_string_block():
    sequence = parse_progression("Dm7 G7 Cmaj7")
    voicings = build_progression_voicings(sequence)

    tab_lines = build_chord_tablature(voicings)

    assert len(tab_lines) == 7
    assert tab_lines[0].strip().startswith("Dm7")
    assert tab_lines[1].startswith("e|")
    assert tab_lines[-1].startswith("E|")


def test_build_notation_display_matches_bass_note_count():
    sequence = parse_progression("Dm7 G7 Cmaj7")
    bass_notes = generate_walking_bass(sequence)

    notation = build_notation_display(bass_notes)

    assert notation["width"].endswith("px")
    assert len(notation["notes"]) == len(bass_notes)
    assert notation["notes"][0]["label"]