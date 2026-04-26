from __future__ import annotations

from dataclasses import dataclass


DJANGO_SYSTEM_PROMPT = (
    "Ti si Django, iskusni Gypsy jazz muzičar i teoretičar harmonije sa preko 40 godina "
    "iskustva. Objašnjavaj jasno, toplo i kroz sokratska pitanja. Uvek vrati JSON sa poljima "
    "analysis, suggestions, socratic_questions, socratic_guides, next_steps i tension_score."
)


@dataclass(slots=True)
class SunoPrompt:
    genre: str = "Gypsy Jazz"
    tempo: int = 120
    key: str = "Am"
    mood: str = "melancholic"

    TEMPLATES = {
        "gypsy": "[Gypsy Jazz] {tempo}bpm, acoustic guitar, violin, Django style, {mood}, {key}",
        "bebop": "[Bebop] {tempo}bpm, walking bass, {changes}, improvisation, {mood}",
        "ballad": "[Jazz Ballad] {tempo}bpm, piano trio, {key}, romantic, {mood}",
        "latin": "[Latin Jazz] {tempo}bpm, bossa nova, {key}, {mood}",
    }

    def generate(self, chord_changes: str | None = None) -> str:
        template_key = self.genre.lower().split()[0]
        template = self.TEMPLATES.get(template_key, self.TEMPLATES["gypsy"])
        return template.format(
            tempo=self.tempo,
            key=self.key,
            mood=self.mood,
            changes=chord_changes or "ii-V-I",
        )

    @classmethod
    def from_analysis(cls, analysis: dict) -> "SunoPrompt":
        return cls(
            genre=analysis.get("style", "Gypsy Jazz"),
            tempo=int(analysis.get("suggested_tempo", 120)),
            key=analysis.get("key", "Am"),
            mood=analysis.get("mood", "melancholic"),
        )