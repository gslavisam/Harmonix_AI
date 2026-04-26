from __future__ import annotations

from dataclasses import dataclass

from .harmony import note_to_pitch_class, semitone_to_note


@dataclass(frozen=True, slots=True)
class ProgressionPattern:
    label: str
    category: str
    description: str
    degrees: tuple[tuple[int, str], ...]


@dataclass(frozen=True, slots=True)
class SongExample:
    title: str
    artist: str
    pattern_key: str
    progression: str
    note: str


PROGRESSION_PATTERNS = {
    "ii_v_i_major": ProgressionPattern(
        label="ii-V-I",
        category="Jazz Cadences",
        description="Klasična jazz kadenca u duru.",
        degrees=((2, "m7"), (7, "7"), (0, "maj7")),
    ),
    "ii_v_i_minor": ProgressionPattern(
        label="ii-V-i",
        category="Jazz Cadences",
        description="Minor kadenca sa half-diminished drugim stepenom.",
        degrees=((2, "m7b5"), (7, "7"), (0, "m7")),
    ),
    "turnaround_major": ProgressionPattern(
        label="Turnaround",
        category="Turnarounds & Standards",
        description="Osnovni I-vi-ii-V tok za zatvaranje forme.",
        degrees=((0, "maj7"), (9, "7"), (2, "m7"), (7, "7")),
    ),
    "circle_of_fifths": ProgressionPattern(
        label="Circle of fifths",
        category="Turnarounds & Standards",
        description="Sekvenca iii-vi-ii-V-I kroz ciklus kvinti.",
        degrees=((4, "m7"), (9, "7"), (2, "m7"), (7, "7"), (0, "maj7")),
    ),
    "tritone_sub": ProgressionPattern(
        label="Tritone sub",
        category="Jazz Cadences",
        description="ii-bII7-I varijanta sa tritonus supstitucijom dominante.",
        degrees=((2, "m7"), (1, "7"), (0, "maj7")),
    ),
    "backdoor": ProgressionPattern(
        label="Backdoor",
        category="Jazz Cadences",
        description="Backdoor rezolucija preko iv-bVII-I.",
        degrees=((5, "m7"), (10, "7"), (0, "maj7")),
    ),
    "doo_wop": ProgressionPattern(
        label="50s / Doo-wop",
        category="Pop & Classical",
        description="Poznati I-vi-IV-V pop standard u jazz-friendly oznakama.",
        degrees=((0, "maj7"), (9, "m7"), (5, "maj7"), (7, "7")),
    ),
    "pachelbel": ProgressionPattern(
        label="Pachelbel canon",
        category="Pop & Classical",
        description="Čuvena I-V-vi-iii-IV-I-IV-V sekvenca.",
        degrees=((0, "maj7"), (7, "7"), (9, "m7"), (4, "m7"), (5, "maj7"), (0, "maj7"), (5, "maj7"), (7, "7")),
    ),
    "andalusian": ProgressionPattern(
        label="Andalusian cadence",
        category="Pop & Classical",
        description="Moll obrazac i-bVII-bVI-V, čest u teoriji i praksi.",
        degrees=((0, "m7"), (10, "maj7"), (8, "maj7"), (7, "7")),
    ),
    "rhythm_changes_bridge": ProgressionPattern(
        label="Rhythm bridge",
        category="Turnarounds & Standards",
        description="Bridge iz Rhythm Changes sa dominantnim ciklusom.",
        degrees=((4, "7"), (9, "7"), (2, "7"), (7, "7")),
    ),
    "jazz_blues": ProgressionPattern(
        label="Jazz blues",
        category="Blues Forms",
        description="Osnovni 12-bar jazz blues sa turnaround završetkom.",
        degrees=((0, "7"), (5, "7"), (0, "7"), (0, "7"), (5, "7"), (5, "7"), (0, "7"), (9, "7"), (2, "m7"), (7, "7"), (0, "7"), (7, "7")),
    ),
    "minor_blues": ProgressionPattern(
        label="Minor blues",
        category="Blues Forms",
        description="12-bar minor blues sa dim prelazom i ii-V povratkom.",
        degrees=((0, "m7"), (5, "m7"), (0, "m7"), (0, "m7"), (5, "m7"), (6, "dim7"), (0, "m7"), (8, "7"), (2, "m7b5"), (7, "7"), (0, "m7"), (7, "7")),
    ),
}


