from harmonix.core.harmony import parse_progression
from harmonix.core.theory_library import build_theory_profile


def test_build_theory_profile_prefers_minor_ii_v_i_cadence() -> None:
    profile = build_theory_profile(
        "",
        "Notation import",
        ["ii-V-i ka Am7"],
        parse_progression("Bm7b5 E7 Am7"),
    )

    assert profile["title"] == "Theory Lab: ii-V-i u molu"


def test_build_theory_profile_prefers_major_ii_v_i_cadence() -> None:
    profile = build_theory_profile(
        "",
        "Notation import",
        ["ii-V-I ka Cmaj7"],
        parse_progression("Dm7 G7 Cmaj7"),
    )

    assert profile["title"] == "Theory Lab: ii-V-I u duru"


def test_build_theory_profile_can_infer_minor_ii_v_i_from_sequence() -> None:
    profile = build_theory_profile(
        "",
        "Notation import",
        [],
        parse_progression("Bm7b5 E7 Am7"),
    )

    assert profile["title"] == "Theory Lab: ii-V-i u molu"