from __future__ import annotations

import reflex as rx

from harmonix.state import AppState, PROGRESSION_PRESETS, SONG_EXAMPLES


ROOT_OPTIONS = ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")
QUALITY_OPTIONS = (
    ("maj7", "maj7"),
    ("m7", "m7"),
    ("7", "7"),
    ("m7b5", "m7b5"),
    ("dim7", "dim7"),
)

PAGE_BACKGROUND = (
    "radial-gradient(circle at top left, rgba(245,158,11,0.16), transparent 24%), "
    "radial-gradient(circle at top right, rgba(59,130,246,0.18), transparent 26%), "
    "linear-gradient(180deg, #090d14 0%, #0b1120 50%, #0a0f1a 100%)"
)
SURFACE_BACKGROUND = "linear-gradient(180deg, rgba(15,23,42,0.92) 0%, rgba(15,23,42,0.76) 100%)"
SURFACE_BORDER = "1px solid rgba(148,163,184,0.16)"
MUTED_TEXT = "rgba(226,232,240,0.74)"
SUBTLE_TEXT = "rgba(148,163,184,0.9)"


def surface_card(*children, **props) -> rx.Component:
    base_props = {
        "background": SURFACE_BACKGROUND,
        "border": SURFACE_BORDER,
        "box_shadow": "0 24px 80px rgba(2,6,23,0.30)",
        "backdrop_filter": "blur(16px)",
        "color": "#e2e8f0",
        "width": "100%",
    }
    base_props.update(props)
    return rx.card(*children, **base_props)


def inner_panel(*children, **props) -> rx.Component:
    base_props = {
        "background": "rgba(15,23,42,0.42)",
        "border": "1px solid rgba(148,163,184,0.14)",
        "border_radius": "16px",
        "padding": "1rem",
        "width": "100%",
    }
    base_props.update(props)
    return rx.box(*children, **base_props)


def section_header(title: str, badge_text: str, badge_color: str = "amber") -> rx.Component:
    return rx.hstack(
        rx.heading(title, size="5"),
        rx.badge(badge_text, color_scheme=badge_color, variant="soft"),
        wrap="wrap",
        spacing="2",
        align="start",
        justify="between",
        width="100%",
    )


def analysis_metric_card(title: str, body, accent: str = "amber") -> rx.Component:
    return inner_panel(
        rx.vstack(
            rx.badge(title, color_scheme=accent, variant="soft"),
            body,
            spacing="2",
            align_items="start",
            width="100%",
        ),
        min_height="132px",
    )


def theory_section_card(section) -> rx.Component:
    return analysis_metric_card(
        section["title"],
        rx.text(section["body"], line_height="1.6", white_space="pre-wrap"),
        accent=section["accent"],
    )


