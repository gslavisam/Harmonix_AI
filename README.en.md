# Harmonix AI

Harmonix AI is a local-first jazz harmony assistant built with Python and Reflex. It combines a deterministic music engine with an optional LM Studio LLM layer for progression analysis, theory explanations, and notation ingest from PDF or image sources.

## What the app currently does

- analyzes manually entered chord progressions
- provides a `Known progressions` catalog with category selection through a compact dropdown
- provides a `Known songs` catalog with the same compact category selector
- supports `Chord Builder` for quick progression assembly
- supports `Upload notation` for LM Studio-based PDF and image ingest
- generates a bar-by-bar walking bass preview
- renders guitar voicings and ASCII fretboard diagrams
- shows `Song Analysis` for form, tonal center, cadences, and bass-to-harmony relationships
- shows `AI Notes` for interpretation, practice suggestions, next steps, and Socratic questions with guided answers
- shows `Theory Lab` for harmonic function, substitutions, common-practice context, and bass-line alternatives
- exports MIDI and generates a Suno prompt

Note: the old `Tablature` card has been removed from the current UI because it overlapped with the guitar and voicing views.

## Main entry flows

1. `Known progressions`
2. `Known songs`
3. `Chord Builder`
4. `Upload notation`

## Analysis outputs

After analysis runs, the app currently builds these outputs:

1. local harmonic analysis of the progression
2. walking bass line and per-bar overview
3. guitar voicings and fretboard view
4. `Song Analysis` for structural and functional summary
5. `AI Notes` for LLM interpretation and guided reflection
6. `Theory Lab` for theory context and alternative approaches

## Tech Stack

- Python 3.10+
- Reflex
- OpenAI-compatible client for LM Studio
- music21, mido, mingus
- PyMuPDF for PDF preview ingest

Recommended Windows runtime: Python 3.12.

## Local setup

### 1. Activate a virtual environment

If you are starting fresh:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If you are using the existing project environment that has already been validated with Harmonix:

```powershell
.\.venv312\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

For development and tests:

```powershell
pip install -r requirements-dev.txt
```

### 3. Configure `.env`

Copy `.env.example` to `.env` and adjust values as needed.

Minimal example:

```env
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_API_KEY=lm-studio
LMSTUDIO_MODEL=gemma-4
LMSTUDIO_TIMEOUT_SECONDS=30
```

The deterministic harmony workflow works without LM Studio. LM Studio is required for `AI Notes` and the `Upload notation` flow.

### 4. Run the app

```powershell
reflex run
```

Default addresses:

- frontend: http://localhost:3000
- backend: http://localhost:8000

## Running tests

```powershell
pytest
```

## Project structure

```text
Harmonix_AI/
├── harmonix/
│   ├── ai/
│   ├── core/
│   ├── services/
│   ├── ui/
│   ├── app.py
│   ├── harmonix.py
│   └── state.py
├── tests/
├── requirements.txt
├── requirements-dev.txt
├── rxconfig.py
├── spec.md
└── plan.md
```

## Key modules

- `harmonix/state.py` - main Reflex state and analysis workflow
- `harmonix/ui/components.py` - UI layout, entry panels, and result cards
- `harmonix/core/harmony.py` - chord parsing and core progression analysis
- `harmonix/core/song_analysis.py` - form, tonal center, cadences, and bass/harmony summaries
- `harmonix/core/bass.py` - walking bass generation and per-bar commentary
- `harmonix/core/guitar.py` - guitar voicings and visual guitar rendering
- `harmonix/core/theory_library.py` - `Theory Lab` knowledge profiles and bass alternatives
- `harmonix/ai/lmstudio.py` - LM Studio client and tolerant AI response parsing
- `harmonix/services/notation_import.py` - notation upload and preprocessing

## How the app works

1. the user chooses an entry flow or types a progression directly
2. the local parser validates and normalizes the input
3. form, tonal center, and key cadences are inferred
4. walking bass, voicings, and supporting visuals are generated
5. `Theory Lab` builds a local theory profile and bass alternatives
6. if LM Studio is available, `AI Notes` adds interpretation and guided reflection
7. the results are rendered in separate dashboard cards with clearer responsibility boundaries

## Troubleshooting

### LM Studio seems available, but `AI Notes` still look wrong or incomplete

The most common cause is near-valid JSON or markdown-fenced JSON. The project now includes a more tolerant parser, but if the model still returns malformed output, check the LM Studio log and the selected model.

### `reflex run` reports a compile or worker error

- verify the correct virtual environment is active
- for this project, `.venv312` is the validated local runtime for compile checks
- verify the Python version and installed dependencies

### `Analyze song` does not behave as expected

The `Known songs` flow now uses a shared internal selection helper before analysis. If behavior still looks off, verify that the chosen example populated `chord_input` correctly.

### The UI feels slow after clicking `Analyze and Generate`

The app shows in-progress status during analysis. If LM Studio responds slowly, the AI phase can still take several seconds.

## Public repo scope

The public GitHub repo is focused on the runnable application, core technical documentation, and setup. Internal planning notes and detailed product-spec documents are intentionally kept out of the public repository.

## Serbian README

The Serbian version is available in `README.md`.