# Dijagnostika Upload Notation - Detaljno Logovanje

## Šta je urađeno?

Dodao sam **korak-po-korak logovanje** u celu Upload Notation funkcionalnost kako bi se videlo tačno gde se proces zaustavlja. Logovanje je dodano na sledećim tačkama:

### 1. **state.py** - `handle_notation_upload()` 
- Početak upload procesa
- Provera da li su fajlovi odabrani
- Čitanje file bytes-a
- Validacija fajla
- Poziv ka `LMStudioClient.extract_progression_from_document()`
- **KLJUČNO**: Provera da li je progresija ekstraktovana
- Primena progresije na input
- Poziv `analyze_and_generate()`
- Završetak procesa

### 2. **state.py** - `analyze_and_generate()`
- Validacija chord_input-a
- Parsovanje progresije
- Lokalna analiza
- **KLJUČNO**: Poziv `LMStudioClient.analyze_progression()`
- Čekanje da se kompletan AsyncIO gather završi
- Ažuriranje svih UI elemenata sa rezultatima

### 3. **lmstudio.py** - `extract_progression_from_document()`
- Kreiranja AsyncOpenAI klijenta
- **KLJUČNO**: `_resolve_model()` - pronalaženje dostupnog modela
- Detektovanje tipa fajla (PDF ili slike)
- Za PDF: renderovanje stranica
- Za slike: konverzija u data URL
- **KLJUČNO**: HTTP zahtev ka LM Studio
- Parsiranje JSON odgovora
- Normalizacija rezultata

### 4. **lmstudio.py** - `analyze_progression()`
- Kreiranja AsyncOpenAI klijenta
- Model resolution
- Izgradnja user prompt-a
- **KLJUČNO**: HTTP zahtev ka LM Studio za analizu
- Parsiranje JSON odgovora
- Normalizacija rezultata

### 5. **lmstudio.py** - `_resolve_model()`
- Provera environment varijable `LMSTUDIO_MODEL`
- Ako nije postavljena: poziva `client.models.list()`
- Filtrira modele da izbegne embedding modele
- Vraća prvi dostupan model ili fallback `gemma-4-e2b-it`

## Kako Čitati Logove?

Logovanje koristi format sa prefixima za lakšu identifikaciju:

```
[NOTATION_UPLOAD] - Glavne operacije u handle_notation_upload()
[LM_STUDIO]       - Operacije u LMStudioClient klasi
[ANALYZE]         - Operacije u analyze_and_generate()
```

Nivoi logovanja:
- `DEBUG` - Detaljne informacije za debugging
- `INFO` - Važne tačke u toku
- `WARNING` - Upozorenja (npr. nema modela)
- `ERROR` - Greške sa detalje
- `EXCEPTION` - Greške sa stack trace

## Gde Videti Logove?

Logovanje se ispisuje na **stdout** (konzola):

### 1. **Ako koristiš `reflex run`:**
Logove vidiš direktno u terminal gde si pokrenuo reflex server.

### 2. **Ako koristiš VS Code terminal:**
Logove vidiš u terminal panelu.

### 3. **Ako koristiš Browser Console:**
Mogu se pojaviti i tu, ali primarno su u server terminalu.

## Očekivani Tok Logovanja (Uspešan Scenario)

```
[NOTATION_UPLOAD] Početak handle_notation_upload, fajlova primljeno: 1
[NOTATION_UPLOAD] Postavljam UI u 'uploading' stanje
[NOTATION_UPLOAD] Obradujem fajl: my_notation.pdf
[NOTATION_UPLOAD] Čitam file bytes iz: my_notation.pdf
[NOTATION_UPLOAD] Pročitano 245632 bajtova
[NOTATION_UPLOAD] Validiram fajl...
[NOTATION_UPLOAD] Validacija prošla uspešno
[NOTATION_UPLOAD] Čuvam notaciju na disk...
[NOTATION_UPLOAD] Notacija sačuvana na: uploads/notation/my_notation.pdf

[LM_STUDIO] extract_progression_from_document START - filename=my_notation.pdf, size=245632 bajtova
[LM_STUDIO] Kreiram AsyncOpenAI klijent sa base_url=http://localhost:1234/v1
[LM_STUDIO] Počinjem sa model resolution...
[LM_STUDIO] _resolve_model - self.model=
[LM_STUDIO] Pozivam client.models.list()...
[LM_STUDIO] Dobio sam modele - broj: 3
[LM_STUDIO] Proveravajući model: gemma-2-9b-it
[LM_STUDIO] Odabrao model: gemma-2-9b-it
[LM_STUDIO] Model resolved: gemma-2-9b-it
[LM_STUDIO] Tip fajla: pdf
[LM_STUDIO] Renderujem PDF stranice...
[LM_STUDIO] PDF renderovan - broj stranica: 2
[LM_STUDIO] PDF content built sa 2 slika

[LM_STUDIO] Počinjem HTTP zahtev ka LM Studio (model=gemma-2-9b-it, timeout=30s)
[LM_STUDIO] Pokušaj #1, response_format=JSON_SCHEMA
[LM_STUDIO] Šaljem zahtev...  (messages=2)
[LM_STUDIO] Primljen odgovor od LM Studio - finish_reason=stop
[LM_STUDIO] Response content length: 542 karaktera
[LM_STUDIO] Parsiran JSON - ključevi: ['progression', 'title', 'note', 'source_excerpt', 'model_used']
[LM_STUDIO] Rezultat: progression='C maj7 F maj7 G maj7 C maj7', model_used=gemma-2-9b-it

[NOTATION_UPLOAD] Odgovor od LM Studio: offline_mode=False, result keys=['progression', 'title', 'note', 'source_excerpt', 'model_used']
[NOTATION_UPLOAD] Ekstraktovana progresija: 'C maj7 F maj7 G maj7 C maj7'
[NOTATION_UPLOAD] UI state ažuriran - model_used: gemma-2-9b-it
[NOTATION_UPLOAD] Progresija pronađena, primenjujem na input
[NOTATION_UPLOAD] Primenjujem progresiju: C maj7 F maj7 G maj7 C maj7

[NOTATION_UPLOAD] Pokrećem analyze_and_generate()
[ANALYZE] Početak analyze_and_generate sa chord_input: 'C maj7 F maj7 G maj7 C maj7'
[ANALYZE] Parsujem progresiju...
[ANALYZE] Progresija parsovana uspešno: 4 akorda
[ANALYZE] Lokalna analiza završena - roots=['C', 'F', 'G']
[ANALYZE] Startam parallel tasks...
[ANALYZE] LLM summary pripremljen
[ANALYZE] Pozivam LMStudioClient.analyze_progression()...

[LM_STUDIO] analyze_progression START - progression='C maj7 F maj7 G maj7 C maj7'
[LM_STUDIO] Šaljem zahtev ka analyze_progression (model=gemma-2-9b-it)
[LM_STUDIO] Primljen odgovor - finish_reason=stop
[LM_STUDIO] Response content length: 1204 karaktera
[LM_STUDIO] Parsiran JSON - ključevi: ['analysis', 'suggestions', 'socratic_questions', ...]
[LM_STUDIO] analyze_progression ZAVRŠENA - model_used=gemma-2-9b-it

[ANALYZE] Čekam bass_task i llm_task...
[ANALYZE] Oba taska završena - bass_notes=8, offline_mode=False
[ANALYZE] Sve rezultate su ažurirane - analiza ZAVRŠENA USPEŠNO
[NOTATION_UPLOAD] analyze_and_generate() završena, 1 eventa
[NOTATION_UPLOAD] Upload notacije ZAVRŠEN USPEŠNO
```

