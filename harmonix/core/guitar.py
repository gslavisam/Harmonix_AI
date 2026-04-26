from __future__ import annotations

from dataclasses import dataclass

from .bass import BassNote, midi_to_name
from .harmony import Chord, ChordSequence, note_to_pitch_class, semitone_to_note


STANDARD_TUNING = ("E", "A", "D", "G", "B", "e")
DISPLAY_STRING_ORDER = ("e", "B", "G", "D", "A", "E")
OPEN_STRING_MIDI = {
    "E": 40,
    "A": 45,
    "D": 50,
    "G": 55,
    "B": 59,
    "e": 64,
}
VOICING_INTERVALS = {
    "maj": (0, 7, 11, 4),
    "min": (0, 7, 10, 3),
    "dom": (0, 7, 10, 4),
    "half-dim": (0, 6, 10, 3),
    "dim": (0, 6, 9, 3),
    "aug": (0, 8, 11, 4),
}


@dataclass(slots=True)
class GuitarVoicing:
    chord_label: str
    strings: tuple[str, ...]
    frets: tuple[int, ...]
    shape: str
    note_names: tuple[str, ...]


def get_voicing(chord: Chord, strings: tuple[str, ...] = ("D", "G", "B", "e")) -> GuitarVoicing:
    selected_strings = strings if strings != ("D", "G", "B", "e") else _choose_string_set(chord)
    shape = "Jazz Shell"
    target_pitch_classes = _target_pitch_classes(chord, len(selected_strings))
    lowest_string = selected_strings[0]
    root_pitch_class = note_to_pitch_class(chord.root)
    root_fret = _choose_root_fret(lowest_string, root_pitch_class)
    frets = [root_fret]
    note_names = [semitone_to_note(root_pitch_class)]

    for string_name, target_pitch_class in zip(selected_strings[1:], target_pitch_classes[1:]):
        fret = _choose_fret(string_name, target_pitch_class, preferred_fret=root_fret)
        frets.append(fret)
        note_names.append(semitone_to_note(target_pitch_class))

    return GuitarVoicing(
        chord_label=chord.label,
        strings=selected_strings,
        frets=tuple(frets),
        shape=shape,
        note_names=tuple(note_names),
    )


def suggest_fingering(voicing: GuitarVoicing) -> dict[str, object]:
    stretch = max(voicing.frets) - min(voicing.frets)
    return {
        "shape": voicing.shape,
        "is_valid": stretch <= 4,
        "stretch": stretch,
    }


def build_progression_voicings(sequence: ChordSequence) -> list[dict[str, object]]:
    voicings: list[dict[str, object]] = []
    for chord in sequence.chords:
        voicing = get_voicing(chord)
        fingering = suggest_fingering(voicing)
        voicings.append(
            {
                "chord": voicing.chord_label,
                "shape": voicing.shape,
                "stretch": fingering["stretch"],
                "is_valid": fingering["is_valid"],
                "fret_range": _format_fret_range(voicing.frets),
                "neck_text": _build_fretboard_text(voicing),
                "strings": _build_string_rows(voicing),
                "fret_headers": _build_fret_headers(voicing.frets),
                "tab_lines": _build_voicing_tab_lines(voicing),
            }
        )
    return voicings


def build_chord_tablature(voicings: list[dict[str, object]]) -> list[str]:
    if not voicings:
        return []

    line_map = {string_name: f"{string_name}|" for string_name in DISPLAY_STRING_ORDER}
    chord_header = "    "
    for voicing in voicings:
        chord_header += f"{str(voicing['chord']):^6}"
        fret_map = {string_name: "x" for string_name in DISPLAY_STRING_ORDER}
        for string_row in voicing["strings"]:
            if string_row["active_fret"] >= 0:
                fret_map[str(string_row["string"])] = str(string_row["active_fret"])
        for string_name in DISPLAY_STRING_ORDER:
            token = fret_map[string_name]
            line_map[string_name] += f"-{token:>2}-"

    return [chord_header, *[line_map[string_name] for string_name in DISPLAY_STRING_ORDER]]


def build_notation_display(notes: list[BassNote]) -> dict[str, object]:
    if not notes:
        return {"width": "640px", "notes": [], "staff_text": ""}

    min_pitch = min(note.pitch for note in notes)
    max_pitch = max(note.pitch for note in notes)
    pitch_span = max(1, max_pitch - min_pitch)
    rendered_notes: list[dict[str, str]] = []
    for index, note in enumerate(notes):
        left = 32 + (index * 28)
        normalized = (note.pitch - min_pitch) / pitch_span
        top = 98 - int(normalized * 58)
        rendered_notes.append(
            {
                "left": f"{left}px",
                "top": f"{top}px",
                "stem_top": f"{top - 34}px",
                "label": midi_to_name(note.pitch),
                "beat": f"B{note.beat_position}",
            }
        )

    width = max(640, 64 + (len(notes) * 28))
    return {
        "width": f"{width}px",
        "notes": rendered_notes,
        "staff_text": _build_notation_text(notes),
    }


def _choose_string_set(chord: Chord) -> tuple[str, ...]:
    root_pitch_class = note_to_pitch_class(chord.root)
    if root_pitch_class in {0, 1, 2, 3, 4, 5, 6}:
        return ("A", "D", "G", "B")
    return ("E", "A", "D", "G")