SONG_EXAMPLES = {
    "autumn_leaves": SongExample(
        title="Autumn Leaves",
        artist="Joseph Kosma / jazz standard",
        pattern_key="circle_of_fifths",
        progression="Cm7 F7 Bbmaj7 Ebmaj7 Am7b5 D7 Gm7",
        note="Otvaranje pesme koristi lanac ii-V rezolucija i ciklus kvinti.",
    ),
    "there_will_never_be_another_you": SongExample(
        title="There Will Never Be Another You",
        artist="Harry Warren / jazz standard",
        pattern_key="ii_v_i_major",
        progression="Em7 A7 Dmaj7",
        note="Kratak i vrlo jasan primer dur ii-V-I kadence.",
    ),
    "blue_bossa": SongExample(
        title="Blue Bossa",
        artist="Kenny Dorham",
        pattern_key="ii_v_i_minor",
        progression="Cm7 Fm7 Dm7b5 G7 Cm7",
        note="Tema kombinuje minor centar i prepoznatljiv minor ii-V povratak.",
    ),
    "i_got_rhythm_bridge": SongExample(
        title="I Got Rhythm (bridge)",
        artist="George Gershwin",
        pattern_key="rhythm_changes_bridge",
        progression="D7 G7 C7 F7",
        note="Bridge je klasični dominantni ciklus poznat kao Rhythm Changes bridge.",
    ),
    "satin_doll": SongExample(
        title="Satin Doll",
        artist="Duke Ellington",
        pattern_key="turnaround_major",
        progression="Cmaj7 A7 Dm7 G7",
        note="Naslovni turnaround je jedan od standardnih ulaza u jazz harmoniju.",
    ),
    "stand_by_me": SongExample(
        title="Stand by Me",
        artist="Ben E. King",
        pattern_key="doo_wop",
        progression="Amaj7 F#m7 Dmaj7 E7",
        note="Poznati I-vi-IV-V obrazac u mirnom pop/soul kontekstu.",
    ),
    "basket_case": SongExample(
        title="Basket Case",
        artist="Green Day",
        pattern_key="pachelbel",
        progression="Emaj7 B7 C#m7 G#m7 Amaj7 Emaj7 Amaj7 B7",
        note="Savremeni pop-punk primer kanonske sekvence nalik Pachelbel obrascu.",
    ),
    "hit_the_road_jack": SongExample(
        title="Hit the Road Jack",
        artist="Ray Charles",
        pattern_key="andalusian",
        progression="Am7 Gmaj7 Fmaj7 E7",
        note="Prepoznatljiv silazni moll obrazac blizak Andalusian kadenci.",
    ),
    "straight_no_chaser": SongExample(
        title="Straight, No Chaser",
        artist="Thelonious Monk",
        pattern_key="jazz_blues",
        progression="F7 Bb7 F7 F7 Bb7 Bb7 F7 D7 Gm7 C7 F7 C7",
        note="Jedan od najprepoznatljivijih jazz blues primera u standardnom obliku.",
    ),
    "equinox": SongExample(
        title="Equinox",
        artist="John Coltrane",
        pattern_key="minor_blues",
        progression="Cm7 Fm7 Cm7 Cm7 Fm7 Gbdim7 Cm7 Ab7 Dm7b5 G7 Cm7 G7",
        note="Poznata minor blues forma sa tipičnim dim prelazom i povratnim ii-V.",
    ),
}


def build_progression_catalog() -> tuple[tuple[str, tuple[tuple[str, str, str], ...]], ...]:
    category_order = (
        "Jazz Cadences",
        "Turnarounds & Standards",
        "Blues Forms",
        "Pop & Classical",
    )
    grouped: dict[str, list[tuple[str, str, str]]] = {category: [] for category in category_order}
    for pattern_key, pattern in PROGRESSION_PATTERNS.items():
        grouped.setdefault(pattern.category, []).append((pattern_key, pattern.label, pattern.description))

    return tuple(
        (category, tuple(grouped[category]))
        for category in category_order
        if grouped.get(category)
    )


def build_song_example_catalog() -> tuple[tuple[str, tuple[tuple[str, str, str, str, str, str], ...]], ...]:
    grouped: dict[str, list[tuple[str, str, str, str, str, str]]] = {
        category: []
        for category, _entries in build_progression_catalog()
    }
    for example in SONG_EXAMPLES.values():
        pattern = PROGRESSION_PATTERNS[example.pattern_key]
        grouped.setdefault(pattern.category, []).append(
            (
                example.title,
                example.artist,
                pattern.label,
                example.progression,
                example.note,
                example.pattern_key,
            )
        )

    return tuple(
        (category, tuple(grouped[category]))
        for category in grouped
        if grouped.get(category)
    )


def build_progression_from_pattern(pattern_key: str, tonic: str) -> str:
    pattern = PROGRESSION_PATTERNS[pattern_key]
    tonic_pc = note_to_pitch_class(tonic)
    chords = []
    for interval, suffix in pattern.degrees:
        root = semitone_to_note(tonic_pc + interval)
        chords.append(f"{root}{suffix}")
    return " ".join(chords)