def processing_panel(title: str, message: str) -> rx.Component:
    return inner_panel(
        rx.hstack(
            rx.box(
                rx.spinner(size="3"),
                background="rgba(245,158,11,0.10)",
                border="1px solid rgba(245,158,11,0.20)",
                border_radius="999px",
                padding="0.55rem",
            ),
            rx.vstack(
                rx.text(title, font_weight="700"),
                rx.text(message, color=MUTED_TEXT, line_height="1.55"),
                spacing="1",
                align_items="start",
                width="100%",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        background="rgba(245,158,11,0.08)",
        border="1px solid rgba(245,158,11,0.18)",
    )


def workspace_tab_button(value: str, label: str, description: str) -> rx.Component:
    is_active = AppState.assistant_panel_tab == value
    return rx.button(
        rx.vstack(
            rx.text(label, font_weight="700", color=rx.cond(is_active, "#f8fafc", "rgba(226,232,240,0.88)")),
            rx.text(description, font_size="0.78rem", color=rx.cond(is_active, "rgba(241,245,249,0.82)", "rgba(148,163,184,0.88)")),
            spacing="1",
            align_items="start",
            width="100%",
        ),
        on_click=AppState.set_assistant_panel_tab(value),
        background=rx.cond(
            is_active,
            "linear-gradient(135deg, rgba(245,158,11,0.28), rgba(59,130,246,0.22))",
            "rgba(15,23,42,0.36)",
        ),
        border=rx.cond(
            is_active,
            "1px solid rgba(245,158,11,0.38)",
            "1px solid rgba(148,163,184,0.14)",
        ),
        border_radius="14px",
        padding="0.9rem 1rem",
        width="100%",
        height="100%",
        justify_content="flex-start",
    )


def progression_category_panel(category: str, entries) -> rx.Component:
    return surface_card(
        rx.vstack(
            rx.hstack(
                rx.heading(category, size="3"),
                rx.badge(str(len(entries)) + " preset", variant="soft"),
                justify="between",
                width="100%",
            ),
            rx.flex(
                *[
                    rx.box(
                        rx.vstack(
                            rx.button(
                                label,
                                size="2",
                                variant="soft",
                                color_scheme="amber",
                                on_click=AppState.apply_preset(pattern_key),
                                width="100%",
                            ),
                            rx.text(
                                description,
                                color=MUTED_TEXT,
                                font_size="0.85rem",
                                line_height="1.45",
                            ),
                            spacing="2",
                            align_items="start",
                            width="100%",
                        ),
                        width="100%",
                        max_width="100%",
                        min_width="0",
                        flex="1 1 260px",
                        min_height="128px",
                        background="rgba(15,23,42,0.34)",
                        border="1px solid rgba(148,163,184,0.12)",
                        border_radius="16px",
                        padding="1rem",
                    )
                    for pattern_key, label, description in entries
                ],
                wrap="wrap",
                gap="3",
                width="100%",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        padding="1rem",
    )


def song_examples_category_panel(category: str, entries) -> rx.Component:
    return surface_card(
        rx.vstack(
            rx.hstack(
                rx.heading(category, size="3"),
                rx.badge(str(len(entries)) + " primer", variant="soft"),
                justify="between",
                width="100%",
            ),
            rx.flex(
                *[
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.heading(title, size="3"),
                                rx.badge(pattern_label, color_scheme="amber", variant="soft"),
                                wrap="wrap",
                                spacing="2",
                                width="100%",
                            ),
                            rx.text(artist, color=MUTED_TEXT, font_size="0.85rem"),
                            rx.text(progression, font_family="Consolas, 'Courier New', monospace", white_space="pre-wrap"),
                            rx.text(note, color=MUTED_TEXT, font_size="0.85rem", line_height="1.45"),
                            rx.hstack(
                                rx.button(
                                    "Učitaj primer",
                                    variant="outline",
                                    on_click=AppState.load_song_example(title, artist, pattern_label, _pattern_key, note, progression),
                                ),
                                rx.button(
                                    "Analiziraj pesmu",
                                    color_scheme="amber",
                                    on_click=AppState.analyze_song_example(title, artist, pattern_label, _pattern_key, note, progression),
                                ),
                                wrap="wrap",
                                spacing="2",
                            ),
                            spacing="2",
                            align_items="start",
                            width="100%",
                        ),
                        width="100%",
                        max_width="100%",
                        min_width="0",
                        flex="1 1 300px",
                        min_height="228px",
                        background="rgba(15,23,42,0.34)",
                        border="1px solid rgba(148,163,184,0.12)",
                        border_radius="16px",
                        padding="1rem",
                    )
                    for title, artist, pattern_label, progression, note, _pattern_key in entries
                ],
                wrap="wrap",
                gap="3",
                width="100%",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        padding="1rem",
    )


def progression_browser_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Poznate progresije", size="4"),
            rx.badge("Klik za brzi unos", color_scheme="amber", variant="soft"),
            justify="between",
            width="100%",
        ),
        rx.text("Katalog je najbolji za trenutni start: prvo biraš harmonski obrazac, pa odmah dobijaš upotrebljiv unos za analizu.", color=MUTED_TEXT),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text("Tonalitet preseta", color=SUBTLE_TEXT),
                    rx.badge(AppState.selected_preset_key, color_scheme="amber", variant="soft"),
                    spacing="2",
                    wrap="wrap",
                ),
                rx.flex(
                    *[
                        rx.button(
                            root,
                            size="1",
                            variant="outline",
                            on_click=AppState.set_selected_preset_key(root),
                        )
                        for root in ROOT_OPTIONS
                    ],
                    wrap="wrap",
                    gap="2",
                    width="100%",
                ),
                spacing="3",
                align_items="start",
                width="100%",
            ),
            background="rgba(15,23,42,0.46)",
            border="1px solid rgba(148,163,184,0.14)",
            border_radius="16px",
            padding="1rem",
            width="100%",
        ),
        rx.vstack(
            inner_panel(
                rx.hstack(
                    rx.vstack(
                        rx.text("Klasifikacija", color=SUBTLE_TEXT, font_size="0.78rem"),
                        rx.select(
                            [category for category, _ in PROGRESSION_PRESETS],
                            value=AppState.selected_progression_category,
                            on_change=AppState.set_selected_progression_category,
                            width=rx.breakpoints(initial="100%", sm="320px"),
                        ),
                        spacing="1",
                        align_items="start",
                        width="100%",
                    ),
                    rx.badge(AppState.selected_progression_category, color_scheme="blue", variant="soft"),
                    justify="between",
                    align="end",
                    wrap="wrap",
                    width="100%",
                ),
            ),
            *[
                rx.cond(
                    AppState.selected_progression_category == category,
                    progression_category_panel(category, entries),
                    rx.fragment(),
                )
                for category, entries in PROGRESSION_PRESETS
            ],
            spacing="3",
            width="100%",
        ),
        spacing="3",
        align_items="start",
        width="100%",
    )


def song_examples_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Poznate pesme", size="4"),
            rx.badge("Primeri po patternu", color_scheme="amber", variant="soft"),
            justify="between",
            width="100%",
        ),
        rx.text("Ovaj pogled je najintuitivniji kada već znaš referencu i želiš da odmah učitaš reprezentativni isečak ili kreneš u analizu pesme.", color=MUTED_TEXT),
        rx.vstack(
            inner_panel(
                rx.hstack(
                    rx.vstack(
                        rx.text("Klasifikacija", color=SUBTLE_TEXT, font_size="0.78rem"),
                        rx.select(
                            [category for category, _ in SONG_EXAMPLES],
                            value=AppState.selected_song_category,
                            on_change=AppState.set_selected_song_category,
                            width=rx.breakpoints(initial="100%", sm="320px"),
                        ),
                        spacing="1",
                        align_items="start",
                        width="100%",
                    ),
                    rx.badge(AppState.selected_song_category, color_scheme="blue", variant="soft"),
                    justify="between",
                    align="end",
                    wrap="wrap",
                    width="100%",
                ),
            ),
            *[
                rx.cond(
                    AppState.selected_song_category == category,
                    song_examples_category_panel(category, entries),
                    rx.fragment(),
                )
                for category, entries in SONG_EXAMPLES
            ],
            spacing="3",
            width="100%",
        ),
        spacing="3",
        align_items="start",
        width="100%",
    )


