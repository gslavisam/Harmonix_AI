from pathlib import Path

from harmonix.core.bass import build_bass_bar_overview, generate_walking_bass
from harmonix.core.harmony import note_to_pitch_class, parse_progression
from harmonix.core.midi import export_midi


def test_generate_walking_bass_emits_four_notes_per_bar() -> None:
    sequence = parse_progression("Dm7 G7 Cmaj7")
    notes = generate_walking_bass(sequence, tempo=120)
    assert len(notes) == 12
    assert [note.beat_position for note in notes[:4]] == [1, 2, 3, 4]


def test_generate_walking_bass_uses_root_on_beat_one() -> None:
    sequence = parse_progression("Dm7 G7")
    notes = generate_walking_bass(sequence, tempo=120)
    first_note = notes[0]
    assert first_note.pitch % 12 == note_to_pitch_class("D")
    assert first_note.role == "root"
    assert first_note.chord_label == "Dm7"


def test_generate_walking_bass_approaches_next_root_on_beat_four() -> None:
    sequence = parse_progression("Dm7 G7")
    notes = generate_walking_bass(sequence, tempo=120)
    beat_four = notes[3]
    next_root_pc = note_to_pitch_class("G")
    assert abs((beat_four.pitch % 12) - next_root_pc) in {1, 11}


def test_export_midi_writes_file(tmp_path: Path) -> None:
    sequence = parse_progression("Dm7 G7")
    notes = generate_walking_bass(sequence, tempo=120)
    output = export_midi(notes, 120, tmp_path / "bass.mid")
    assert output.exists()
    assert output.suffix == ".mid"


def test_build_bass_bar_overview_groups_notes_by_bar() -> None:
    sequence = parse_progression("Dm7 G7")
    notes = generate_walking_bass(sequence, tempo=120)

    overview = build_bass_bar_overview(notes)

    assert len(overview) == 2
    assert overview[0]["bar_title"] == "Takt 1"
    assert overview[0]["chord_label"] == "Dm7"
    assert "motion" in overview[0]["bar_comment"]
    assert overview[0]["beat_one_note"] == "D2"
    assert overview[0]["beat_one_role"] == "root"
    assert overview[0]["beat_one_color"] == "green"
    assert overview[0]["beat_four_role"] == "approach"
    assert overview[0]["beat_four_color"] == "red"