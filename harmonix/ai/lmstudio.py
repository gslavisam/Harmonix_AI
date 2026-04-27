from __future__ import annotations

import base64
import json
import logging
import os
import re
from pathlib import Path
from typing import Any

from .prompts import DJANGO_SYSTEM_PROMPT
from harmonix.core.harmony import HarmonyParseError, parse_chord, parse_progression
from harmonix.services.notation_import import detect_notation_file_kind, normalize_progression_text, render_pdf_pages_to_png


logger = logging.getLogger(__name__)


def offline_message() -> str:
    return "Agent Django trenutno odmara (LLM nedostupan). Pokrenite LM Studio."


class LMStudioClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
        self.api_key = os.getenv("LMSTUDIO_API_KEY", "lm-studio")
        self.model = os.getenv("LMSTUDIO_MODEL", "").strip()
        self.timeout_seconds = float(os.getenv("LMSTUDIO_TIMEOUT_SECONDS", "30"))

    async def analyze_progression(self, progression: str, summary: dict[str, Any]) -> tuple[dict[str, Any], bool]:
        logger.info(f"[LM_STUDIO] analyze_progression START - progression='{progression}'")
        try:
            from openai import AsyncOpenAI
        except ImportError:
            logger.error("[LM_STUDIO] OpenAI async client nije dostupan (ImportError)")
            return self.fallback_response(summary), True

        logger.debug(f"[LM_STUDIO] Kreiram AsyncOpenAI klijent sa base_url={self.base_url}")
        client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout_seconds)
        logger.debug("[LM_STUDIO] Počinjem sa model resolution...")
        model_name = await self._resolve_model(client)
        logger.debug(f"[LM_STUDIO] Model resolved: {model_name}")
        user_prompt = self._build_user_prompt(progression, summary)
        logger.debug(f"[LM_STUDIO] User prompt built, length={len(user_prompt)}")
        received_response = False
        last_error: Exception | None = None

        try:
            logger.info(f"[LM_STUDIO] Šaljem zahtev ka analyze_progression (model={model_name})")
            response = await client.chat.completions.create(
                model=model_name,
                temperature=0.3,
                messages=[
                    {"role": "system", "content": DJANGO_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
            )
            received_response = True
            logger.info(f"[LM_STUDIO] Primljen odgovor - finish_reason={response.choices[0].finish_reason}")
            content = response.choices[0].message.content or "{}"
            logger.debug(f"[LM_STUDIO] Response content length: {len(content)} karaktera")
            parsed = self._parse_json_payload(content)
            logger.debug(f"[LM_STUDIO] Parsiran JSON - ključevi: {list(parsed.keys())}")
            result = self._normalize_response(parsed, summary, model_name)
            logger.info(f"[LM_STUDIO] analyze_progression ZAVRŠENA - model_used={result.get('model_used')}")
            return result, False
        except Exception as exc:
            logger.error(f"[LM_STUDIO] GREŠKA pri analyze_progression: {type(exc).__name__}: {exc}")
            last_error = exc

        if received_response:
            logger.error("[LM_STUDIO] Primljen je odgovor ali parse failed, vraćam invalid_response")
            return self.invalid_response(summary, model_name, last_error), False
        logger.error("[LM_STUDIO] Nema primljenog odgovora, vraćam fallback_response")
        return self.fallback_response(summary), True

    async def extract_progression_from_document(self, filename: str, file_bytes: bytes) -> tuple[dict[str, Any], bool]:
        logger.info(f"[LM_STUDIO] extract_progression_from_document START - filename={filename}, size={len(file_bytes)} bajtova")
        
        # Pokušaj importa
        try:
            logger.debug("[LM_STUDIO] [1/5] Pokušavam import AsyncOpenAI...")
            from openai import AsyncOpenAI
            logger.debug("[LM_STUDIO] [1/5] AsyncOpenAI import uspešan")
        except ImportError as e:
            logger.error(f"[LM_STUDIO] [1/5] IMPORTERROR: {e}")
            return self.fallback_document_response(filename), True
        except Exception as e:
            logger.error(f"[LM_STUDIO] [1/5] EXCEPTION during import: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"[LM_STUDIO] [1/5] Traceback: {traceback.format_exc()}")
            return self.fallback_document_response(filename), True

        # Kreiranja klijenta
        try:
            logger.debug(f"[LM_STUDIO] [2/5] Kreiram AsyncOpenAI klijent sa base_url={self.base_url}")
            client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url, timeout=self.timeout_seconds)
            logger.debug("[LM_STUDIO] [2/5] AsyncOpenAI klijent kreiran")
        except Exception as e:
            logger.error(f"[LM_STUDIO] [2/5] EXCEPTION during client creation: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"[LM_STUDIO] [2/5] Traceback: {traceback.format_exc()}")
            return self.fallback_document_response(filename, f"Klijent error: {e}"), True
        
        # Model resolution
        try:
            logger.debug("[LM_STUDIO] [3/5] Počinjem sa model resolution...")
            model_name = await self._resolve_model(client)
            logger.debug(f"[LM_STUDIO] [3/5] Model resolved: {model_name}")
        except Exception as e:
            logger.error(f"[LM_STUDIO] [3/5] EXCEPTION during model resolution: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"[LM_STUDIO] [3/5] Traceback: {traceback.format_exc()}")
            return self.fallback_document_response(filename, f"Model error: {e}"), True
        
        kind = detect_notation_file_kind(filename)
        logger.debug(f"[LM_STUDIO] [4/5] Tip fajla: {kind}")

        received_response = False
        last_error: Exception | None = None
        try:
            if kind == "pdf":
                logger.debug("[LM_STUDIO] [4/5] Renderujem PDF stranice...")
                try:
                    rendered_pages = render_pdf_pages_to_png(file_bytes)
                    logger.debug(f"[LM_STUDIO] [4/5] PDF renderovan - broj stranica: {len(rendered_pages)}")
                except Exception as e:
                    logger.error(f"[LM_STUDIO] [4/5] PDF render error: {type(e).__name__}: {e}")
                    import traceback
                    logger.error(f"[LM_STUDIO] [4/5] Traceback: {traceback.format_exc()}")
                    return self.fallback_document_response(filename, f"PDF error: {e}"), True
                    
                if not rendered_pages:
                    logger.warning("[LM_STUDIO] [4/5] PDF nije uspešno renderovan (no pages)")
                    return self.fallback_document_response(filename, "PDF nije uspešno pretvoren u preview stranice za LLM tumačenje."), True
                user_content = self._build_document_pdf_content(filename, rendered_pages)
                logger.debug(f"[LM_STUDIO] [4/5] PDF content built sa {len(rendered_pages)} slika")
            elif kind == "image":
                logger.debug("[LM_STUDIO] [4/5] Obrađujem sliku...")
                user_content = [
                    {"type": "text", "text": self._build_document_image_prompt(filename)},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": self._build_data_url(filename, file_bytes),
                        },
                    },
                ]
                logger.debug("[LM_STUDIO] [4/5] Image content built")
            else:
                logger.error(f"[LM_STUDIO] [4/5] Nepodržan tip fajla: {kind}")
                return self.fallback_document_response(filename, "Tip fajla nije podržan za ekstrakciju notacije."), True

            logger.info(f"[LM_STUDIO] [5/5] Počinjem HTTP zahtev ka LM Studio (model={model_name}, timeout={self.timeout_seconds}s)")
            attempt = 0
            for response_format in (self._build_document_json_schema(), None):
                attempt += 1
                logger.debug(f"[LM_STUDIO] [5/5] Pokušaj #{attempt}, response_format={'JSON_SCHEMA' if response_format else 'None'}")
                try:
                    request_kwargs: dict[str, Any] = {
                        "model": model_name,
                        "temperature": 0.2,
                        "messages": [
                            {"role": "system", "content": DJANGO_SYSTEM_PROMPT},
                            {
                                "role": "user",
                                "content": user_content,
                            },
                        ],
                    }
                    if response_format is not None:
                        request_kwargs["response_format"] = response_format
                    
                    logger.debug(f"[LM_STUDIO] [5/5] Šaljem zahtev...  (messages={len(request_kwargs['messages'])})")
                    response = await client.chat.completions.create(**request_kwargs)
                    received_response = True
                    logger.info(f"[LM_STUDIO] [5/5] Primljen odgovor od LM Studio - finish_reason={response.choices[0].finish_reason}")
                    
                    content = response.choices[0].message.content or "{}"
                    logger.debug(f"[LM_STUDIO] [5/5] Response content length: {len(content)} karaktera")
                    parsed = self._parse_json_payload(content)
                    logger.debug(f"[LM_STUDIO] [5/5] Parsiran JSON - ključevi: {list(parsed.keys())}")
                    
                    result = self._normalize_document_response(parsed, filename, model_name)
                    logger.info(f"[LM_STUDIO] [5/5] Rezultat: progression='{result.get('progression', '')}', model_used={result.get('model_used')}")
                    return result, False
                except Exception as exc:
                    last_error = exc
                    logger.warning(f"[LM_STUDIO] [5/5] Pokušaj #{attempt} FAILED: {type(exc).__name__}: {exc}")
                    import traceback
                    logger.debug(f"[LM_STUDIO] [5/5] Traceback: {traceback.format_exc()}")
                    continue

        except Exception as exc:
            last_error = exc
            logger.error(f"[LM_STUDIO] OUTER EXCEPTION: {type(exc).__name__}: {exc}")
            import traceback
            logger.error(f"[LM_STUDIO] Traceback: {traceback.format_exc()}")
            if received_response:
                logger.error(f"[LM_STUDIO] Vraćam invalid_document_response")
                return self.invalid_document_response(filename, model_name, exc), False
            logger.error(f"[LM_STUDIO] Vraćam fallback_document_response")
            return self.fallback_document_response(filename, str(exc)), True

        if received_response:
            logger.error(f"[LM_STUDIO] Svi pokušaji su failed, vraćam invalid_document_response")
            return self.invalid_document_response(filename, model_name, last_error), False
        logger.error(f"[LM_STUDIO] Nema primljenog odgovora, vraćam fallback_document_response")
        return self.fallback_document_response(filename, str(last_error) if last_error else None), True

    def fallback_response(self, summary: dict[str, Any]) -> dict[str, Any]:
        roots = ", ".join(summary.get("roots", [])) or "neodređen centar"
        questions = ["Koji akord u progresiji stvara najjači osećaj napetosti?"]
        guides = [
            f"Uporedi gde se napetost najduže zadržava i kako se potom razrešava prema centru {roots}; traži trenutak u kom bi melodija prirodno poželela da sleti.",
        ]
        return {
            "analysis": f"{offline_message()} Lokalna analiza je mapirala root tok: {roots}.",
            "suggestions": [
                "Pokrenite LM Studio za dublje teorijsko objašnjenje.",
                "Iskoristite lokalni bass preview i MIDI eksport za dalje vežbanje.",
            ],
            "socratic_questions": questions,
            "socratic_prompts": self._format_socratic_prompts(questions, guides, summary),
            "next_steps": "Pokrenite LM Studio i pokušajte ponovo za puni Django odgovor.",
            "tension_score": summary.get("tension_score", 0.0),
            "model_used": "offline",
        }

    def invalid_response(self, summary: dict[str, Any], model_name: str, error: Exception | None = None) -> dict[str, Any]:
        roots = ", ".join(summary.get("roots", [])) or "neodređen centar"
        detail = f" Model je odgovorio u formatu koji nije mogao potpuno da se parsira ({error})." if error else ""
        questions = ["Koje polje iz AI odgovora ti je najvažnije da sačuvamo i kada JSON nije savršen?"]
        guides = [
            f"Nemoj tražiti samo tehničku ispravnost; razmisli da li ti je važniji opis funkcije, osećaj napetosti ili put ka centru {roots}, pa odatle proceni šta model mora da sačuva.",
        ]
        return {
            "analysis": f"LM Studio je dostupan, ali je vratio neispravan JSON.{detail} Lokalna analiza i dalje daje root tok: {roots}.",
            "suggestions": [
                "Pojačaj striktan JSON output u promptu ili promeni model ako se ovo ponavlja.",
                "Proveri LM Studio log i raw content ako želiš tačan razlog parsiranja.",
            ],
            "socratic_questions": questions,
            "socratic_prompts": self._format_socratic_prompts(questions, guides, summary),
            "next_steps": "Aplikacija može da nastavi sa lokalnom analizom i bez punog AI JSON-a.",
            "tension_score": summary.get("tension_score", 0.0),
            "model_used": model_name,
        }

    def fallback_document_response(self, filename: str, reason: str | None = None) -> dict[str, Any]:
        note = "LM Studio nije uspeo da pročita notaciju." if not reason else f"LM Studio nije uspeo da pročita notaciju: {reason}"
        return {
            "progression": "",
            "title": Path(filename).stem or "Uploaded notation",
            "note": note,
            "source_excerpt": "",
            "model_used": "offline",
        }

    def invalid_document_response(self, filename: str, model_name: str, error: Exception | None = None) -> dict[str, Any]:
        reason = "LM Studio je odgovorio, ali JSON nije bio validan"
        if error:
            reason += f": {error}"
        return {
            "progression": "",
            "title": Path(filename).stem or "Uploaded notation",
            "note": reason,
            "source_excerpt": "",
            "model_used": model_name,
        }

    def _build_user_prompt(self, progression: str, summary: dict[str, Any]) -> str:
        song_reference = summary.get("song_reference")
        pattern_reference = summary.get("pattern_reference")
        context_lines = []
        if song_reference:
            context_lines.append(f"Referentna pesma: {song_reference}")
        if pattern_reference:
            context_lines.append(f"Pattern: {pattern_reference}")
        return (
            f"Progresija: {progression}\n"
            f"Lokalna analiza: {json.dumps(summary, ensure_ascii=False)}\n"
            + ("\n".join(context_lines) + "\n" if context_lines else "")
            + "Objasni progresiju, odredi formu isečka, tonalni centar i ključne kadence, "
            + "daj kratke preporuke za vežbu i postavi jedno ili dva sokratska pitanja. "
            + "Za svako pitanje dodaj i kratak vodeći odgovor koji ne zatvara temu, već usmerava korisnika šta da sluša, poredi ili proveri. "
            + "Vrati ta pitanja u polju socratic_questions, a vodeće odgovore u paralelnom polju socratic_guides. "
            + "Vrati isključivo validan JSON."
        )

    def _build_document_pdf_content(self, filename: str, rendered_pages: list[bytes]) -> list[dict[str, Any]]:
        content: list[dict[str, Any]] = [
            {
                "type": "text",
                "text": (
                    f"Dokument: {filename}. "
                    "Na slikama su preview stranice PDF lead sheet-a ili chord chart-a. "
                    "Protumači ih kao muzičku notaciju, prepoznaj naslov ako postoji i izdvoji harmoniju. "
                    "Vrati NORMALIZOVANU progresiju u polju progression kao akorde odvojene samo razmakom, bez taktovskih crta. "
                    "Vrati i polje harmony_text sa sirovim harmonijskim tekstom ili najbližim čitljivim nizom akorda kakav vidiš na dokumentu. "
                    "Ignoriši dekorativni tekst, tekst pesme i komentare. Ako harmonija nije čitljiva, ostavi progression kao prazan string i objasni razlog u note."
                ),
            }
        ]
        for page_index, page_bytes in enumerate(rendered_pages, start=1):
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": self._build_data_url(f"page-{page_index}.png", page_bytes),
                    },
                }
            )
        return content

    def _build_document_image_prompt(self, filename: str) -> str:
        return (
            f"Dokument: {filename}. "
            "Na slici je verovatno notacija, lead sheet ili chord chart. "
            "Pročitaj harmonijske oznake i izdvoji harmoniju. "
            "Vrati NORMALIZOVANU progresiju u polju progression kao akorde odvojene samo razmakom, bez taktovskih crta. "
            "Vrati i polje harmony_text sa sirovim harmonijskim tekstom ili najbližim čitljivim nizom akorda koji vidiš. "
            "Ako postoji naslov, vrati ga. Ignoriši dekorativni tekst i tekst pesme. "
            "Ako harmonija nije čitljiva, progression neka bude prazan string i razlog upiši u note."
        )

    def _normalize_response(self, payload: dict[str, Any], summary: dict[str, Any], model_name: str) -> dict[str, Any]:
        analysis_payload = payload.get("analysis")
        analysis_map = analysis_payload if isinstance(analysis_payload, dict) else {}
        if isinstance(analysis_payload, dict):
            analysis_parts = [
                analysis_map.get("description"),
                analysis_map.get("progression_explanation"),
                analysis_map.get("progression_description"),
                analysis_map.get("summary"),
                analysis_map.get("notes"),
            ]
            analysis_text = "\n".join(str(part).strip() for part in analysis_parts if part) or "Nema dodatnog objašnjenja."
        else:
            analysis_text = analysis_payload or payload.get("description") or payload.get("progression_explanation") or payload.get("explanation") or "Nema dodatnog objašnjenja."
        suggestions = self._coerce_string_list(payload.get("suggestions") or payload.get("practice_suggestions") or payload.get("practice_tips") or analysis_map.get("suggestions"))
        questions = self._coerce_string_list(payload.get("socratic_questions") or payload.get("questions"))
        socratic_prompts = self._coerce_socratic_prompt_cards(payload, analysis_map, questions, summary)
        cadential_map = self._coerce_string_list(payload.get("cadential_map") or payload.get("cadences") or payload.get("key_cadences") or analysis_map.get("key_cadences"))
        form_overview = payload.get("form_overview") or payload.get("form") or payload.get("structure") or analysis_map.get("form_identification") or ""
        tonal_center = payload.get("tonal_center") or payload.get("key_center") or payload.get("center") or ""
        if isinstance(analysis_payload, dict):
            form_overview = form_overview or analysis_payload.get("form") or analysis_payload.get("form_overview") or ""
            tonal_center = tonal_center or analysis_payload.get("tonal_center") or analysis_payload.get("center") or ""
            cadential_map = cadential_map or self._coerce_string_list(analysis_payload.get("cadences"))
        next_steps_payload = payload.get("next_steps", "Vežbaj progresiju u više tonaliteta.")
        if isinstance(next_steps_payload, list):
            next_steps_text = "\n".join(str(step).strip() for step in next_steps_payload if step)
        else:
            next_steps_text = str(next_steps_payload)
        raw_tension_score = payload.get("tension_score", summary.get("tension_score", 0.0))
        try:
            tension_score = float(raw_tension_score)
        except (TypeError, ValueError):
            tension_score = float(summary.get("tension_score", 0.0))
        return {
            "analysis": str(analysis_text),
            "suggestions": list(suggestions)[:3],
            "socratic_questions": list(questions)[:3],
            "socratic_prompts": socratic_prompts,
            "next_steps": next_steps_text,
            "tension_score": tension_score,
            "form_overview": str(form_overview),
            "tonal_center": str(tonal_center),
            "cadential_map": list(cadential_map)[:4],
            "model_used": model_name,
        }

    def _normalize_document_response(self, payload: dict[str, Any], filename: str, model_name: str) -> dict[str, Any]:
        progression = self._extract_document_progression(payload)
        title = str(payload.get("title") or Path(filename).stem or "Uploaded notation")
        raw_note = str(payload.get("note") or "").strip()
        source_excerpt = str(payload.get("source_excerpt") or "")
        if not progression:
            if raw_note and "izvučena iz uploadovanog dokumenta" not in raw_note.lower():
                note = raw_note
            else:
                note = "Model je odgovorio, ali nije vratio čitljivu progresiju u očekivanom formatu."
        elif not raw_note:
            note = "Progresija je izvučena iz uploadovanog dokumenta."
        else:
            note = raw_note
        return {
            "progression": progression,
            "title": title,
            "note": note,
            "source_excerpt": source_excerpt[:400],
            "model_used": model_name,
        }

    async def _resolve_model(self, client: Any) -> str:
        logger.debug(f"[LM_STUDIO] _resolve_model - self.model={self.model}")
        if self.model:
            logger.debug(f"[LM_STUDIO] Model iz env: {self.model}")
            return self.model
        try:
            logger.debug("[LM_STUDIO] Pozivam client.models.list()...")
            response = await client.models.list()
            logger.debug(f"[LM_STUDIO] Dobio sam modele - broj: {len(response.data)}")
            for model in response.data:
                model_id = getattr(model, "id", "")
                logger.debug(f"[LM_STUDIO] Proveravajući model: {model_id}")
                if model_id and "embedding" not in model_id.lower():
                    logger.info(f"[LM_STUDIO] Odabrao model: {model_id}")
                    return model_id
        except Exception as exc:
            logger.warning(f"[LM_STUDIO] Greška pri listanju modela: {type(exc).__name__}: {exc}")
            pass
        logger.info("[LM_STUDIO] Korišćenje fallback modela: gemma-4-e2b-it")
        return "gemma-4-e2b-it"

    def _parse_json_payload(self, content: str) -> dict[str, Any]:
        candidate = self._extract_json_candidate(content)
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            repaired = self._repair_json_payload(candidate)
            return json.loads(repaired)

    def _extract_json_candidate(self, content: str) -> str:
        stripped = content.strip()
        stripped = re.sub(r"^```json\s*", "", stripped, flags=re.IGNORECASE)
        stripped = re.sub(r"```$", "", stripped).strip()
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start != -1 and end != -1 and end > start:
            return stripped[start : end + 1]
        return stripped

    def _repair_json_payload(self, content: str) -> str:
        repaired = content.replace("\r\n", "\n")
        repaired = re.sub(r'(?<=")\s*\.\s*(?="\s*[^\"]+"\s*:)', ",\n", repaired)
        repaired = re.sub(r",(\s*[}\]])", r"\1", repaired)
        return repaired

    def _coerce_string_list(self, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]
        text = str(value).strip()
        return [text] if text else []

    def _extract_document_progression(self, payload: dict[str, Any]) -> str:
        candidate_fields = (
            payload.get("progression"),
            payload.get("normalized_progression"),
            payload.get("harmony_progression"),
            payload.get("harmony_text"),
            payload.get("extracted_progression"),
            payload.get("chord_progression"),
            payload.get("progression_text"),
            payload.get("changes"),
            payload.get("chords"),
            payload.get("source_excerpt"),
            payload.get("note"),
        )
        best_progression = ""
        for candidate in candidate_fields:
            progression = self._coerce_progression_candidate(candidate)
            if progression and self._count_progression_tokens(progression) > self._count_progression_tokens(best_progression):
                best_progression = progression

        for candidate in self._iter_document_candidates(payload):
            progression = self._coerce_progression_candidate(candidate)
            if progression and self._count_progression_tokens(progression) > self._count_progression_tokens(best_progression):
                best_progression = progression

        return best_progression

    def _coerce_progression_candidate(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, (list, tuple)):
            text = " ".join(str(item).strip() for item in value if str(item).strip())
        else:
            text = str(value).strip()
        if not text:
            return ""

        normalized = normalize_progression_text(text)
        if not normalized:
            return ""

        try:
            sequence = parse_progression(normalized)
            return " ".join(chord.label for chord in sequence.chords)
        except HarmonyParseError:
            recovered = self._extract_progression_tokens(normalized)
            if not recovered:
                return ""
            try:
                sequence = parse_progression(recovered)
            except HarmonyParseError:
                return recovered
            return " ".join(chord.label for chord in sequence.chords)

    def _extract_progression_tokens(self, text: str) -> str:
        tokens: list[str] = []
        for raw_token in text.split():
            token = raw_token.strip(",.;:()[]{}<>!?-–—−")
            if not token:
                continue
            try:
                chord = parse_chord(token)
            except HarmonyParseError:
                continue
            tokens.append(chord.label)
        return " ".join(tokens)

    def _iter_document_candidates(self, value: Any):
        if isinstance(value, dict):
            for item in value.values():
                yield from self._iter_document_candidates(item)
            return
        if isinstance(value, (list, tuple)):
            for item in value:
                yield from self._iter_document_candidates(item)
            return
        if isinstance(value, str):
            yield value

    def _count_progression_tokens(self, progression: str) -> int:
        return len([token for token in progression.split() if token])

    def _build_document_json_schema(self) -> dict[str, Any]:
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "notation_extraction",
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "progression": {"type": "string"},
                        "harmony_text": {"type": "string"},
                        "note": {"type": "string"},
                        "source_excerpt": {"type": "string"},
                    },
                    "required": ["title", "progression", "harmony_text", "note", "source_excerpt"],
                    "additionalProperties": False,
                },
            },
        }

    def _coerce_socratic_prompt_cards(
        self,
        payload: dict[str, Any],
        analysis_map: dict[str, Any],
        questions: list[str],
        summary: dict[str, Any],
    ) -> list[str]:
        prompt_payload = payload.get("socratic_prompts") or payload.get("socratic_pairs") or analysis_map.get("socratic_prompts")
        cards: list[str] = []
        if isinstance(prompt_payload, (list, tuple)):
            for item in prompt_payload:
                if isinstance(item, dict):
                    question = str(item.get("question") or item.get("prompt") or "").strip()
                    guide = str(item.get("answer") or item.get("guide") or item.get("hint") or "").strip()
                    if question:
                        cards.append(self._format_socratic_card(question, guide or self._fallback_socratic_guide(question, summary)))
                else:
                    text = str(item).strip()
                    if text:
                        cards.append(text)
        if cards:
            return cards[:3]

        guides = self._coerce_string_list(
            payload.get("socratic_guides")
            or payload.get("socratic_answers")
            or payload.get("question_guides")
            or analysis_map.get("socratic_guides")
        )
        return self._format_socratic_prompts(questions, guides, summary)

    def _format_socratic_prompts(self, questions: list[str], guides: list[str], summary: dict[str, Any]) -> list[str]:
        cards: list[str] = []
        for index, question in enumerate(questions[:3]):
            guide = guides[index] if index < len(guides) and guides[index].strip() else self._fallback_socratic_guide(question, summary)
            cards.append(self._format_socratic_card(question, guide))
        return cards

    def _format_socratic_card(self, question: str, guide: str) -> str:
        return f"Pitanje: {question}\nOdgovor koji vodi dalje: {guide}"

    def _fallback_socratic_guide(self, question: str, summary: dict[str, Any]) -> str:
        lowered = question.lower()
        roots = ", ".join(summary.get("roots", [])) or "tonalni centar"
        cadences = self._coerce_string_list(summary.get("local_cadences"))
        cadence_hint = cadences[0] if cadences else "glavni trenutak razrešenja"

        if "napet" in lowered or "tenz" in lowered:
            return f"Slušaj koji akord najduže odlaže smirenje, pa prati kako se razrešava prema {roots}; probaj da otpevaš notu koja tom akordu najviše " + '"traži"' + " sledeći korak."
        if "tonal" in lowered or "centar" in lowered or "dom" in lowered:
            return f"Uporedi više kandidata za centar, ali posebno proveri gde progresija zvuči kao da se vraća kući; često će ti {cadence_hint} pokazati zašto baš {roots} deluje stabilno."
        if "bas" in lowered:
            return "Pevaj samo donji glas kroz celu progresiju i obrati pažnju gde linija ide stepeno, a gde skače; baš ti prelomi otkrivaju zašto bass vodi harmoniju na određeni način."
        return f"Nemoj žuriti ka konačnom odgovoru; uzmi jedno slušanje za funkciju, drugo za bass, a treće za melodijsko očekivanje, pa proveri kako svaki ugao menja tvoj utisak o centru {roots}."

    def _build_data_url(self, filename: str, file_bytes: bytes) -> str:
        suffix = Path(filename).suffix.lower()
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }
        mime_type = mime_map.get(suffix, "application/octet-stream")
        encoded = base64.b64encode(file_bytes).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"