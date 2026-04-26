# GitHub Publish Checklist

Koristi ovaj spisak pre prvog public push-a za `gslavisam/Harmonix_AI`.

## Pre publish-a

1. Proveri da li aplikacija prolazi lokalni compile kroz `.venv312`.
2. Proveri da `.gitignore` pokriva privatne i generisane fajlove.
3. Potvrdi da `README.md` i `README.en.md` opisuju javni scope projekta.
4. Potvrdi da `plan.md`, `spec.md`, `.env`, lokalni export-i i upload-i nisu deo commit-a.
5. Proveri da u root-u nema fajlova sa tajnama, tokenima ili privatnim dokumentima.

## Predlog javnog sadržaja repoa

Zadrži javno:

- `harmonix/`
- `tests/`
- `README.md`
- `README.en.md`
- `requirements.txt`
- `requirements-dev.txt`
- `pyproject.toml`
- `rxconfig.py`
- `.env.example`
- `.gitignore`

Nemoj publicovati:

- `.env`
- `plan.md`
- `spec.md`
- `dev_plan_ai_harmonix.xlsx`
- `exports/`
- `uploaded_files/`
- `data/documents/`
- `data/vectordb/`
- `.states/`, `.web/`, `__pycache__/`, `.pytest_cache/`
- lokalna virtuelna okruženja

## VS Code publish tok

1. Otvori `Harmonix_AI` kao aktivan workspace folder.
2. U Source Control panelu izaberi `Initialize Repository` ako repo još nije inicijalizovan.
3. Pregledaj listu fajlova za prvi commit i potvrdi da su ignorisani interni dokumenti zaista van staging-a.
4. Napravi prvi commit, na primer: `Initial public release`.
5. U VS Code GitHub integraciji izaberi `Publish to GitHub`.
6. Kao owner koristi `gslavisam`.
7. Kao ime repoa koristi `Harmonix_AI` ili `harmonix-ai` ako želiš standardizovanije ime.
8. Izaberi `Public repository`.
9. Posle publish-a proveri GitHub stranicu repoa i otvori `README.md` iz browsera.

## Posle publish-a

1. Dodaj kratak opis repoa na GitHub-u.
2. Dodaj topic tagove, na primer: `reflex`, `python`, `jazz`, `music-theory`, `lm-studio`.
3. Ako želiš, dodaj screenshot aplikacije u repozitorijum kroz poseban javni assets folder.
4. Tek posle prve objave razmisli o GitHub Releases ili demo videu.