from __future__ import annotations

from pathlib import Path

from .bass import BassNote


def export_midi(bass_notes: list[BassNote], tempo: int, output_path: str | Path) -> Path:
    try:
        from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
    except ImportError as exc:
        raise RuntimeError("mido nije instaliran; MIDI eksport nije dostupan.") from exc

    midi_file = MidiFile()
    track = MidiTrack()
    midi_file.tracks.append(track)

    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(tempo), time=0))
    track.append(
        MetaMessage(
            "time_signature",
            numerator=4,
            denominator=4,
            clocks_per_click=24,
            notated_32nd_notes_per_beat=8,
            time=0,
        )
    )

    ticks_per_beat = midi_file.ticks_per_beat
    for note in bass_notes:
        duration_ticks = int(note.duration * ticks_per_beat)
        track.append(Message("note_on", note=note.pitch, velocity=note.velocity, time=0))
        track.append(Message("note_off", note=note.pitch, velocity=0, time=duration_ticks))

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    midi_file.save(output)
    return output