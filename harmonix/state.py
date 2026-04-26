from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import reflex as rx

from harmonix.ai.lmstudio import LMStudioClient
from harmonix.ai.prompts import SunoPrompt
from harmonix.core.bass import BassNote, build_bass_bar_overview, generate_walking_bass, midi_to_name
from harmonix.core.guitar import build_notation_display, build_progression_voicings
from harmonix.core.harmony import HarmonyParseError, analyze_progression, parse_progression
from harmonix.core.midi import export_midi
from harmonix.core.progression_presets import build_progression_catalog, build_progression_from_pattern, build_song_example_catalog
from harmonix.core.song_analysis import build_bass_harmonic_summary, build_form_overview, detect_key_cadences, infer_tonal_center
from harmonix.core.theory_library import build_bass_theory_sections, build_theory_profile
from harmonix.services.notation_import import default_notation_title, store_uploaded_notation, validate_notation_upload


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

PROGRESSION_PRESETS = build_progression_catalog()
SONG_EXAMPLES = build_song_example_catalog()

CHORD_QUALITIES = {
    "maj7": "maj7",
    "m7": "m7",
    "7": "7",
    "m7b5": "m7b5",
    "dim7": "dim7",
}


class AppState(rx.State):
    chord_input: str = ""
    assistant_panel_tab: str = "progressions"
    selected_progression_category: str = PROGRESSION_PRESETS[0][0] if PROGRESSION_PRESETS else ""
    selected_song_category: str = SONG_EXAMPLES[0][0] if SONG_EXAMPLES else ""
    selected_preset_key: str = "C"
    selected_root: str = "C"
    selected_quality: str = "maj7"
    selected_song_title: str = ""
    selected_song_artist: str = ""
    selected_song_pattern: str = ""
    selected_song_note: str = ""
    current_pattern_key: str = ""
    uploaded_notation_filename: str = ""
    uploaded_notation_status: str = ""
    uploaded_notation_error: str = ""
    uploaded_notation_excerpt: str = ""
    uploaded_notation_progression_preview: str = ""
    uploaded_notation_note: str = ""
    uploaded_notation_model_used: str = ""
    uploaded_notation_offline_mode: bool = False
    is_uploading_notation: bool = False
    uploaded_notation_path: str = ""
    tempo: int = 120
    validation_error: str = ""
    is_processing: bool = False
    analysis_status_text: str = ""
    parsed_chords: list[str] = []
    bass_notes: list[BassNote] = []
    bass_note_count_text: str = ""
    bass_range_text: str = ""
    bass_motion_text: str = ""
    bass_bar_overview: list[dict] = []
    guitar_voicings: list[dict] = []
    notation_notes: list[dict] = []
    notation_width: str = "640px"
    notation_text: str = ""
    analysis_form_text: str = ""
    analysis_tonal_center_text: str = ""
    analysis_cadence_items: list[str] = []
    analysis_bass_harmony_text: str = ""
    analysis_roots_text: str = ""
    analysis_tension_text: str = ""
    analysis_turnaround_text: str = ""
    theory_title: str = ""
    theory_overview: str = ""
    theory_sections: list[dict[str, str]] = []
    theory_resource_hint: str = ""
    llm_result: dict = {}
    llm_model_used: str = ""
    llm_analysis: str = ""
    llm_suggestions: list[str] = []
    llm_questions: list[str] = []
    llm_socratic_prompts: list[str] = []
    llm_next_steps: str = ""
    offline_mode: bool = False
    can_export_midi: bool = False
    can_copy_suno_prompt: bool = False
    midi_export_path: str = ""
    suno_prompt_text: str = ""

    def validate_input(self, value: str) -> None:
        self._apply_progression_input(value)

    def track_notation_upload_progress(self, progress: dict[str, int | float | bool]) -> None:
        self.assistant_panel_tab = "upload"
        self.is_uploading_notation = True
        self.uploaded_notation_error = ""
        self.uploaded_notation_excerpt = ""
        self.uploaded_notation_progression_preview = ""
        self.uploaded_notation_note = ""
        self.uploaded_notation_model_used = ""
        self.uploaded_notation_offline_mode = False
        ratio = float(progress.get("progress", 0.0) or 0.0)
        percent = max(0, min(100, int(ratio * 100)))
        if percent >= 100:
            self.uploaded_notation_status = "Upload završen. Backend priprema dokument za LM Studio..."
        elif percent > 0:
            self.uploaded_notation_status = f"Uploadujem dokument... {percent}%"
        else:
            self.uploaded_notation_status = "Pokrećem upload i pripremam dokument za obradu..."

    def set_assistant_panel_tab(self, tab: str) -> None:
        self.assistant_panel_tab = tab

    def set_selected_preset_key(self, root: str) -> None:
        self.selected_preset_key = root

    def set_selected_progression_category(self, category: str) -> None:
        self.selected_progression_category = category

    def set_selected_song_category(self, category: str) -> None:
        self.selected_song_category = category

    def apply_preset(self, pattern_key: str) -> None:
        self.assistant_panel_tab = "progressions"
        self.validate_input(build_progression_from_pattern(pattern_key, self.selected_preset_key))
        self.current_pattern_key = pattern_key

    def _select_song_example(
        self,
        title: str,
        artist: str,
        pattern_label: str,
        pattern_key: str,
        note: str,
        progression: str,
    ) -> None:
        self.assistant_panel_tab = "songs"
        self.selected_song_title = title
        self.selected_song_artist = artist
        self.selected_song_pattern = pattern_label
        self.selected_song_note = note
        self._apply_progression_input(progression, preserve_song_context=True)
        self.current_pattern_key = pattern_key

    @rx.event
    def load_song_example(
        self,
        title: str,
        artist: str,
        pattern_label: str,
        pattern_key: str,
        note: str,
        progression: str,
    ) -> None:
        self._select_song_example(title, artist, pattern_label, pattern_key, note, progression)

    @rx.event
    async def handle_notation_upload(self, files: list[rx.UploadFile]):
        logger.debug(f"[NOTATION_UPLOAD] Početak handle_notation_upload, fajlova primljeno: {len(files) if files else 0}")
        
        if not files:
            logger.warning("[NOTATION_UPLOAD] Nema fajlova za obradu")
            self.is_uploading_notation = False
            self.uploaded_notation_error = "Izaberi PDF ili sliku pre pokretanja analize."
            self.uploaded_notation_status = ""
            self.uploaded_notation_excerpt = ""
            self.uploaded_notation_progression_preview = ""
            self.uploaded_notation_note = ""
            self.uploaded_notation_model_used = ""
            self.uploaded_notation_offline_mode = False
            return

        self.assistant_panel_tab = "upload"
        self.is_uploading_notation = True
        self.uploaded_notation_error = ""
        self.uploaded_notation_status = "Čitam uploadovani dokument..."
        logger.debug("[NOTATION_UPLOAD] Postavljam UI u 'uploading' stanje")
        yield

        try:
            file = files[0]
            logger.debug(f"[NOTATION_UPLOAD] Obradujem fajl: {file.filename}")
            self.uploaded_notation_filename = file.filename
            self.uploaded_notation_status = "Pripremam fajl za čitanje..."
            yield

            logger.debug(f"[NOTATION_UPLOAD] Čitam file bytes iz: {file.filename}")
            file_bytes = await file.read()
            logger.debug(f"[NOTATION_UPLOAD] Pročitano {len(file_bytes)} bajtova")
            
            logger.debug("[NOTATION_UPLOAD] Validiram fajl...")
            validation_error = validate_notation_upload(file.filename, file_bytes)
            if validation_error:
                logger.error(f"[NOTATION_UPLOAD] Greška pri validaciji: {validation_error}")
                self.uploaded_notation_error = validation_error
                self.uploaded_notation_status = ""
                return
            logger.debug("[NOTATION_UPLOAD] Validacija prošla uspešno")

            logger.debug("[NOTATION_UPLOAD] Čuvam notaciju na disk...")
            self.uploaded_notation_path = store_uploaded_notation(file_bytes, file.filename)
            logger.debug(f"[NOTATION_UPLOAD] Notacija sačuvana na: {self.uploaded_notation_path}")
            self.uploaded_notation_status = "Šaljem dokument LM Studio modelu i čekam odgovor..."
            logger.debug("[NOTATION_UPLOAD] Yield #1 - pre poziva LMStudioClient")
            yield

            logger.info(f"[NOTATION_UPLOAD] Pozivam LMStudioClient.extract_progression_from_document za {file.filename}")
            result, offline_mode = await LMStudioClient().extract_progression_from_document(file.filename, file_bytes)
            logger.debug(f"[NOTATION_UPLOAD] Odgovor od LM Studio: offline_mode={offline_mode}, result keys={list(result.keys())}")
            logger.debug(f"[NOTATION_UPLOAD] Result sadržaj: {result}")
            
            extracted_progression = (result.get("progression") or "").strip()
            logger.debug(f"[NOTATION_UPLOAD] Ekstraktovana progresija: '{extracted_progression}'")
            
            self.uploaded_notation_excerpt = result.get("source_excerpt", "")
            self.uploaded_notation_progression_preview = extracted_progression
            self.uploaded_notation_note = result.get("note", "")
            self.uploaded_notation_model_used = result.get("model_used", "")
            self.uploaded_notation_offline_mode = offline_mode
            self.offline_mode = offline_mode
            self.llm_model_used = result.get("model_used", "")
            logger.debug(f"[NOTATION_UPLOAD] UI state ažuriran - model_used: {self.uploaded_notation_model_used}")
            logger.debug("[NOTATION_UPLOAD] Yield #2 - nakon ažuriranja UI state-a")
            yield

            if not extracted_progression:
                logger.warning(f"[NOTATION_UPLOAD] Progresija nije pronađena: {self.uploaded_notation_note}")
                self.uploaded_notation_error = result.get("note", "Nije pronađena čitljiva progresija u dokumentu.")
                self.uploaded_notation_status = ""
                self.uploaded_notation_progression_preview = ""
                logger.debug("[NOTATION_UPLOAD] Yield #3 - progresija nije pronađena, vraćam")
                yield
                return

            logger.debug("[NOTATION_UPLOAD] Progresija pronađena, primenjujem na input")
            title = result.get("title") or default_notation_title(file.filename)
            note = result.get("note") or "Progresija je učitana iz uploadovane notacije."
            self.selected_song_title = title
            self.selected_song_artist = "Uploaded notation"
            self.selected_song_pattern = "Notation import"
            self.selected_song_note = note
            self.uploaded_notation_status = f"Progresija izvučena preko modela {result.get('model_used', 'offline')}. Pokrećem analizu..."
            
            logger.debug(f"[NOTATION_UPLOAD] Primenjujem progresiju: {extracted_progression}")
            self._apply_progression_input(extracted_progression, preserve_song_context=True)
            yield
            
            logger.info("[NOTATION_UPLOAD] Pokrećem analyze_and_generate()")
            analysis_count = 0
            async for event in self.analyze_and_generate():
                analysis_count += 1
                logger.debug(f"[NOTATION_UPLOAD] Analiza event #{analysis_count}")
                yield event
            logger.info(f"[NOTATION_UPLOAD] analyze_and_generate() završena, {analysis_count} eventa")
            
            self.uploaded_notation_status = "Upload je pročitan i progresija je analizirana."
            logger.info("[NOTATION_UPLOAD] Upload notacije ZAVRŠEN USPEŠNO")
        except Exception as exc:
            logger.exception(f"[NOTATION_UPLOAD] GREŠKA pri obradi: {exc}")
            self.uploaded_notation_error = f"Upload notacije nije uspeo: {exc}"
            self.uploaded_notation_status = ""
        finally:
            self.is_uploading_notation = False
            logger.debug("[NOTATION_UPLOAD] Završavanje - is_uploading_notation set na False")

    @rx.event
    async def analyze_song_example(
        self,
        title: str,
        artist: str,
        pattern_label: str,
        pattern_key: str,
        note: str,
        progression: str,
    ) -> None:
        self._select_song_example(title, artist, pattern_label, pattern_key, note, progression)
        async for event in self.analyze_and_generate():
            yield event

    def set_selected_root(self, root: str) -> None:
        self.selected_root = root

    def set_selected_quality(self, quality: str) -> None:
        self.selected_quality = quality

    def append_selected_chord(self) -> None:
        self.assistant_panel_tab = "builder"
        quality_suffix = CHORD_QUALITIES.get(self.selected_quality, self.selected_quality)
        token = f"{self.selected_root}{quality_suffix}"
        next_value = f"{self.chord_input} {token}".strip()
        self.validate_input(next_value)

    def clear_progression_input(self) -> None:
        self.validate_input("")

    def set_tempo(self, value: str) -> None:
        parsed_value = int(value or 120)
        self.tempo = max(40, min(320, parsed_value))

    @rx.event
    async def analyze_and_generate(self) -> None:
        logger.info(f"[ANALYZE] Početak analyze_and_generate sa chord_input: '{self.chord_input}'")
        if not self.chord_input.strip():
            logger.warning("[ANALYZE] chord_input je prazan")
            self.validation_error = "Unesi progresiju pre analize."
            self.analysis_status_text = ""
            return

        try:
            logger.debug("[ANALYZE] Parsujem progresiju...")
            sequence = parse_progression(self.chord_input)
            logger.debug(f"[ANALYZE] Progresija parsovana uspešno: {len(sequence.chords)} akorda")
        except HarmonyParseError as exc:
            logger.error(f"[ANALYZE] Parse error: {exc}")
            self.validation_error = str(exc)
            self.analysis_status_text = ""
            return

        self.is_processing = True
        self.validation_error = ""
        self.analysis_status_text = "Pokrećem analizu i pripremam rezultate..."
        self._reset_generated_outputs()
        logger.debug("[ANALYZE] Postavljam is_processing=True i resetujem output")
        yield

        try:
            logger.debug("[ANALYZE] Startam parallel tasks...")
            summary = analyze_progression(sequence)
            logger.debug(f"[ANALYZE] Analiza završena - roots={summary.roots}")
            local_form_text = build_form_overview(self.selected_song_pattern, len(summary.chord_labels))
            local_tonal_center = infer_tonal_center(sequence)
            local_cadences = detect_key_cadences(sequence, self.selected_song_pattern)
            theory_profile = build_theory_profile(
                self.current_pattern_key,
                self.selected_song_pattern,
                local_cadences,
                sequence,
            )
            self.theory_title = str(theory_profile.get("title") or "")
            self.theory_overview = str(theory_profile.get("overview") or "")
            self.theory_sections = list(theory_profile.get("sections") or [])
            self.theory_resource_hint = str(theory_profile.get("resource_hint") or "")
            self.analysis_status_text = "Računam walking bass, voicing-e i AI interpretaciju..."
            logger.debug("[ANALYZE] Lokalna analiza završena, startam bass i LLM tasks...")
            yield

            bass_task = asyncio.to_thread(generate_walking_bass, sequence, self.tempo)
            llm_summary = {
                "roots": summary.roots,
                "tension_score": summary.tension_score,
                "contains_turnaround": summary.contains_turnaround,
                "local_form": local_form_text,
                "local_tonal_center": local_tonal_center,
                "local_cadences": local_cadences,
            }
            if self.selected_song_title:
                llm_summary["song_reference"] = f"{self.selected_song_title} - {self.selected_song_artist}"
                llm_summary["pattern_reference"] = self.selected_song_pattern
            logger.debug("[ANALYZE] LLM summary pripremljen")
            
            logger.info("[ANALYZE] Pozivam LMStudioClient.analyze_progression()...")
            llm_task = LMStudioClient().analyze_progression(
                self.chord_input,
                llm_summary,
            )
            logger.debug("[ANALYZE] Čekam bass_task i llm_task...")
            bass_notes, (llm_result, offline_mode) = await asyncio.gather(bass_task, llm_task)
            logger.info(f"[ANALYZE] Oba taska završena - bass_notes={len(bass_notes)}, offline_mode={offline_mode}")
            self.analysis_status_text = "Finalizujem prikaz i ažuriram kartice..."
            voicings = build_progression_voicings(sequence)
            notation_display = build_notation_display(bass_notes)

            self.parsed_chords = summary.chord_labels
            self.bass_notes = bass_notes
            self.bass_note_count_text = f"{len(bass_notes)} note line"
            self.bass_range_text = self._build_bass_range_text(bass_notes)
            self.bass_motion_text = f"{len(summary.chord_labels)} bars, roots: {', '.join(summary.roots)}"
            self.bass_bar_overview = build_bass_bar_overview(bass_notes)
            self.theory_sections = self.theory_sections + build_bass_theory_sections(
                sequence,
                self.bass_bar_overview,
                local_cadences,
                self.current_pattern_key,
            )
            self.guitar_voicings = voicings
            self.notation_notes = notation_display["notes"]
            self.notation_width = notation_display["width"]
            self.notation_text = notation_display["staff_text"]
            self.analysis_form_text = str(llm_result.get("form_overview") or local_form_text)
            self.analysis_tonal_center_text = str(llm_result.get("tonal_center") or local_tonal_center)
            self.analysis_cadence_items = list(llm_result.get("cadential_map") or local_cadences)
            self.analysis_bass_harmony_text = build_bass_harmonic_summary(
                self.bass_bar_overview,
                self.analysis_tonal_center_text,
                self.analysis_cadence_items,
                summary.contains_turnaround,
            )
            self.analysis_roots_text = ", ".join(summary.roots)
            self.analysis_tension_text = f"Tension score {summary.tension_score:.2f}"
            self.analysis_turnaround_text = "Sadrži turnaround" if summary.contains_turnaround else "Bez jasnog turnaround-a"
            self.llm_result = llm_result
            self.llm_model_used = llm_result.get("model_used", "")
            self.llm_analysis = llm_result.get("analysis", "")
            self.llm_suggestions = llm_result.get("suggestions", [])
            self.llm_questions = llm_result.get("socratic_questions", [])
            self.llm_socratic_prompts = llm_result.get("socratic_prompts", [])
            self.llm_next_steps = llm_result.get("next_steps", "")
            self.offline_mode = offline_mode
            self.can_export_midi = bool(bass_notes)
            self.suno_prompt_text = SunoPrompt.from_analysis({"suggested_tempo": self.tempo}).generate(self.chord_input)
            self.can_copy_suno_prompt = bool(self.suno_prompt_text)
            logger.info("[ANALYZE] Sve rezultate su ažurirane - analiza ZAVRŠENA USPEŠNO")
        except Exception as exc:
            logger.exception(f"[ANALYZE] GREŠKA pri analizi: {exc}")
            self.validation_error = f"Analiza nije uspela: {exc}"
        finally:
            self.analysis_status_text = ""
            self.is_processing = False
            logger.debug("[ANALYZE] Završavanje - is_processing=False")

    def export_midi_file(self) -> None:
        if not self.bass_notes:
            return
        output_path = Path("exports") / "harmonix_bass.mid"
        exported = export_midi(self.bass_notes, self.tempo, output_path)
        self.midi_export_path = str(exported)

    def copy_suno_prompt(self):
        if not self.suno_prompt_text:
            return
        return rx.set_clipboard(self.suno_prompt_text)

    def _reset_generated_outputs(self) -> None:
        self.bass_notes = []
        self.bass_note_count_text = ""
        self.bass_range_text = ""
        self.bass_motion_text = ""
        self.bass_bar_overview = []
        self.guitar_voicings = []
        self.notation_notes = []
        self.notation_width = "640px"
        self.notation_text = ""
        self.analysis_form_text = ""
        self.analysis_tonal_center_text = ""
        self.analysis_cadence_items = []
        self.analysis_bass_harmony_text = ""
        self.analysis_roots_text = ""
        self.analysis_tension_text = ""
        self.analysis_turnaround_text = ""
        self.theory_title = ""
        self.theory_overview = ""
        self.theory_sections = []
        self.theory_resource_hint = ""
        self.llm_result = {}
        self.llm_model_used = ""
        self.llm_analysis = ""
        self.llm_suggestions = []
        self.llm_questions = []
        self.llm_socratic_prompts = []
        self.llm_next_steps = ""
        self.offline_mode = False
        self.can_export_midi = False
        self.can_copy_suno_prompt = False
        self.midi_export_path = ""
        self.suno_prompt_text = ""

    def _apply_progression_input(self, value: str, preserve_song_context: bool = False) -> None:
        self.chord_input = value
        self._reset_generated_outputs()
        if not preserve_song_context:
            self._clear_song_context()
            self.current_pattern_key = ""
        if not value.strip():
            self.validation_error = ""
            self.parsed_chords = []
            return
        try:
            sequence = parse_progression(value)
        except HarmonyParseError as exc:
            self.validation_error = str(exc)
            self.parsed_chords = []
            self.can_export_midi = False
            self.can_copy_suno_prompt = False
            return

        self.validation_error = ""
        self.parsed_chords = [chord.label for chord in sequence.chords]

    def _clear_song_context(self) -> None:
        self.selected_song_title = ""
        self.selected_song_artist = ""
        self.selected_song_pattern = ""
        self.selected_song_note = ""

    def _build_bass_range_text(self, notes: list[BassNote]) -> str:
        if not notes:
            return ""
        lowest = min(notes, key=lambda note: note.pitch)
        highest = max(notes, key=lambda note: note.pitch)
        return f"{midi_to_name(lowest.pitch)} -> {midi_to_name(highest.pitch)}"