def notation_upload_panel() -> rx.Component:
    upload_id = "notation-upload"
    selected_files = rx.selected_files(upload_id)
    upload_busy = AppState.is_notation_file_uploading | AppState.is_uploading_notation
    return rx.vstack(
        rx.hstack(
            rx.heading("Upload notation", size="4"),
            rx.badge("PDF + image", color_scheme="amber", variant="soft"),
            justify="between",
            width="100%",
        ),
        rx.text(
            "Uploaduj lead sheet, chord chart ili fotografiju notacije. Sistem pokušava da pročita harmonijske oznake preko LM Studio modela, prebaci ih u gotovu progresiju i odmah pokrene analizu.",
            color=MUTED_TEXT,
        ),
        inner_panel(
            rx.vstack(
                rx.upload(
                    rx.vstack(
                        rx.box(
                            rx.icon("upload", size=26, color="#fbbf24"),
                            background="rgba(245,158,11,0.10)",
                            border="1px solid rgba(245,158,11,0.20)",
                            border_radius="999px",
                            padding="0.7rem",
                        ),
                        rx.text("Drag & drop ili klik za upload"),
                        rx.text("Podržani su PDF, PNG, JPG, JPEG i WEBP", size="1", color=SUBTLE_TEXT),
                        align="center",
                        spacing="2",
                        padding="2.2rem 1.6rem",
                    ),
                    id=upload_id,
                    accept={
                        "application/pdf": [".pdf"],
                        "image/png": [".png"],
                        "image/jpeg": [".jpg", ".jpeg"],
                        "image/webp": [".webp"],
                    },
                    max_files=1,
                    border="2px dashed rgba(245,158,11,0.28)",
                    background="rgba(2,6,23,0.24)",
                    border_radius="18px",
                    cursor="pointer",
                    width="100%",
                ),
                rx.button(
                    rx.cond(
                        upload_busy,
                        rx.hstack(
                            rx.spinner(size="2"),
                            rx.text("Čitam i analiziram notaciju..."),
                            spacing="2",
                            align="center",
                        ),
                        rx.cond(
                            selected_files.length() > 0,
                            rx.text("Učitaj i analiziraj notaciju"),
                            rx.text("Prvo izaberi fajl za upload"),
                        ),
                    ),
                    on_click=AppState.handle_notation_upload(
                        rx.upload_files(
                            upload_id=upload_id,
                            on_upload_progress=AppState.track_notation_upload_progress,
                        )
                    ),
                    color_scheme="amber",
                    width="100%",
                    disabled=(selected_files.length() == 0) | upload_busy | AppState.is_processing,
                ),
                rx.cond(
                    selected_files.length() > 0,
                    inner_panel(
                        rx.vstack(
                            rx.text("Odabrano za upload", font_weight="600"),
                            rx.foreach(
                                selected_files,
                                lambda file_name: rx.badge(file_name, variant="soft", color_scheme="amber"),
                            ),
                            spacing="2",
                            align_items="start",
                            width="100%",
                        ),
                        background="rgba(245,158,11,0.07)",
                        border="1px solid rgba(245,158,11,0.18)",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    upload_busy,
                    processing_panel(
                        "Notation upload je u toku",
                        rx.cond(
                            AppState.uploaded_notation_status != "",
                            AppState.uploaded_notation_status,
                            "Uploadujem dokument i čekam odgovor modela.",
                        ),
                    ),
                ),
                rx.cond(
                    AppState.uploaded_notation_filename != "",
                    inner_panel(
                        rx.vstack(
                            rx.hstack(
                                rx.badge("File", variant="soft", color_scheme="blue"),
                                rx.text(AppState.uploaded_notation_filename, font_weight="600"),
                                wrap="wrap",
                                spacing="2",
                                width="100%",
                            ),
                            rx.cond(AppState.uploaded_notation_status != "", rx.text(AppState.uploaded_notation_status, color=MUTED_TEXT)),
                            rx.cond(
                                AppState.uploaded_notation_model_used != "",
                                rx.hstack(
                                    rx.badge(
                                        rx.cond(AppState.uploaded_notation_offline_mode, "Offline extraction", "LLM extraction"),
                                        color_scheme=rx.cond(AppState.uploaded_notation_offline_mode, "orange", "amber"),
                                        variant="soft",
                                    ),
                                    rx.badge(AppState.uploaded_notation_model_used, color_scheme="blue", variant="soft"),
                                    spacing="2",
                                    wrap="wrap",
                                    width="100%",
                                ),
                            ),
                            rx.cond(
                                AppState.uploaded_notation_progression_preview != "",
                                rx.vstack(
                                    rx.text("Izvučena progresija", font_weight="600"),
                                    rx.box(
                                        rx.text(
                                            AppState.uploaded_notation_progression_preview,
                                            font_family="Consolas, 'Courier New', monospace",
                                            white_space="pre-wrap",
                                        ),
                                        background="rgba(2,6,23,0.28)",
                                        border="1px solid rgba(148,163,184,0.12)",
                                        border_radius="12px",
                                        padding="0.85rem 1rem",
                                        width="100%",
                                    ),
                                    spacing="2",
                                    align_items="start",
                                    width="100%",
                                ),
                            ),
                            rx.cond(
                                AppState.uploaded_notation_note != "",
                                rx.text(AppState.uploaded_notation_note, color=MUTED_TEXT, line_height="1.6"),
                            ),
                            rx.cond(AppState.uploaded_notation_excerpt != "", rx.text("Izvod iz dokumenta: " + AppState.uploaded_notation_excerpt, color=MUTED_TEXT, line_height="1.6")),
                            spacing="2",
                            align_items="start",
                            width="100%",
                        ),
                        background="rgba(2,6,23,0.24)",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    AppState.uploaded_notation_error != "",
                    inner_panel(
                        rx.text(AppState.uploaded_notation_error, color="#fecaca"),
                        background="rgba(127,29,29,0.45)",
                        border="1px solid rgba(248,113,113,0.35)",
                    ),
                    rx.fragment(),
                ),
                spacing="3",
                align_items="start",
                width="100%",
            ),
        ),
        spacing="3",
        align_items="start",
        width="100%",
    )


def chord_builder_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Chord Builder", size="4"),
            rx.badge("Ručni unos", color_scheme="amber", variant="soft"),
            justify="between",
            width="100%",
        ),
        rx.text("Builder je najkorisniji kada već znaš akorde koje želiš da sastaviš, ali hoćeš brži izbor korena i kvaliteta bez kucanja svakog tokena ručno.", color=MUTED_TEXT),
        rx.hstack(
            rx.box(
                rx.vstack(
                    rx.text("Izaberi koren", font_weight="600"),
                    rx.badge(AppState.selected_root, color_scheme="amber", variant="soft"),
                    rx.flex(
                        *[
                            rx.button(
                                root,
                                size="2",
                                variant="outline",
                                on_click=AppState.set_selected_root(root),
                            )
                            for root in ROOT_OPTIONS
                        ],
                        wrap="wrap",
                        gap="2",
                        width="100%",
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
                background="rgba(15,23,42,0.40)",
                border="1px solid rgba(148,163,184,0.14)",
                border_radius="16px",
                padding="1rem",
                width="100%",
            ),
            rx.box(
                rx.vstack(
                    rx.text("Izaberi kvalitet", font_weight="600"),
                    rx.badge(AppState.selected_quality, color_scheme="amber", variant="soft"),
                    rx.flex(
                        *[
                            rx.button(
                                label,
                                size="2",
                                variant="outline",
                                on_click=AppState.set_selected_quality(quality),
                            )
                            for label, quality in QUALITY_OPTIONS
                        ],
                        wrap="wrap",
                        gap="2",
                        width="100%",
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
                background="rgba(15,23,42,0.40)",
                border="1px solid rgba(148,163,184,0.14)",
                border_radius="16px",
                padding="1rem",
                width="100%",
            ),
            spacing="3",
            align_items="stretch",
            width="100%",
            wrap="wrap",
        ),
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text("Sledeći akord", color=SUBTLE_TEXT, font_size="0.82rem"),
                    rx.text(AppState.selected_root + AppState.selected_quality, font_family="Consolas, 'Courier New', monospace", font_size="1.1rem", font_weight="700"),
                    spacing="1",
                    align_items="start",
                ),
                rx.hstack(
                    rx.button("Dodaj akord", on_click=AppState.append_selected_chord, color_scheme="amber"),
                    rx.button("Očisti unos", on_click=AppState.clear_progression_input, variant="outline"),
                    spacing="3",
                    wrap="wrap",
                ),
                justify="between",
                align="center",
                width="100%",
                wrap="wrap",
            ),
            background="linear-gradient(135deg, rgba(245,158,11,0.16), rgba(59,130,246,0.10))",
            border="1px solid rgba(245,158,11,0.18)",
            border_radius="16px",
            padding="1rem",
            width="100%",
        ),
        spacing="3",
        align_items="start",
        width="100%",
    )


def progression_assistant() -> rx.Component:
    return surface_card(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.badge("Creative Workspace", color_scheme="amber", variant="soft"),
                    rx.heading("Izbor početnog materijala", size="5"),
                    rx.text("Najlogičniji tok je: prvo izaberi izvor progresije, zatim po potrebi doradi unos i tek onda pokreni analizu.", color=MUTED_TEXT),
                    spacing="2",
                    align_items="start",
                ),
                rx.badge("Presets + songs + builder", color_scheme="blue", variant="soft"),
                justify="between",
                align="start",
                width="100%",
            ),
            rx.grid(
                workspace_tab_button("progressions", "Poznate progresije", "Za brzi start iz harmonskog obrasca"),
                workspace_tab_button("songs", "Poznate pesme", "Za rad iz referentne pesme"),
                workspace_tab_button("builder", "Chord Builder", "Za ručno sastavljanje progresije"),
                workspace_tab_button("upload", "Upload notation", "Za PDF, sliku i gotovu notaciju"),
                columns=rx.breakpoints(initial="1", sm="2", lg="4"),
                    spacing="2",
                width="100%",
            ),
            rx.box(
                rx.cond(
                    AppState.assistant_panel_tab == "progressions",
                    progression_browser_panel(),
                    rx.cond(
                        AppState.assistant_panel_tab == "songs",
                        song_examples_panel(),
                        rx.cond(
                            AppState.assistant_panel_tab == "builder",
                            chord_builder_panel(),
                            notation_upload_panel(),
                        ),
                    ),
                ),
                background="rgba(2,6,23,0.18)",
                border="1px solid rgba(148,163,184,0.12)",
                border_radius="18px",
                padding="1rem",
                width="100%",
            ),
            rx.hstack(
                rx.badge("Preset key: " + AppState.selected_preset_key, variant="soft", color_scheme="amber"),
                rx.badge("Builder: " + AppState.selected_root + AppState.selected_quality, variant="soft", color_scheme="blue"),
                rx.cond(
                    AppState.selected_song_title != "",
                    rx.badge("Song focus: " + AppState.selected_song_title, variant="soft", color_scheme="green"),
                    rx.badge("Song focus: none", variant="soft"),
                ),
                rx.cond(
                    AppState.uploaded_notation_filename != "",
                    rx.badge("Upload: " + AppState.uploaded_notation_filename, variant="soft", color_scheme="orange"),
                    rx.fragment(),
                ),
                wrap="wrap",
                spacing="2",
                width="100%",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        padding="1.2rem",
    )


