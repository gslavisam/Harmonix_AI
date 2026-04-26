from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Optional


NOTE_TO_SEMITONE = {
    "C": 0,
    "B#": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "Fb": 4,
    "E#": 5,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
    "Cb": 11,
}

QUALITY_INTERVALS = {
    "maj": (0, 4, 7),
    "min": (0, 3, 7),
    "dom": (0, 4, 7),
    "dim": (0, 3, 6),
    "aug": (0, 4, 8),
    "half-dim": (0, 3, 6),
}

CHORD_PATTERN = re.compile(
    r"^(?P<root>[A-G](?:#|b)?)(?P<body>[^/]*)?(?:/(?P<bass>[A-G](?:#|b)?))?$"
)


class HarmonyParseError(ValueError):
    """Raised when a chord token or progression cannot be parsed."""


@dataclass(slots=True)
class Chord:
    root: str
    quality: str
    extension: int | None = None
    alterations: list[str] = field(default_factory=list)
    bass: Optional[str] = None

    @property
    def label(self) -> str:
        quality_map = {
            "maj": "maj",
            "min": "m",
            "dom": "",
            "dim": "dim",
            "aug": "aug",
            "half-dim": "m7b5",
        }
        suffix = quality_map.get(self.quality, self.quality)
        extension = str(self.extension or "")
        alterations = "".join(self.alterations)
        bass = f"/{self.bass}" if self.bass else ""
        return f"{self.root}{suffix}{extension}{alterations}{bass}"

    def chord_tones(self) -> tuple[int, ...]:
        root_pc = note_to_pitch_class(self.root)
        intervals = QUALITY_INTERVALS[self.quality]
        return tuple((root_pc + interval) % 12 for interval in intervals)


@dataclass(slots=True)
class ChordSequence:
    chords: list[Chord]
    time_signature: tuple[int, int] = (4, 4)
    total_bars: int = 0

    def __post_init__(self) -> None:
        if not self.total_bars:
            self.total_bars = len(self.chords)


@dataclass(slots=True)
class ProgressionAnalysis:
    chord_labels: list[str]
    roots: list[str]
    tension_score: float
    contains_turnaround: bool


def note_to_pitch_class(note: str) -> int:
    if note not in NOTE_TO_SEMITONE:
        raise HarmonyParseError(f"Nepoznata nota: {note}")
    return NOTE_TO_SEMITONE[note]


def semitone_to_note(semitone: int) -> str:
    canonical = {
        0: "C",
        1: "Db",
        2: "D",
        3: "Eb",
        4: "E",
        5: "F",
        6: "Gb",
        7: "G",
        8: "Ab",
        9: "A",
        10: "Bb",
        11: "B",
    }
    return canonical[semitone % 12]


def parse_chord(token: str) -> Chord:
    raw = token.strip()
    if not raw:
        raise ValueError(f"Nepoznat akord: {token}")
    match = CHORD_PATTERN.match(raw)
    if not match:
        raise HarmonyParseError(f"Nepoznat akord: {token}")

    root = match.group("root")
    body = (match.group("body") or "").strip()
    bass = match.group("bass")
    quality, extension, alterations = _parse_body(body)
    return Chord(root=root, quality=quality, extension=extension, alterations=alterations, bass=bass)


def parse_progression(progression: str) -> ChordSequence:
    tokens = [token for token in progression.split() if token]
    if not tokens:
        raise HarmonyParseError("Unesite bar jedan akord")

    chords: list[Chord] = []
    for index, token in enumerate(tokens, start=1):
        try:
            chords.append(parse_chord(token))
        except HarmonyParseError as exc:
            raise HarmonyParseError(f"Nepoznat akord na poziciji {index}: {token}") from exc

    return ChordSequence(chords=chords)


def analyze_progression(sequence: ChordSequence) -> ProgressionAnalysis:
    roots = [chord.root for chord in sequence.chords]
    labels = [chord.label for chord in sequence.chords]
    dominant_count = sum(1 for chord in sequence.chords if chord.quality == "dom")
    alterations_count = sum(len(chord.alterations) for chord in sequence.chords)
    tension_score = min(1.0, round((dominant_count * 0.2) + (alterations_count * 0.1), 2))
    contains_turnaround = labels[-3:] == ["Dm7", "G7", "Cmaj7"] if len(labels) >= 3 else False
    return ProgressionAnalysis(
        chord_labels=labels,
        roots=roots,
        tension_score=tension_score,
        contains_turnaround=contains_turnaround,
    )


def tritone_sub(chord: Chord) -> Chord:
    if chord.quality != "dom":
        return chord
    root_pc = (note_to_pitch_class(chord.root) + 6) % 12
    return Chord(root=semitone_to_note(root_pc), quality=chord.quality, extension=chord.extension)


def related_ii(chord: Chord) -> Chord | None:
    if chord.quality != "dom":
        return None
    root_pc = (note_to_pitch_class(chord.root) - 5) % 12
    return Chord(root=semitone_to_note(root_pc), quality="min", extension=7)


def _parse_body(body: str) -> tuple[str, int | None, list[str]]:
    normalized = body.replace("Δ", "maj")
    quality = "dom"
    extension: int | None = None
    alterations = re.findall(r"(?:b|#)\d+", normalized)
    quality_tokens = [
        ("m7b5", "half-dim"),
        ("maj", "maj"),
        ("min", "min"),
        ("dim", "dim"),
        ("aug", "aug"),
        ("m", "min"),
        ("o", "dim"),
        ("+", "aug"),
    ]

    for token, mapped_quality in quality_tokens:
        if token in normalized:
            quality = mapped_quality
            normalized = normalized.replace(token, "", 1)
            break

    ext_match = re.search(r"(6|7|9|11|13)", normalized)
    if ext_match:
        extension = int(ext_match.group(1))

    if quality == "dom" and extension is None and alterations:
        extension = 7

    leftovers = re.sub(r"(?:b|#)\d+", "", normalized)
    leftovers = re.sub(r"(6|7|9|11|13)", "", leftovers).strip()
    if leftovers:
        raise HarmonyParseError(f"Nepodržan kvalitet akorda: {body}")

    return quality, extension, alterations