## Mogući Problemi i Šta da Tražiš u Logovima

### Problem 1: "Vizuelno se ništa ne desava"

**Šta tražiti u logovima:**
```
[NOTATION_UPLOAD] Pročitano XXX bajtova
```
Ako ova linija nema, fajl se nije čitao.

```
[LM_STUDIO] Pozivam client.models.list()...
[LM_STUDIO] Dobio sam modele - broj: 0
```
Ako je `broj: 0`, LM Studio nema dostupnih modela.

### Problem 2: "LM Studio se ne dobacuje"

**Šta tražiti:**
```
[LM_STUDIO] Šaljem zahtev...  (messages=2)
```
Ako ova linija nema, nikad se zahtev nije poslao.

```
[LM_STUDIO] Primljen odgovor od LM Studio - finish_reason=stop
```
Ako ova linija nema, problem je u mreži ili timeout.

### Problem 3: "Progresija nije pronađena"

**Šta tražiti:**
```
[LM_STUDIO] Rezultat: progression='', model_used=gemma-2-9b-it
[NOTATION_UPLOAD] Progresija nije pronađena: LM Studio nije uspeo...
```

### Problem 4: `analyze_and_generate()` se ne pokreće

**Šta tražiti:**
```
[NOTATION_UPLOAD] Pokrećem analyze_and_generate()
[ANALYZE] Početak analyze_and_generate sa chord_input: 'C maj7...'
```
Ako `[ANALYZE]` nema, metoda se nije pokrenula.

## Kako Aktivirati Logovanje?

Logovanje je **automatski aktivirano** sa nivoom `DEBUG`. Ako želiš da ga prilagodim:

### 1. **Privremeno isključi DEBUG logove:**
U `state.py`, promeni:
```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```

U:
```python
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```

### 2. **Isključi samo određene module:**
```python
logging.getLogger('harmonix.ai.lmstudio').setLevel(logging.WARNING)
```

## Sledeći Koraci - Šta da Uradiš?

1. **Pokupi logove:**
   - Pokreni Upload Notation
   - Kopira sve logove iz terminala
   - Pasteaj ih negde

2. **Analiziraj logove:**
   - Pronađi `[ERROR]` ili `[EXCEPTION]` poruke
   - Vidi na kojoj tački se zaustavlja
   - Vidi tačnu poruku greške

3. **Diagnoza problema:**
   - Ako nema `[LM_STUDIO] Šaljem zahtev...` → LM Studio nije dostupan
   - Ako je `broj: 0` modela → LM Studio nema učitanog modela
   - Ako je `progression=''` → Model nije mogao da pročita notaciju
   - Ako nema `[ANALYZE]` logova → Analiza se nikad nije pokrenula

## Testiranje

Za brzo testiranje, testiraj sa **song examples** (npr. "Autumn Leaves"):
1. Otvori "Bekend Progresije" tab
2. Klikni "Analiziraj pesmu" na Autumn Leaves

Ako to radi, onda je LM Studio OK, problem je u notaciji OCR-u.

## Kontakt za Debug

Ako problemi persista, prikazi mi logove sa sledeće tri poruke:
1. `[NOTATION_UPLOAD] Početak handle_notation_upload`
2. `[LM_STUDIO] Odgovor od LM Studio` ili `[LM_STUDIO]` greška
3. `[ANALYZE] Početak analyze_and_generate` ili `[ANALYZE]` greška

---

**Status:** ✅ Logovanje je implementirano i sprema za rad
**Verzija:** 1.0
**Datum:** 2026-04-26
