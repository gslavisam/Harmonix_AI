from __future__ import annotations

from dataclasses import dataclass

from .harmony import ChordSequence, note_to_pitch_class, semitone_to_note


MAJOR_SCALE_INTERVALS = (0, 2, 4, 5, 7, 9, 11)


@dataclass(slots=True)
class BassNote:
    pitch: int
    duration: float
    velocity: int
    beat_position: int
    role: str = ""
    chord_label: str = ""
    bar_number: int = 0


def generate_walking_bass(
    sequence: ChordSequence,
    tempo: int = 120,
    start_octave: int = 2,
) -> list[BassNote]:
    notes: list[BassNote] = []
    previous_pitch: int | None = None

    for index, chord in enumerate(sequence.chords):
        next_chord = sequence.chords[index + 1] if index + 1 < len(sequence.chords) else None
        beat_events = [
            (root_pitch(chord.root, start_octave), "root"),
            third_or_fifth_pitch(chord, previous_pitch),
            passing_pitch(chord, previous_pitch),
            (approach_pitch(chord.root, next_chord.root if next_chord else None, previous_pitch, start_octave), "approach"),
        ]

        for beat, (pitch, role) in enumerate(beat_events, start=1):
            if previous_pitch is not None and abs(pitch - previous_pitch) > 12:
                pitch = closest_pitch_class(pitch % 12, previous_pitch)

            note = BassNote(
                pitch=pitch,
                duration=1.0,
                velocity=88 if beat in (1, 3) else 76,
                beat_position=beat,
                role=role,
                chord_label=chord.label,
                bar_number=index + 1,
            )
            notes.append(note)
            previous_pitch = note.pitch

    return notes


def bass_preview(notes: list[BassNote]) -> list[str]:
    return [f"B{note.beat_position}:{midi_to_name(note.pitch)}" for note in notes]


def build_bass_bar_overview(notes: list[BassNote]) -> list[dict[str, str]]:
    if not notes:
        return []
    bars: list[dict[str, str]] = []
    for start in range(0, len(notes), 4):
        bar_notes = notes[start : start + 4]
        bar = {
            "bar_title": f"Takt {bar_notes[0].bar_number}",
            "chord_label": bar_notes[0].chord_label,
            "bar_comment": build_bar_commentary(bar_notes),
            "beat_one_note": "-",
            "beat_one_role": "",
            "beat_one_color": "gray",
            "beat_two_note": "-",
            "beat_two_role": "",
            "beat_two_color": "gray",
            "beat_three_note": "-",
            "beat_three_role": "",
            "beat_three_color": "gray",
            "beat_four_note": "-",
            "beat_four_role": "",
            "beat_four_color": "gray",
        }
        for note in bar_notes:
            if note.beat_position == 1:
                bar["beat_one_note"] = midi_to_name(note.pitch)
                bar["beat_one_role"] = note.role
                bar["beat_one_color"] = color_for_role(note.role)
            elif note.beat_position == 2:
                bar["beat_two_note"] = midi_to_name(note.pitch)
                bar["beat_two_role"] = note.role
                bar["beat_two_color"] = color_for_role(note.role)
            elif note.beat_position == 3:
                bar["beat_three_note"] = midi_to_name(note.pitch)
                bar["beat_three_role"] = note.role
                bar["beat_three_color"] = color_for_role(note.role)
            elif note.beat_position == 4:
                bar["beat_four_note"] = midi_to_name(note.pitch)
                bar["beat_four_role"] = note.role
                bar["beat_four_color"] = color_for_role(note.role)
        bars.append(bar)
    return bars


def root_pitch(root: str, octave: int) -> int:
    return 12 * (octave + 1) + note_to_pitch_class(root)


def third_or_fifth_pitch(chord, previous_pitch: int | None) -> tuple[int, str]:
    chord_tones = chord.chord_tones()
    target_pc = chord_tones[1] if len(chord_tones) > 1 else chord_tones[0]
    anchor = previous_pitch if previous_pitch is not None else root_pitch(chord.root, 2)
    return closest_pitch_class(target_pc, anchor), describe_role_for_pitch_class(chord, target_pc)


def passing_pitch(chord, previous_pitch: int | None) -> tuple[int, str]:
    root_pc = note_to_pitch_class(chord.root)
    scale = {((root_pc + interval) % 12) for interval in MAJOR_SCALE_INTERVALS}
    chord_tones = chord.chord_tones()
    for pitch_class in chord_tones[1:]:
        if pitch_class in scale:
            anchor = previous_pitch if previous_pitch is not None else root_pitch(chord.root, 2)
            return closest_pitch_class(pitch_class, anchor), describe_role_for_pitch_class(chord, pitch_class)
    anchor = previous_pitch if previous_pitch is not None else root_pitch(chord.root, 2)
    return closest_pitch_class((root_pc + 2) % 12, anchor), "passing"


def approach_pitch(root: str, next_root: str | None, previous_pitch: int | None, octave: int) -> int:
    target_root = next_root or root
    target_pitch = root_pitch(target_root, octave)
    anchor = previous_pitch if previous_pitch is not None else root_pitch(root, octave)
    candidates = [target_pitch - 1, target_pitch + 1]
    return min(candidates, key=lambda candidate: abs(candidate - anchor))


def closest_pitch_class(target_pc: int, anchor_pitch: int) -> int:
    candidates = [target_pc + (12 * octave) for octave in range(1, 7)]
    return min(candidates, key=lambda pitch: (abs(pitch - anchor_pitch), pitch))


def describe_role_for_pitch_class(chord, pitch_class: int) -> str:
    chord_tones = chord.chord_tones()
    for index, tone in enumerate(chord_tones):
        if tone == pitch_class:
            if index == 0:
                return "root"
            if index == 1:
                return "3rd"
            if index == 2:
                return "5th"
            if index == 3:
                return "7th"
    return "passing"


def color_for_role(role: str) -> str:
    if role == "root":
        return "green"
    if role == "3rd":
        return "blue"
    if role == "5th":
        return "bronze"
    if role == "7th":
        return "indigo"
    if role == "approach":
        return "red"
    if role == "passing":
        return "orange"
    return "gray"


def build_bar_commentary(notes: list[BassNote]) -> str:
    if not notes:
        return ""

    intervals = [abs(notes[index + 1].pitch - notes[index].pitch) for index in range(len(notes) - 1)]
    if intervals and max(intervals) <= 2:
        motion_text = "stepwise motion"
    elif any(interval == 1 for interval in intervals):
        motion_text = "chromatic motion"
    else:
        motion_text = "mixed motion"

    guide_tone_roles = {note.role for note in notes[1:3] if note.role in {"3rd", "7th"}}
    if guide_tone_roles:
        guide_text = "guide tone emphasis"
    elif any(note.role == "5th" for note in notes[1:3]):
        guide_text = "stable chord-tone support"
    else:
        guide_text = "passing color"

    if notes[-1].role == "approach":
        arrival_text = "chromatic approach into next chord"
    else:
        arrival_text = "settles inside current harmony"

    return f"{guide_text}, {motion_text}, {arrival_text}."


def midi_to_name(midi_note: int) -> str:
    note_name = semitone_to_note(midi_note % 12)
    octave = (midi_note // 12) - 1
    return f"{note_name}{octave}"