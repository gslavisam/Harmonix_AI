from __future__ import annotations

from .harmony import ChordSequence, note_to_pitch_class


def build_form_overview(pattern_label: str, chord_count: int) -> str:
    pattern = pattern_label.lower()
    if "blues" in pattern:
        return "12-bar blues form" if chord_count >= 12 else f"Blues-derived excerpt ({chord_count} bars)"
    if "bridge" in pattern:
        return f"Bridge excerpt / dominant cycle ({chord_count} bars)"
    if "turnaround" in pattern:
        return f"Turnaround cell ({chord_count} bars)"
    if "ii-v" in pattern or "tritone" in pattern or "backdoor" in pattern:
        return f"Cadential cell ({chord_count} bars)"
    if "circle of fifths" in pattern:
        return f"Sequential cycle-of-fifths phrase ({chord_count} bars)"
    if pattern:
        return f"Representative {pattern_label} excerpt ({chord_count} bars)"
    return f"Representative excerpt ({chord_count} bars)"


def infer_tonal_center(sequence: ChordSequence) -> str:
    if not sequence.chords:
        return "Nedovoljno podataka"
    tonic = sequence.chords[-1]
    if tonic.quality == "maj":
        return f"{tonic.root} major"
    if tonic.quality == "min":
        return f"{tonic.root} minor"
    if tonic.quality == "dom":
        return f"{tonic.root} dominant pull"
    if tonic.quality == "half-dim":
        return f"{tonic.root} minor environment"
    return tonic.label


def detect_key_cadences(sequence: ChordSequence, pattern_label: str = "") -> list[str]:
    cadences: list[str] = []
    chords = sequence.chords
    pattern_lower = pattern_label.lower()

    for index in range(len(chords) - 2):
        first, second, third = chords[index : index + 3]
        first_to_second = (note_to_pitch_class(second.root) - note_to_pitch_class(first.root)) % 12
        second_to_third = (note_to_pitch_class(third.root) - note_to_pitch_class(second.root)) % 12
        if first.quality in {"min", "half-dim"} and second.quality == "dom" and first_to_second == 5 and second_to_third == 5:
            if third.quality == "maj":
                cadences.append(f"ii-V-I ka {third.label}")
            elif third.quality == "min":
                cadences.append(f"ii-V-i ka {third.label}")
        elif first.quality == "min" and second.quality == "dom" and third.quality == "maj" and first_to_second == 5 and second_to_third == 2:
            cadences.append(f"Backdoor ka {third.label}")

    for index in range(len(chords) - 3):
        first, second, third, fourth = chords[index : index + 4]
        first_to_second = (note_to_pitch_class(second.root) - note_to_pitch_class(first.root)) % 12
        second_to_third = (note_to_pitch_class(third.root) - note_to_pitch_class(second.root)) % 12
        third_to_fourth = (note_to_pitch_class(fourth.root) - note_to_pitch_class(third.root)) % 12
        if (
            first.quality == "maj"
            and second.quality == "dom"
            and third.quality == "min"
            and fourth.quality == "dom"
            and first_to_second == 9
            and second_to_third == 5
            and third_to_fourth == 5
        ):
            cadences.append(f"Turnaround: {first.label} - {second.label} - {third.label} - {fourth.label}")

    if "turnaround" in pattern_lower:
        cadences.append(f"Turnaround: frame ({len(chords)} chords)")

    if not cadences and pattern_label:
        cadences.append(pattern_label)

    unique: list[str] = []
    for cadence in cadences:
        if cadence not in unique:
            unique.append(cadence)
    return unique[:4]


def build_bass_harmonic_summary(
    bass_bar_overview: list[dict[str, str]],
    tonal_center: str,
    cadence_items: list[str],
    contains_turnaround: bool,
) -> str:
    if not bass_bar_overview:
        return "Bass linija jos nije generisana, pa nema sire harmonijske veze za komentar."

    total_bars = len(bass_bar_overview)
    root_anchors = sum(1 for bar in bass_bar_overview if bar.get("beat_one_role") == "root")
    guide_tone_bars = sum(1 for bar in bass_bar_overview if "guide tone emphasis" in bar.get("bar_comment", ""))
    chromatic_bars = sum(1 for bar in bass_bar_overview if "chromatic" in bar.get("bar_comment", ""))
    approach_bars = sum(1 for bar in bass_bar_overview if bar.get("beat_four_role") == "approach")

    if root_anchors == total_bars:
        anchor_text = "Bass linija na prvom beatu svakog takta jasno sidri koren akorda"
    else:
        anchor_text = f"Bass linija na prvom beatu potvrdjuje koren u {root_anchors} od {total_bars} taktova"

    if tonal_center and tonal_center != "Nedovoljno podataka":
        anchor_text += f", pa tonalni centar {tonal_center} ostaje pregledan."
    else:
        anchor_text += "."

    if guide_tone_bars:
        voice_leading_text = f"Srednji beatovi u {guide_tone_bars} taktova naglasavaju guide tone kretanje, sto pomaze da se funkcija akorda cuje i bez pune pratnje."
    else:
        voice_leading_text = "Srednji beatovi vise rade kao stabilna chord-tone podrska nego kao izrazena guide tone linija."

    if cadence_items:
        cadence_text = f"To posebno podrzava kadencu {cadence_items[0]}."
    elif contains_turnaround:
        cadence_text = "Zavrsni tonovi pripremaju turnaround i drze liniju funkcionalno otvorenom."
    else:
        cadence_text = "Linija ostaje vise u funkciji stabilizacije harmonije nego eksplicitne kadence."

    if approach_bars:
        approach_text = f"U {approach_bars} taktova cetvrti beat radi kao approach ton ka sledecem akordu"
        if chromatic_bars:
            approach_text += ", pa prelazi zvuce povezano i usmereno."
        else:
            approach_text += ", pa prelazi ostaju glatki."
    else:
        approach_text = "Zavrseci taktova ostaju unutar aktuelne harmonije umesto da guraju sledeci akord."

    return " ".join([anchor_text, voice_leading_text, cadence_text, approach_text])