def _target_pitch_classes(chord: Chord, count: int) -> tuple[int, ...]:
    root_pitch_class = note_to_pitch_class(chord.root)
    intervals = VOICING_INTERVALS.get(chord.quality, VOICING_INTERVALS["dom"])
    template = [(root_pitch_class + interval) % 12 for interval in intervals]
    while len(template) < count:
        template.append(root_pitch_class)
    return tuple(template[:count])


def _choose_root_fret(string_name: str, root_pitch_class: int) -> int:
    preferred_frets = {
        "E": (3, 5, 6, 8, 10, 1),
        "A": (3, 5, 6, 8, 10, 1),
        "D": (3, 5, 7, 9),
        "G": (2, 4, 5, 7),
        "B": (1, 3, 5, 6),
        "e": (1, 3, 5, 7),
    }
    open_pitch = OPEN_STRING_MIDI[string_name]
    candidates = [
        fret
        for fret in range(0, 13)
        if (open_pitch + fret) % 12 == root_pitch_class
    ]
    preference = preferred_frets.get(string_name, (3, 5, 7))
    return min(candidates, key=lambda fret: (min(abs(fret - target) for target in preference), fret))


def _choose_fret(string_name: str, target_pitch_class: int, preferred_fret: int) -> int:
    open_pitch = OPEN_STRING_MIDI[string_name]
    candidates = [
        fret
        for fret in range(0, 13)
        if (open_pitch + fret) % 12 == target_pitch_class
    ]
    return min(candidates, key=lambda fret: (abs(fret - preferred_fret), fret))


def _format_fret_range(frets: tuple[int, ...]) -> str:
    fret_min = min(frets)
    fret_max = max(frets)
    if fret_min == fret_max:
        return f"Fret {fret_min}"
    return f"Frets {fret_min}-{fret_max}"


def _build_fret_headers(frets: tuple[int, ...]) -> list[str]:
    start_fret = max(0, min(frets) - 1)
    end_fret = max(frets) + 1
    return [str(fret) for fret in range(start_fret, end_fret + 1)]


def _build_string_rows(voicing: GuitarVoicing) -> list[dict[str, object]]:
    headers = _build_fret_headers(voicing.frets)
    segment_frets = [int(header) for header in headers[:-1]]
    active_map = {
        string_name: (fret, note_name)
        for string_name, fret, note_name in zip(voicing.strings, voicing.frets, voicing.note_names)
    }
    rows: list[dict[str, object]] = []
    for string_name in DISPLAY_STRING_ORDER:
        active = active_map.get(string_name)
        cells = []
        for fret in segment_frets:
            is_active = active is not None and active[0] == fret
            cells.append(
                {
                    "label": active[1] if is_active else "",
                    "background": "var(--amber-9)" if is_active else "var(--gray-2)",
                    "color": "white" if is_active else "var(--gray-10)",
                    "border_color": "var(--amber-8)" if is_active else "var(--gray-5)",
                }
            )
        rows.append(
            {
                "string": string_name,
                "active_fret": active[0] if active is not None else -1,
                "note": active[1] if active is not None else "x",
                "cells": cells,
            }
        )
    return rows


def _build_voicing_tab_lines(voicing: GuitarVoicing) -> list[str]:
    active_map = {string_name: fret for string_name, fret in zip(voicing.strings, voicing.frets)}
    lines = []
    for string_name in DISPLAY_STRING_ORDER:
        marker = str(active_map[string_name]) if string_name in active_map else "x"
        lines.append(f"{string_name}|--{marker}--")
    return lines


def _build_fretboard_text(voicing: GuitarVoicing) -> str:
    headers = _build_fret_headers(voicing.frets)
    segment_frets = [int(header) for header in headers[:-1]]
    active_map = {string_name: fret for string_name, fret in zip(voicing.strings, voicing.frets)}
    rows = ["    " + " ".join(f"{fret:^3}" for fret in segment_frets)]
    for string_name in DISPLAY_STRING_ORDER:
        marker_row = []
        active_fret = active_map.get(string_name)
        for fret in segment_frets:
            if active_fret is not None and active_fret == fret:
                marker_row.append(" o ")
            else:
                marker_row.append("---")
        rows.append(f"{string_name:>2} |" + "|".join(marker_row) + "|")
    return "\n".join(rows)


def _build_notation_text(notes: list[BassNote]) -> str:
    if not notes:
        return ""

    width = 4 + (len(notes) * 4)
    rows = [[" " for _ in range(width)] for _ in range(9)]
    for row_index in (0, 2, 4, 6, 8):
        rows[row_index] = ["-" for _ in range(width)]

    min_pitch = min(note.pitch for note in notes)
    max_pitch = max(note.pitch for note in notes)
    pitch_span = max(1, max_pitch - min_pitch)
    note_labels: list[str] = []
    for index, note in enumerate(notes):
        column = 2 + (index * 4)
        normalized = (note.pitch - min_pitch) / pitch_span
        row_index = 8 - int(round(normalized * 8))
        rows[row_index][column] = "o"
        note_labels.append(f"{note.beat_position}:{midi_to_name(note.pitch)}")

    staff_lines = ["".join(row) for row in rows]
    staff_lines.append("")
    staff_lines.append(" ".join(note_labels))
    return "\n".join(staff_lines)