def selected_song_card() -> rx.Component:
    return surface_card(
        rx.vstack(
            section_header("Song Analysis", AppState.selected_song_pattern),
            inner_panel(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.heading(AppState.selected_song_title, size="6"),
                            rx.text(AppState.selected_song_artist, color=MUTED_TEXT),
                            spacing="1",
                            align_items="start",
                        ),
                        rx.badge("Reference track", color_scheme="green", variant="soft"),
                        justify="between",
                        align="start",
                        width="100%",
                    ),
                    rx.text(AppState.selected_song_note, color=MUTED_TEXT),
                    rx.box(
                        rx.text(AppState.chord_input, font_family="Consolas, 'Courier New', monospace", white_space="pre-wrap"),
                        background="rgba(2,6,23,0.28)",
                        border="1px solid rgba(148,163,184,0.12)",
                        border_radius="12px",
                        padding="0.85rem 1rem",
                        width="100%",
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
            ),
            rx.hstack(
                rx.badge("Roots: " + AppState.analysis_roots_text, variant="soft"),
                rx.badge(AppState.analysis_tension_text, variant="soft"),
                rx.badge(AppState.analysis_turnaround_text, variant="soft"),
                wrap="wrap",
                spacing="2",
                width="100%",
            ),
            rx.grid(
                analysis_metric_card(
                    "Forma",
                    rx.text(AppState.analysis_form_text, line_height="1.55"),
                    accent="amber",
                ),
                analysis_metric_card(
                    "Tonalni Centar",
                    rx.text(AppState.analysis_tonal_center_text, line_height="1.55"),
                    accent="blue",
                ),
                analysis_metric_card(
                    "Ključne Kadence",
                    rx.cond(
                        AppState.analysis_cadence_items.length() > 0,
                        rx.vstack(
                            rx.foreach(AppState.analysis_cadence_items, lambda item: rx.text("- " + item)),
                            spacing="1",
                            align_items="start",
                            width="100%",
                        ),
                        rx.text("Nema izdvojenih kadenci za ovaj isečak."),
                    ),
                    accent="green",
                ),
                columns=rx.breakpoints(initial="1", md="2", xl="3"),
                spacing="3",
                width="100%",
            ),
            inner_panel(
                rx.vstack(
                    rx.hstack(
                        rx.badge("Bass i Harmonija", color_scheme="amber", variant="soft"),
                        rx.badge("Cross-layer summary", color_scheme="blue", variant="soft"),
                        wrap="wrap",
                        spacing="2",
                        width="100%",
                    ),
                    rx.text(AppState.analysis_bass_harmony_text, line_height="1.7"),
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
            ),
            inner_panel(
                rx.vstack(
                    rx.hstack(
                        rx.badge("Song focus", color_scheme="amber", variant="soft"),
                        rx.badge("AI Notes ispod", color_scheme="blue", variant="soft"),
                        wrap="wrap",
                        spacing="2",
                        width="100%",
                    ),
                    rx.text(
                        "Ova kartica ostaje fokusirana na formu, tonalni centar, kadence i odnos bass linije i harmonije. AI interpretacija, preporuke i sokratska pitanja ostaju u AI Notes kako se sadržaj ne bi ponavljao.",
                        color=MUTED_TEXT,
                        line_height="1.65",
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
                background="rgba(2,6,23,0.20)",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
    )


def theory_lab_card() -> rx.Component:
    return surface_card(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(rx.cond(AppState.theory_title != "", AppState.theory_title, "Theory Lab"), size="5"),
                    rx.text(
                        rx.cond(
                            AppState.theory_overview != "",
                            AppState.theory_overview,
                            "Analiziraj progresiju da ovde dobiješ teorijsku mapu: funkciju, supstitucije, bass line opcije i standardnu praksu izvođenja.",
                        ),
                        color=MUTED_TEXT,
                        line_height="1.7",
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
                rx.badge("Knowledge base", color_scheme="amber", variant="soft"),
                justify="between",
                align="start",
                width="100%",
            ),
            rx.cond(
                AppState.theory_sections.length() > 0,
                rx.vstack(
                    rx.foreach(
                        AppState.theory_sections,
                        lambda section: rx.box(theory_section_card(section), width="100%"),
                    ),
                    spacing="3",
                    align_items="stretch",
                    width="100%",
                ),
                inner_panel(
                    rx.text(
                        "Theory Lab ostaje prazan dok ne pokreneš analizu nad poznatim ili ručno unetim materijalom.",
                        color=MUTED_TEXT,
                    ),
                    background="rgba(2,6,23,0.20)",
                ),
            ),
            rx.cond(
                AppState.theory_resource_hint != "",
                inner_panel(
                    rx.vstack(
                        rx.badge("Dalje istraživanje", color_scheme="blue", variant="soft"),
                        rx.text(AppState.theory_resource_hint, color=MUTED_TEXT, line_height="1.65"),
                        spacing="2",
                        align_items="start",
                        width="100%",
                    ),
                    background="rgba(59,130,246,0.06)",
                    border="1px solid rgba(59,130,246,0.16)",
                ),
                rx.fragment(),
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
    )


def chord_input() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.badge("Composing Workspace", color_scheme="amber", variant="soft"),
            rx.heading("Harmonix AI", size="8", line_height="1.02"),
            rx.text(
                "Organizuj unos kao radni tok: izaberi progresiju ili referentnu pesmu u tabovima, doradi ulaz po potrebi i tek onda pokreni analizu i generisanje bass linije.",
                color=MUTED_TEXT,
                max_width="820px",
                line_height="1.7",
            ),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        progression_assistant(),
        surface_card(
            rx.vstack(
                rx.hstack(
                    rx.heading("Radni ulaz", size="4"),
                    rx.badge("Editable progression", color_scheme="blue", variant="soft"),
                    justify="between",
                    width="100%",
                ),
                rx.text_area(
                    placeholder="Unesi progresiju, npr. Dm7 G7 Cmaj7",
                    value=AppState.chord_input,
                    on_change=AppState.validate_input,
                    width="100%",
                    min_height="140px",
                ),
                rx.hstack(
                    rx.input(
                        type="number",
                        value=AppState.tempo,
                        on_change=AppState.set_tempo,
                        width="140px",
                    ),
                    rx.button(
                        rx.cond(
                            AppState.is_processing,
                            rx.hstack(
                                rx.spinner(size="2"),
                                rx.text("Analiza u toku..."),
                                spacing="2",
                                align="center",
                            ),
                            rx.text("Analiziraj i Generiši"),
                        ),
                        on_click=AppState.analyze_and_generate,
                        disabled=(AppState.validation_error != "") | (AppState.chord_input == "") | AppState.is_processing,
                        color_scheme="amber",
                    ),
                    wrap="wrap",
                    spacing="3",
                    width="100%",
                ),
                rx.cond(
                    AppState.is_processing,
                    inner_panel(
                        rx.hstack(
                            rx.spinner(size="3"),
                            rx.vstack(
                                rx.text("Analiza je u toku", font_weight="700"),
                                rx.text(
                                    rx.cond(
                                        AppState.analysis_status_text != "",
                                        AppState.analysis_status_text,
                                        "Obrađujem progresiju i pripremam prikaz rezultata.",
                                    ),
                                    color=MUTED_TEXT,
                                    line_height="1.55",
                                ),
                                spacing="1",
                                align_items="start",
                                width="100%",
                            ),
                            spacing="3",
                            align="start",
                            width="100%",
                        ),
                        background="rgba(59,130,246,0.08)",
                        border="1px solid rgba(59,130,246,0.20)",
                    ),
                ),
                rx.cond(
                    AppState.is_processing,
                    rx.fragment(),
                    rx.fragment(),
                ),
                rx.cond(AppState.validation_error != "", rx.text(AppState.validation_error, color="#fda4af")),
                spacing="3",
                align_items="start",
                width="100%",
            ),
            padding="1.2rem",
        ),
        align_items="start",
        width="100%",
    )


def chord_chips() -> rx.Component:
    return rx.flex(
        rx.foreach(AppState.parsed_chords, lambda chord: rx.badge(chord, color_scheme="amber", variant="soft")),
        wrap="wrap",
        gap="2",
        width="100%",
    )


def progression_snapshot_card() -> rx.Component:
    return surface_card(
        rx.vstack(
            rx.hstack(
                rx.heading("Progression Snapshot", size="4"),
                rx.badge("Current material", color_scheme="blue", variant="soft"),
                justify="between",
                width="100%",
            ),
            rx.cond(
                AppState.parsed_chords.length() > 0,
                rx.vstack(
                    chord_chips(),
                    rx.hstack(
                        rx.badge("Tempo: " + AppState.tempo.to_string(), variant="soft"),
                        rx.badge("Chords: " + AppState.parsed_chords.length().to_string(), variant="soft"),
                        rx.cond(
                            AppState.selected_song_title != "",
                            rx.badge("Reference: " + AppState.selected_song_title, color_scheme="green", variant="soft"),
                            rx.badge("Reference: manual", variant="soft"),
                        ),
                        wrap="wrap",
                        spacing="2",
                        width="100%",
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
                rx.cond(
                    AppState.is_processing,
                    processing_panel(
                        "Gradim progression snapshot",
                        "Prvo lokalno validiram unos i pripremam harmonski pregled pre nego što popunim ostale sekcije.",
                    ),
                    rx.text("Kada uneseš ili izabereš progresiju, ovde dobijaš brzi pregled trenutnog materijala pre detaljne analize.", color=MUTED_TEXT),
                ),
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        padding="1.1rem",
    )


def analysis_actions_card() -> rx.Component:
    return surface_card(
        rx.vstack(
            rx.hstack(
                rx.heading("Actions", size="4"),
                rx.cond(
                    AppState.is_processing,
                    rx.badge("Waiting for results", color_scheme="orange", variant="soft"),
                    rx.badge("Export + prompt", color_scheme="amber", variant="soft"),
                ),
                justify="between",
                width="100%",
            ),
            rx.cond(
                AppState.is_processing,
                processing_panel(
                    "Akcije će se otključati po završetku",
                    "Kada bass i AI rezultat budu spremni, ovde će postati dostupni MIDI eksport i kopiranje Suno prompta.",
                ),
                rx.vstack(
                    rx.text("Kada analiza postoji, odavde izvoziš MIDI ili prenosiš prompt dalje u produkcioni tok.", color=MUTED_TEXT),
                    export_actions(),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        padding="1.1rem",
    )


def analysis_workspace_header() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.badge("Analysis Dashboard", color_scheme="blue", variant="soft"),
                    rx.heading("Rezultati i izvođenje", size="6"),
                    rx.text(
                        "Leva strana nosi harmonijsku priču i bass analizu, dok desna strana prikazuje instrument-specifične poglede. Na manjim ekranima kolone se prirodno slažu jedna ispod druge.",
                        color=MUTED_TEXT,
                        max_width="860px",
                        line_height="1.7",
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
                rx.cond(
                    AppState.is_processing,
                    rx.badge("Analyzing...", color_scheme="amber", variant="soft"),
                    rx.badge("Ready", color_scheme="green", variant="soft"),
                ),
                justify="between",
                align="start",
                width="100%",
            ),
            rx.hstack(
                rx.badge("Harmony + narrative", variant="soft", color_scheme="amber"),
                rx.badge("Instrument views", variant="soft", color_scheme="blue"),
                rx.badge("Responsive layout", variant="soft", color_scheme="green"),
                wrap="wrap",
                spacing="2",
                width="100%",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
    )


def bass_beat_cell(beat_label: str, note_value, role_value, role_color) -> rx.Component:
    return inner_panel(
        rx.vstack(
            rx.badge(beat_label, variant="soft", color_scheme="gray"),
            rx.text(note_value, font_size="1.0rem", font_weight="700", font_family="Consolas, 'Courier New', monospace"),
            rx.badge(role_value, variant="soft", color_scheme=role_color),
            spacing="1",
            align_items="start",
            width="100%",
        ),
        padding="0.75rem",
        min_height="0",
        width="100%",
    )


def bass_bar_card(bar) -> rx.Component:
    return inner_panel(
        rx.vstack(
            rx.hstack(
                rx.badge(bar["bar_title"], color_scheme="amber", variant="soft"),
                rx.heading(bar["chord_label"], size="3"),
                justify="between",
                width="100%",
            ),
            rx.grid(
                bass_beat_cell("Beat 1", bar["beat_one_note"], bar["beat_one_role"], bar["beat_one_color"]),
                bass_beat_cell("Beat 2", bar["beat_two_note"], bar["beat_two_role"], bar["beat_two_color"]),
                bass_beat_cell("Beat 3", bar["beat_three_note"], bar["beat_three_role"], bar["beat_three_color"]),
                bass_beat_cell("Beat 4", bar["beat_four_note"], bar["beat_four_role"], bar["beat_four_color"]),
                columns=rx.breakpoints(initial="2", xl="4"),
                    spacing="1",
                width="100%",
            ),
            inner_panel(
                rx.text(bar["bar_comment"], color=MUTED_TEXT, font_size="0.88rem", line_height="1.45"),
                background="rgba(2,6,23,0.36)",
                padding="0.75rem",
            ),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        background="rgba(2,6,23,0.22)",
            padding="0.6rem",
    )


def bass_preview() -> rx.Component:
    return surface_card(
        rx.vstack(
            section_header("Bass Preview", "Walking line"),
            rx.cond(
                AppState.can_export_midi,
                rx.vstack(
                    rx.hstack(
                        rx.badge(AppState.bass_note_count_text, variant="soft"),
                        rx.badge(AppState.bass_range_text, variant="soft"),
                        rx.badge(AppState.bass_motion_text, variant="soft"),
                        wrap="wrap",
                        spacing="2",
                        width="100%",
                    ),
                    inner_panel(
                        rx.vstack(
                            rx.badge("Kako da čitaš", color_scheme="blue", variant="soft"),
                            rx.text(
                                "Svaki takt pokazuje redosled nota kroz četiri dobe, njihovu harmonsku ulogu i kratko objašnjenje zašto linija tako funkcioniše.",
                                color=SUBTLE_TEXT,
                                font_size="0.82rem",
                                line_height="1.55",
                            ),
                            spacing="2",
                            align_items="start",
                            width="100%",
                        ),
                    ),
                    rx.grid(
                        rx.foreach(AppState.bass_bar_overview, bass_bar_card),
                        columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                        spacing="3",
                        width="100%",
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
                rx.cond(
                    AppState.is_processing,
                    processing_panel(
                        "Generišem bass liniju",
                        "Čim walking line bude spreman, ovde će se pojaviti taktovi, note po dobama i kratka objašnjenja njihove funkcije.",
                    ),
                    rx.text("Posle generisanja bass linije, ovde će se pojaviti notacija i pregled po taktovima sa funkcijom svakog tona.", color="gray"),
                ),
            ),
            align_items="start",
            spacing="3",
        ),
        width="100%",
    )


def guitar_neck_card() -> rx.Component:
    return surface_card(
        rx.vstack(
            section_header("Vrata Gitare", "Voicing pregled"),
            rx.cond(
                AppState.can_export_midi,
                rx.grid(
                    rx.foreach(
                        AppState.guitar_voicings,
                        lambda voicing: inner_panel(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading(voicing["chord"], size="4"),
                                    rx.badge(voicing["shape"], color_scheme="amber"),
                                    rx.badge(voicing["fret_range"], variant="soft"),
                                    spacing="2",
                                    wrap="wrap",
                                    width="100%",
                                ),
                                inner_panel(
                                    rx.text(
                                        voicing["neck_text"],
                                        font_family="Consolas, 'Courier New', monospace",
                                        white_space="pre",
                                        line_height="1.2",
                                        width="max-content",
                                        min_width="100%",
                                    ),
                                    background="rgba(2,6,23,0.28)",
                                    padding="0.5rem 0.6rem",
                                    overflow_x="auto",
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            width="100%",
                        ),
                    ),
                    columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                    spacing="2",
                    width="100%",
                ),
                rx.cond(
                    AppState.is_processing,
                    processing_panel(
                        "Računam gitarske voicing-e",
                        "Kada harmonski engine završi obradu, ovde će se pojaviti konkretni shape-ovi i ASCII pregled vrata gitare.",
                    ),
                    inner_panel(
                        rx.text("Analiza progresije će ovde prikazati voicinge preko vrata gitare.", color=MUTED_TEXT),
                        background="rgba(2,6,23,0.20)",
                    ),
                ),
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
    )


def django_response_card() -> rx.Component:
    return surface_card(
        rx.vstack(
            rx.hstack(
                rx.heading("AI Notes", size="5"),
                rx.cond(AppState.llm_model_used != "", rx.badge(AppState.llm_model_used, color_scheme="amber", variant="soft")),
                justify="between",
                width="100%",
            ),
            rx.cond(
                AppState.llm_analysis != "",
                rx.flex(
                    rx.box(
                        rx.vstack(
                            rx.cond(AppState.offline_mode, rx.badge("Offline mode", color_scheme="orange")),
                            rx.text(AppState.llm_analysis, line_height="1.75"),
                            spacing="2",
                            align_items="start",
                            width="100%",
                        ),
                        flex="2 1 520px",
                        min_width="0",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.cond(
                                AppState.llm_suggestions.length() > 0,
                                inner_panel(
                                    rx.vstack(
                                        rx.badge("Preporuke", color_scheme="amber", variant="soft"),
                                        rx.foreach(AppState.llm_suggestions, lambda suggestion: rx.text("- " + suggestion, line_height="1.55")),
                                        spacing="2",
                                        align_items="start",
                                        width="100%",
                                    ),
                                    background="rgba(245,158,11,0.07)",
                                    border="1px solid rgba(245,158,11,0.18)",
                                    padding="1rem",
                                ),
                            ),
                            rx.cond(
                                AppState.llm_socratic_prompts.length() > 0,
                                inner_panel(
                                    rx.vstack(
                                        rx.badge("Sokratska pitanja", color_scheme="blue", variant="soft"),
                                        rx.foreach(
                                            AppState.llm_socratic_prompts,
                                            lambda prompt: rx.box(
                                                rx.text(prompt, line_height="1.6", white_space="pre-wrap"),
                                                background="rgba(2,6,23,0.22)",
                                                border="1px solid rgba(148,163,184,0.14)",
                                                border_radius="14px",
                                                padding="0.85rem",
                                                width="100%",
                                            ),
                                        ),
                                        spacing="2",
                                        align_items="start",
                                        width="100%",
                                    ),
                                    background="rgba(59,130,246,0.07)",
                                    border="1px solid rgba(59,130,246,0.18)",
                                    padding="1rem",
                                ),
                            ),
                            rx.cond(
                                AppState.llm_next_steps != "",
                                inner_panel(
                                    rx.vstack(
                                        rx.badge("Sledeći koraci", color_scheme="green", variant="soft"),
                                        rx.text(AppState.llm_next_steps, white_space="pre-wrap", line_height="1.55"),
                                        spacing="2",
                                        align_items="start",
                                        width="100%",
                                    ),
                                    background="rgba(34,197,94,0.07)",
                                    border="1px solid rgba(34,197,94,0.18)",
                                    padding="1rem",
                                ),
                            ),
                            spacing="3",
                            align_items="start",
                            width="100%",
                        ),
                        flex="1 1 320px",
                        min_width="0",
                    ),
                    wrap="wrap",
                    gap="5",
                    align="start",
                    width="100%",
                ),
                rx.cond(
                    AppState.is_processing,
                    processing_panel(
                        "Čekam AI interpretaciju",
                        "Lokalna analiza se radi odmah, a LM Studio zatim dopunjava objašnjenje, preporuke i sledeće korake.",
                    ),
                    rx.text("Ovde će se pojaviti AI beleške i dodatna interpretacija kada analiza bude dostupna.", color=MUTED_TEXT),
                ),
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
        padding="1.5rem",
    )


def export_actions() -> rx.Component:
    return rx.hstack(
        rx.button(
            "Eksportuj MIDI",
            on_click=AppState.export_midi_file,
            disabled=AppState.can_export_midi == False,
        ),
        rx.button(
            "Kopiraj Suno Prompt",
            on_click=AppState.copy_suno_prompt,
            disabled=AppState.can_copy_suno_prompt == False,
        ),
        gap="3",
    )


def app_page() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute",
            inset="0",
            background=(
                "radial-gradient(circle at top left, rgba(245,158,11,0.10), transparent 26%), "
                "radial-gradient(circle at 80% 20%, rgba(59,130,246,0.12), transparent 24%)"
            ),
            pointer_events="none",
        ),
        rx.container(
            rx.vstack(
                chord_input(),
                analysis_workspace_header(),
                progression_snapshot_card(),
                rx.cond(AppState.selected_song_title != "", selected_song_card()),
                theory_lab_card(),
                guitar_neck_card(),
                bass_preview(),
                django_response_card(),
                analysis_actions_card(),
                rx.cond(AppState.is_processing, rx.spinner(size="3")),
                spacing="5",
                width="100%",
                padding_y="7",
            ),
            max_width=rx.breakpoints(initial="1460px", xl="1820px"),
            padding_x="1rem",
            position="relative",
            z_index="1",
        ),
        background=PAGE_BACKGROUND,
        min_height="100vh",
        width="100%",
        position="relative",
    )