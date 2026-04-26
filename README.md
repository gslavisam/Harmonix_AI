# Harmonix AI

Harmonix AI je local-first jazz harmony assistant napravljen u Python + Reflex stack-u. Aplikacija kombinuje deterministički muzički engine sa opcionim LM Studio LLM slojem za analizu progresija, teorijska objašnjenja i notation ingest iz PDF-a ili slike.

## Šta aplikacija trenutno radi

- analizira ručno unetu chord progresiju
- nudi katalog `Poznate progresije` sa klasifikacijama kroz dropdown izbor
- nudi katalog `Poznate pesme` sa istim kompaktnim izborom kategorije
- podržava `Chord Builder` za brzo sastavljanje progresije
- podržava `Upload notation` za LM Studio ingest PDF-a i slika
- generiše walking bass preview po taktovima
- prikazuje gitarske voicing-e i ASCII vrat gitare
- prikazuje `Song Analysis` sa formom, tonalnim centrom, kadencama i odnosom bass linije i harmonije
- prikazuje `AI Notes` sa interpretacijom, preporukama, sledećim koracima i sokratskim pitanjima sa vodećim odgovorima
- prikazuje `Theory Lab` sa funkcionalnom analizom, substitucijama, standardnom praksom i alternativama za bass line
- izvozi MIDI i generiše Suno prompt

Napomena: kartica `Tablatura` je uklonjena iz trenutnog UI-a jer je duplirala informacije koje su već bile pokrivene gitarom i voicing prikazima.

## Glavni ulazni tokovi

1. `Poznate progresije`
2. `Poznate pesme`
3. `Chord Builder`
4. `Upload notation`

## Rezultati analize

Posle pokretanja analize, aplikacija trenutno gradi sledeće izlaze:

1. lokalnu harmonijsku analizu progresije
2. walking bass liniju i pregled po taktovima
3. gitarske voicing-e i pregled vrata gitare
4. `Song Analysis` za strukturni i funkcionalni rezime
5. `AI Notes` za LLM interpretaciju i vođeno promišljanje
6. `Theory Lab` za teorijski kontekst i alternativne pristupe

## Tech Stack

- Python 3.10+
- Reflex
- OpenAI kompatibilan klijent za LM Studio
- music21, mido, mingus
- PyMuPDF za PDF preview ingest

Preporuka za Windows radno okruženje: Python 3.12.

## Pokretanje lokalno

### 1. Aktiviraj virtuelno okruženje

Ako krećeš od nule:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Ako koristiš postojeće projektno okruženje koje je provereno za Harmonix:

```powershell
.\.venv312\Scripts\Activate.ps1
```

### 2. Instaliraj zavisnosti

```powershell
pip install -r requirements.txt
```

Za razvoj i testove:

```powershell
pip install -r requirements-dev.txt
```

### 3. Konfiguriši `.env`

Kopiraj `.env.example` u `.env` i prilagodi vrednosti po potrebi.

Minimalan primer:

```env
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_API_KEY=lm-studio
LMSTUDIO_MODEL=gemma-4
LMSTUDIO_TIMEOUT_SECONDS=30
```

Osnovna harmonijska analiza radi i bez LM Studio. LM Studio je potreban za `AI Notes` i `Upload notation` tok.

### 4. Pokreni aplikaciju

```powershell
reflex run
```

Podrazumevane adrese:

- frontend: http://localhost:3000
- backend: http://localhost:8000

## Pokretanje testova

```powershell
pytest
```

## Struktura projekta

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

## Najvažniji moduli

- `harmonix/state.py` - glavni Reflex state i tok analize
- `harmonix/ui/components.py` - UI layout, input paneli i kartice rezultata
- `harmonix/core/harmony.py` - parsiranje i osnovna analiza progresije
- `harmonix/core/song_analysis.py` - forma, tonalni centar, kadence i rezime bass/harmonija
- `harmonix/core/bass.py` - walking bass generisanje i komentari po taktovima
- `harmonix/core/guitar.py` - voicing-i i vizuelni prikazi gitare
- `harmonix/core/theory_library.py` - `Theory Lab` znanje i bass alternativa objašnjenja
- `harmonix/ai/lmstudio.py` - LM Studio klijent i tolerantno parsiranje AI odgovora
- `harmonix/services/notation_import.py` - upload i priprema notacije

## Kako aplikacija radi

1. korisnik bira jedan od ulaznih tokova ili direktno unosi progresiju
2. lokalni parser validira akorde i normalizuje unos
3. izračunavaju se forma, tonalni centar i ključne kadence
4. generišu se walking bass, voicing-i i pomoćni vizuelni prikazi
5. `Theory Lab` gradi lokalni teorijski profil i bass alternative
6. ako je LM Studio dostupan, dodaje se `AI Notes` interpretacija
7. rezultat se prikazuje kroz odvojene dashboard kartice sa jasnom podelom odgovornosti

## Troubleshooting

### LM Studio izgleda dostupno, ali `AI Notes` ne izlazi kako treba

Najčešći razlog je da model vrati skoro-validan JSON ili markdown fenced JSON. Projekat sada ima tolerantniji parser za te slučajeve, ali ako model i dalje šalje loš format, proveri LM Studio log i model koji koristiš.

### `reflex run` prijavi compile ili worker error

- proveri da li je aktivno pravo virtuelno okruženje
- na ovom projektu je `.venv312` provereni runtime za lokalni compile
- proveri Python verziju i instalirane zavisnosti

### Dugme `Analiziraj pesmu` ne daje očekivan rezultat

Tok za `Poznate pesme` je prebačen na zajednički interni helper za izbor pesme i analizu. Ako nešto i dalje deluje čudno, proveri da li je `chord_input` zaista popunjen posle izbora primera.

### UI deluje sporo posle klika na `Analiziraj i Generiši`

Aplikacija prikazuje status obrade tokom analize. Ako LM Studio odgovara sporije, AI faza može trajati više sekundi.

## Javni repo fokus

Javni GitHub repo je fokusiran na runnable aplikaciju, osnovnu tehničku dokumentaciju i setup. Interni planning i detaljni product spec dokumenti nisu deo javnog repoa.

## English README

English version is available in `README.en.md`.