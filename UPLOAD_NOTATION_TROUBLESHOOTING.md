# Upload Notation - Troubleshooting Checklist

## 🔴 Greške pri Upload Notation

Koristi ovaj checklist da identifikuješ problem na osnovu logova.

---

## ❌ Problem: \"Uploadujem dokument... 100%\" ali ništa se ne desava

### Šta vidim u logovima?

```
[NOTATION_UPLOAD] Notacija sačuvana na: uploads/notation/my_file.pdf
[NOTATION_UPLOAD] Šaljem dokument LM Studio modelu i čekam odgovor...
```

**ALI** nema sledećeg:
```
[LM_STUDIO] extract_progression_from_document START
```

### 🔧 Rješenje:

1. **Provjeri da li je LM Studio pokrenut:**
   ```bash
   # Terminal 1 - LM Studio
   lm-studio
   # Trebao bi da bude dostupan na http://localhost:1234
   ```

2. **Provjeri environment varijable:**
   ```bash
   # U terminalu gdje koristiš `reflex run`
   echo %LMSTUDIO_BASE_URL%
   echo %LMSTUDIO_MODEL%
   ```

3. **Testiraj LM Studio konekciju:**
   ```bash
   curl http://localhost:1234/v1/models
   ```
   Trebao bi da vrati JSON sa dostupnim modelima.

---

## ❌ Problem: \"Dobio sam modele - broj: 0\"

### Šta vidim u logovima?

```
[LM_STUDIO] Pozivam client.models.list()...
[LM_STUDIO] Dobio sam modele - broj: 0
[LM_STUDIO] Korišćenje fallback modela: gemma-4-e2b-it
```

### 🔧 Rješenje:

1. **LM Studio nema učitanog modela!**
   - Otvori LM Studio aplikaciju
   - Učitaj model (npr. `Gemma 2 9B IT`)
   - Čekaj da se model u potpunosti učita

2. **Provjeri da li je model dostupan:**
   ```bash
   curl http://localhost:1234/v1/models
   ```
   Trebalo bi da vrati nešto kao:
   ```json
   {
     \"object\": \"list\",
     \"data\": [
       {\"id\": \"gemma-2-9b-it\", ...}
     ]
   }
   ```

---

## ❌ Problem: \"Primljen odgovor - finish_reason=length\"

### Šta vidim u logovima?

```
[LM_STUDIO] Primljen odgovor od LM Studio - finish_reason=length
[LM_STUDIO] Response content length: 4096 karaktera
```

### 🔧 Rješenje:

Model je počeo da generiše odgovor ali je dostigao limit tokena.

1. **Krađa model sa većim token limitom:**
   - Koristi `Gemma 2 27B` umjesto `Gemma 2 9B`
   - Ili `Llama 2 70B` ako je dostupan

2. **Ili skrati prompt:**
   - Idi u `harmonix/ai/lmstudio.py`
   - Pronađi `_build_document_pdf_content()` i `_build_document_image_prompt()`
   - Skrati instrukcije LLM-u

---

## ❌ Problem: \"Rezultat: progression=''\"

### Šta vidim u logovima?

```
[LM_STUDIO] Parsiran JSON - ključevi: ['progression', 'title', 'note', ...]
[LM_STUDIO] Rezultat: progression='', model_used=gemma-2-9b-it
[NOTATION_UPLOAD] Progresija nije pronađena: Nije pronađena čitljiva progresija
```

### 🔧 Rješenje:

Model je procesirao sliku/PDF ali nije mogao izdvojiti akorde.

1. **Provjeri sliku:**
   - Slika mora biti jasna i čitljiva
   - Akorde trebalo bi da budu vidljive
   - Probaj sa bolesnijom slikom

2. **Testiraj sa primjerom:**
   - Umjesto custom slike, koristi `Autumn Leaves` primjer
   - Klikni \"Analiziraj pesmu\" na song example
   - Ako to radi → problem je u OCR-u ili kvaliteti slike

3. **Provjeri model:**
   - Gemma 2 9B može imati problema sa vizuelnim zadacima
   - Pokušaj sa boljim modelom ako dostupan

---

## ❌ Problem: JSON parse error

### Šta vidim u logovima?

```
[LM_STUDIO] Parsiran JSON - ključevi: [...]
[LM_STUDIO] GREŠKA pri extract_progression_from_document: JSONDecodeError
```

### 🔧 Rješenje:

Model je vratio response koji nije validan JSON.

