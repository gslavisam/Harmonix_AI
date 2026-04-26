from __future__ import annotations

from .harmony import note_to_pitch_class


MODES = {
    "ionian": (0, 2, 4, 5, 7, 9, 11),
    "dorian": (0, 2, 3, 5, 7, 9, 10),
    "mixolydian": (0, 2, 4, 5, 7, 9, 10),
}


def build_scale(root: str, mode: str = "ionian") -> list[int]:
    root_pc = note_to_pitch_class(root)
    intervals = MODES[mode]
    return [((root_pc + interval) % 12) for interval in intervals]