1. **Provjeri raw response:**
   - Dodaj `print(response_content)` u `_parse_json_payload()`
   - Vidi tačno šta je model vratio

2. **Koristi različit response format:**
   - U `extract_progression_from_document()` ima dva pokušaja:
     - Prvi: sa `response_format=JSON_SCHEMA`
     - Drugi: bez response format-a
   - Ako prvi ne radi, drugi trebao bi da radi

3. **Provjeri prompt:**
   - Možda LLM upustva trebalo bi biti jasnija
   - Idi u `_build_document_pdf_content()` i `_build_document_image_prompt()`

---

## ❌ Problem: Timeout - \"Šaljem zahtev...\" ali nema odgovora

### Šta vidim u logovima?

```
[LM_STUDIO] Šaljem zahtev...  (messages=2)
[čeka se 30 sekundi...]
[LM_STUDIO] GREŠKA pri extract_progression_from_document: TimeoutError
```

### 🔧 Rješenje:

1. **LM Studio je spor:**
   - Model je veliki i traje obradu
   - Čekaj da se zahtjev procesira
   - Možeš povećati timeout:
     ```python
     # U `.env` fajl
     LMSTUDIO_TIMEOUT_SECONDS=120
     ```

2. **LM Studio je odlepljen:**
   - Restartuj LM Studio
   - Restartuj reflex app: `reflex run`

3. **Mreža je loša:**
   - Provjeri da je `http://localhost:1234` dostupna
   - Ako koristiš drugačiji host, promijeni `LMSTUDIO_BASE_URL`

---

## ❌ Problem: \"Analiza nije uspela\" (analyze_and_generate greška)

### Šta vidim u logovima?

```
[NOTATION_UPLOAD] Pokrećem analyze_and_generate()
[ANALYZE] Početak analyze_and_generate sa chord_input: 'C maj7...'
[ANALYZE] GREŠKA pri analizi: [GREŠKA]
```

### 🔧 Rješenje:

1. **Provjeri grešku:**
   - Loguj tačnu grešku iz `[ANALYZE] GREŠKA pri analizi`
   - Ako je `HarmonyParseError`, progresija nije valida
   - Ako je `AttributeError`, problem je u teorijskoj analizi

2. **Testiraj progresiju:**
   - Manuelno unesi istu progresiju u \"Manual Entry\" tab
   - Ako radi tamo, problem je u extraktu iz notacije

3. **Provjeri LM Studio za analizu:**
   - `analyze_progression()` se izvršava paralelno sa bass generacijom
   - Ako nema `[LM_STUDIO] analyze_progression START`, nema zahteva

---

## ✅ Problem: Sve radi ali je SPORO

### Šta vidim u logovima?

```
[NOTATION_UPLOAD] Pročitano XXX bajtova
[...dugačka čekanja...]
[ANALYZE] Oba taska završena
```

### 🔧 Rješenje:

Sve je OK, samo je sporo jer:

1. **PDF renderovanje** - ako je PDF veliki, rendering je spora
2. **LLM analiza** - model traje da obradi zahtjev
3. **Bass generacija** - music theory kalkulacije

To je normalno! Čekaj 10-30 sekundi.

---

## 🔍 Debug Mode - Detaljniji Logovi

Ako želiš još detaljnije logove, dodaj u `state.py`:

```python
import logging
logging.getLogger('harmonix').setLevel(logging.DEBUG)
logging.getLogger('harmonix.ai').setLevel(logging.DEBUG)

# Za MAXIMUM debug (uključi OpenAI client logove)
logging.getLogger('openai').setLevel(logging.DEBUG)
logging.getLogger('httpx').setLevel(logging.DEBUG)
```

---

## 📋 Checklist za Bug Report

Ako se problem ne može riješiti, prikupi:

- [ ] Kompletan log od `[NOTATION_UPLOAD] Početak` do kraja
- [ ] Verzija LM Studio-a (`lm-studio --version`)
- [ ] Naziv i veličina file-a koji testira
- [ ] Output od `curl http://localhost:1234/v1/models`
- [ ] Environment varijable: `LMSTUDIO_BASE_URL`, `LMSTUDIO_MODEL`, `LMSTUDIO_TIMEOUT_SECONDS`
- [ ] OS i verzija (Windows 10/11, macOS, Linux)

---

**Poslednja Ažuriranja:** 2026-04-26  
**Verzija:** 1.0  
**Status:** ✅ Sprema za troubleshooting
