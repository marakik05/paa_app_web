# paa_app_web — CLAUDE.md

## Project Overview

Web εφαρμογή για Έλληνες γεωπόνους μελετητές που υποστηρίζει αιτήσεις επιδοτήσεων του ΠΑΑ 2023-2027.
Είναι η web έκδοση της desktop εφαρμογής `paa_app_moria` (PySide2), φτιαγμένη με Flask + Vanilla JS.

UI strings, comments, and variable names are in Greek.

---

## Architecture

- **Backend**: Python 3.x + Flask (`server.py`)
- **Frontend**: Vanilla JS + HTML + CSS (χωρίς framework)
- **Storage**: SQLite via `database_manager.py`; DB at `%LOCALAPPDATA%\OsdeCalculatorApp_web\osde_app_web.db`
- **Reference data**: `data/ta.xlsx` (τυπικές αποδόσεις) — φορτώνεται στο startup μέσω `utils/excel_loader.py`
- **Styling**: 6 αρχεία CSS στο `static/` (βλ. πίνακα παρακάτω) — CSS variables (πράσινο θέμα) στο `base.css`

### Page / Section flow

Μία μόνο HTML σελίδα (`templates/index.html`) με δύο sections που εναλλάσσονται μέσω navbar. Το  modal (_modals.html) είναι Jinja partials στο `templates/partials/`, συμπεριλαμβανόμενα με `{% include %}`:

```
index.html
    ├── section[data-page-container="arxiki"]  — Συγκεντρωτικός πίνακας παραγωγών
    ├── section[data-page-container="ta"]      — Πίνακας υπολογισμού ΤΑ Αρχικής
    └── {% include 'partials/_modals.html' %}
```

### JS αρχεία

| Αρχείο | Σκοπός |
|--------|--------|
| `static/main_window.js` | Navigation, import/export handlers, save handler |
| `static/section_arxiki.js` | Πίνακας παραγωγών — φόρτωση, φιλτράρισμα, επεξεργασία, διαγραφή |
| `static/section_ta.js` | Πίνακας ΤΑ — δόμηση γραμμών, recalcAll, searchable comboboxes |
| `static/messages.js` | `showToast(msg, color)`, `showConfirmModal(msg, title)` |

### CSS αρχεία

| Αρχείο | Σκοπός |
|--------|--------|
| `static/base.css` | Variables, reset, navbar, layout, buttons, section headers, toast |
| `static/forms.css` | `#personal-info`, αναζήτηση αρχικής |
| `static/tables.css` | Κοινά table styles, records-table, ta-table, tfoot |
| `static/combobox.css` | Searchable combo + portal dropdown |
| `static/modals.css` | Modal-overlay/box/header/actions, conflict-list |
| `static/responsive.css` | 3 media queries (tablet/mobile/large screens) |

### Navigation logic (`main_window.js`)

- `.navbar a[data-page]` links εναλλάσσουν `hidden` attribute στα sections
- `nav-disabled` class → `pointer-events: none` (κλειδωμένο section)
- `lockTaSection()` / `unlockTaSection()` — κλειδώνει/ξεκλειδώνει το ΤΑ section και το nav link
- Κουμπιά `new-record` / `import` ενεργά μόνο στο section arxiki

### Βασική ροή χρήστη

1. Αρχική σελίδα → πίνακας παραγωγών (`loadProducersTable()`)
2. Κουμπί **Νέα Εγγραφή** → modal για ΑΦΜ/Όνομα/Επώνυμο → αποθήκευση στη βάση
3. Κουμπί **Επεξεργασία** (στον πίνακα) → `handleEditClick(afm)`:
   - Γεμίζει AFM/Όνομα/Επώνυμο/Περιφέρεια στη φόρμα
   - Ξεκλειδώνει section ΤΑ + πλοηγείται εκεί αυτόματα
   - Καθαρίζει τα φίλτρα αναζήτησης
4. **Αποθήκευση** → POST `/api/producer/<afm>/save` με name/surname/region + TA rows
5. **Εισαγωγή** → xlsx upload, parse, conflict modal, execute
6. **Εξαγωγή** → POST `/api/producer/<afm>/export` με UI data → κατεβάζει xlsx

---

## Key Files

| Αρχείο | Σκοπός |
|--------|--------|
| `server.py` | Flask routes + startup (canon dicts, TA mapping) |
| `database_manager.py` | Όλες οι SQLite λειτουργίες |
| `utils/excel_loader.py` | Φόρτωση ta.xlsx, `norm()`, constants |
| `utils/ta_calculations.py` | Pure-Python υπολογισμοί ΤΑ (χωρίς Qt) |
| `utils/import_utils.py` | Canonicalization + validation + xlsx parsing για import |
| `templates/index.html` | Μόνο HTML template |
| `data/ta.xlsx` | Reference data — κατηγορίες, τυπικές αποδόσεις |

---

## API Routes (`server.py`)

| Method | Route | Περιγραφή |
|--------|-------|-----------|
| `GET` | `/` | Render index.html |
| `GET` | `/api/regions` | Λίστα περιφερειών |
| `GET` | `/api/producer/<afm>/exists` | Έλεγχος αν ΑΦΜ υπάρχει |
| `GET` | `/api/producer/<afm>/full` | Δεδομένα παραγωγού + ΤΑ γραμμές |
| `POST` | `/api/producer/<afm>/save` | Αποθήκευση παραγωγού + ΤΑ |
| `DELETE` | `/api/producer/<afm>` | Διαγραφή παραγωγού |
| `GET` | `/api/producers` | Όλοι οι παραγωγοί (για πίνακα αρχικής) |
| `GET` | `/api/ta/reference` | TA mapping (categories → descriptions) |
| `POST` | `/api/ta/recalculate` | Επανυπολογισμός ΤΑ γραμμών από server |
| `POST` | `/api/import/parse` | Parse xlsx → επιστρέφει new_data + conflicts |
| `POST` | `/api/import/execute` | Εκτέλεση import με decisions |
| `POST` | `/api/producer/<afm>/export` | Export ΤΑ σε xlsx (διαβάζει από request body) |

### Startup globals στο `server.py`

```python
TA_MAPPING, TA_VALUE_MAPPING = load_excel_data(resource_path('data/ta.xlsx'))
_CANON_PAIR, _CANON_CAT, _VALID_CATS, _VALID_DESCS = build_canon_dicts(TA_VALUE_MAPPING)
```

---

## ΤΑ Table (section_ta.js)

### Στήλες

| # | data-col | Περιεχόμενο | Input |
|---|----------|-------------|-------|
| 0 | 0 | Κατηγορία ΟΣΔΕ | searchable combo (portal dropdown) |
| 1 | 1 | Περιγραφή | searchable combo (δυναμική ανά κατηγορία) |
| 2 | 2 | Τυπική Απόδοση | read-only (από server) |
| 3 | 3 | Έκταση/Αριθμός ζώων | text input (decimal) |
| 4 | 4 | Βιολογικά/Ολοκλ/μένη/ΠΟΠ-ΠΓΕ | `<select>` |
| 5 | 5 | Δένδρα >=4 ετών | text input (int) |
| 6 | 6 | Δένδρα <4 ετών | text input (int) |
| 7 | 7 | Αμπέλι >3 ετών | `<select>` (Ναι/Όχι) — ενεργό μόνο για LOCK_AMPELI |
| 8 | 8 | ΤΑ ανά επιλογή | read-only (από server) |
| 9 | 9 | Διαγραφή | button × |

**tfoot**: `total-ta`, `total-ta-sum`, `total-ta-plant`, `total-ta-animal`, `total-ta-bee-silk`

### Βασικές συναρτήσεις

| Συνάρτηση | Περιγραφή |
|-----------|-----------|
| `buildTaRow()` | Δημιουργεί νέα `<tr>` με όλα τα inputs |
| `buildSearchableCombo(options, initialValue)` | Searchable combo με βελάκι (▼) + portal dropdown + tooltip |
| `recalcAll()` | POST στο `/api/ta/recalculate` → ενημερώνει cols 2, 8, tfoot, lock states |
| `getTaRows()` | Διαβάζει όλες τις γραμμές από DOM → 14-element arrays |
| `loadTaTable(rows)` | Γεμίζει πίνακα από DB rows (17-element arrays από `fetch_entries`) |
| `lockTaSection()` | Disabled fieldset + nav-disabled + disabled name/surname/district + καθαρισμός δεδομένων |
| `unlockTaSection()` | Αντίστροφο του lock |

### `getTaRows()` layout (14 στοιχεία ανά γραμμή)

```
[cat(0), desc(1), typ_out(2), qty(3), cert(4),
 trees4+(5), trees4-(6), vine(7), out_pc(8),
 total_output(9), ta_productive(10), ta_plant(11), ta_animal(12), ta_bees(13)]
```

Τα indices 9–13 διαβάζονται από το tfoot (ίδια τιμή σε όλες τις γραμμές).

### Searchable Combo — Portal pattern

Το `.combo-dropdown` δεν βρίσκεται μέσα στο wrapper αλλά στο `document.body` με `position: absolute` και `z-index: 9999`. Η `positionDropdown()` χρησιμοποιεί `getBoundingClientRect()` για σωστή τοποθέτηση. Έτσι δεν κόβεται από το table overflow. Το `input.title` ενημερώνεται σε κάθε `change` για tooltip με πλήρη περιγραφή.

---

## Section Αρχική (section_arxiki.js)

### Πίνακας παραγωγών

| # | Στήλη | Πηγή |
|---|-------|------|
| 0 | ΑΦΜ | `row[0]` |
| 1 | Όνομα | `row[1]` |
| 2 | Επώνυμο | `row[2]` |
| 3 | Περιφέρεια | `row[3]` |
| 4 | Αρχική ΤΑ | `row[4]` |
| 5 | Τελευταία Επεξεργασία | `row[5]` |
| 6 | Επεξεργασία | EditButton |
| 7 | Διαγραφή | DeleteButton |

`/api/producers` επιστρέφει: `[afm, first_name, last_name, region, initial_ta, last_modified]`

### Live φιλτράρισμα

- `_allProducers` — module-level cache με όλες τις εγγραφές
- `_renderTable()` — φιλτράρει το cache και αποδίδει τον πίνακα
- `search-afm` input → μόνο ψηφία, `includes()` match
- `search-surname` input → case-insensitive `includes()` match
- AND λογική μεταξύ των δύο φίλτρων
- `loadProducersTable()` → ανανεώνει cache + καλεί `_renderTable()`

### `handleEditClick(afm)`

1. Γεμίζει `#AFM` input
2. `unlockTaSection()` — ξεκλειδώνει nav link ΤΑ
3. `.click()` στο nav link "ΤΑ Αρχικής" — αυτόματη πλοήγηση
4. Καθαρίζει `search-afm` / `search-surname` + `_renderTable()`
5. `loadProducer(afm)` — φορτώνει δεδομένα

---

## Import / Export

### Import (`/api/import/parse` + `/api/import/execute`)

- Format: **xlsx μόνο** (όχι CSV)
- Φόρτωση: producer info (ΑΦΜ/Όνομα/Επώνυμο/**Περιφέρεια**) + initial TA (sheet "Τυπική Απόδοση")
- Magic-bytes check: πρώτα 2 bytes πρέπει να είναι `PK`
- Canonicalization → `_canonicalize_entry_row()` (διορθώνει γραφή ακόμα και με διαφορές σε case/τόνους)
- Validation → `_validate_import_row()` (raises `ValueError`)
- **Περιφέρεια**: υποχρεωτική στήλη ("Περιφέρεια"/"region"). Τιμή της κάθε ομάδας ΑΦΜ ελέγχεται norm-based έναντι `build_region_canon(PERIFERIES)` (`utils/import_utils.py`) — αν δεν ταιριάζει με καμία επιλογή του `district`, raises `ValueError` (το αρχείο θεωρείται μη έγκυρο). Κενό κελί → `"--Επιλέξτε"` (έγκυρο, μέλος του `PERIFERIES`)
- Conflicts → `ImportConflictDialog` modal στο frontend (radio buttons ανά ΑΦΜ)
- Αποφάσεις: `replace` (διαγράφει `osde_entries` + ενημερώνει **name, surname, region** + `last_modified`) ή `skip`
- Μετά από import: καθαρισμός AFM/name/surname/district inputs + `lockTaSection()`
- **Calculated fields ΔΕΝ εισάγονται** — πάντα ξαναυπολογίζονται

### Export (`POST /api/producer/<afm>/export`)

- **Διαβάζει ΠΑΝΤΑ από request body** (όχι από DB) — ο χρήστης μπορεί να εξάγει αναποθήκευτα δεδομένα
- JS στέλνει: `{name, surname, region, rows: getTaRows(), totals: {total_ta, ta_prod, ta_plant, ta_animal, ta_bees}}`
- Excel sheet "Τυπική Απόδοση" με 18 στήλες — "Περιφέρεια" δίπλα στο "Επώνυμο", επαναλαμβάνεται σε κάθε γραμμή (ίδια λογική με ΑΦΜ/Όνομα/Επώνυμο)
- Τα αθροίσματα (totals) γράφονται μόνο στη γραμμή 2 (πρώτη data row), υπόλοιπες κενές

---

## Database (`database_manager.py`)

DB path: `%LOCALAPPDATA%\OsdeCalculatorApp_web\osde_app_web.db`

### Functions

| Function | Usage |
|----------|-------|
| `setup_database()` | Create tables + migrations — καλείται στο Flask startup |
| `_now_iso()` | Timestamp ISO 8601 (`YYYY-MM-DD HH:MM:SS`) |
| `save_producer_basics(afm, name, surname, region)` | INSERT or UPDATE producer + `last_modified` |
| `save_scenario_data(afm, scenario, data)` | Αποθήκευση ΤΑ γραμμών (`'initial'`) |
| `fetch_producer(afm)` | Returns `(name, surname, region)` or None |
| `fetch_entries(afm, scenario)` | ΤΑ γραμμές για scenario |
| `fetch_all_producers()` | Όλοι οι παραγωγοί ORDER BY afm ASC → `[afm, first_name, last_name, region, initial_ta, last_modified]` |
| `fetch_single_producer_row(afm)` | Ίδιο shape με μία γραμμή της `fetch_all_producers()` για ένα ΑΦΜ (ορίζεται, δεν καλείται ακόμα από `server.py`) |
| `delete_producer(afm)` | Cascade διαγραφή |
| `delete_producer_entries(cursor, afm, scenario_type)` | Helper για import replace |
| `import_producers_batch_transaction_web(producers_data)` | Batch import — mini-transaction ανά ΑΦΜ |
| `to_float_or_empty(value)` / `to_int_or_empty(value)` | Safe cast helpers |

### Schema

```sql
CREATE TABLE producers (
    afm           TEXT PRIMARY KEY,
    first_name    TEXT,
    last_name     TEXT,
    region        TEXT,
    last_modified TEXT   -- ISO 8601 'YYYY-MM-DD HH:MM:SS'
)

CREATE TABLE osde_entries (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    producer_afm      TEXT,
    scenario_type     TEXT,    -- 'initial' (μόνο)
    category_osde     TEXT,
    description       TEXT,
    typical_output    REAL,
    quantity          REAL,
    certification     TEXT,
    trees_over_4      INTEGER,
    trees_under_4     INTEGER,
    vine_over_3       TEXT,
    output_per_choice REAL,
    total_output      REAL,
    ta_productive     REAL,
    ta_plant          REAL,
    ta_animal         REAL,
    ta_bees           REAL,
    FOREIGN KEY (producer_afm) REFERENCES producers(afm) ON DELETE CASCADE
)
```

`fetch_entries` row order: `[id, producer_afm, scenario_type, category_osde, description, typical_output, quantity, certification, trees_over_4, trees_under_4, vine_over_3, output_per_choice, total_output, ta_productive, ta_plant, ta_animal, ta_bees]` (index 0–16)

`loadTaTable` loading: `r[3]=cat, r[4]=desc, r[5]=typ_out, r[6]=qty, r[7]=cert, r[8]=trees4+, r[9]=trees4-, r[10]=vine`

---

## TA Calculations (`utils/ta_calculations.py`)

Pure-Python functions χωρίς Qt dependency.

| Function | Περιγραφή |
|----------|-----------|
| `lookup_typical_output(value_mapping, cat, desc, region)` | Στήλη 2: aegean ή default column |
| `typiki_apodosi(cat, ta, qty, t4p, t4m, vine)` | Στήλη 8: ΤΑ ανά επιλογή |
| `ta_paragwgikwn(cat, ta, qty, t4p, t4m, vine)` | ΤΑ παραγωγικών δένδρων |
| `paragwgikwn(cat, desc, out_pc, productive)` | Στήλη 11: ΤΑ Παραγωγικών |
| `route_fzm(category)` | Routing: 12=Φυτικής, 13=Ζωικής, 14=Μελισσιών |
| `calc_row(value_mapping, region, cat, desc, qty, t4p, t4m, vine)` | Υπολογισμός 1 γραμμής |
| `calc_totals(rows_calc)` | Σύνολα tfoot |
| `to_float(value)` / `to_int(value)` | Parse helpers |

---

## Constants (`utils/excel_loader.py`)

| Constant | Usage |
|----------|-------|
| `PERIFERIES` | Λίστα περιφερειών για combo |
| `AEGEAN_PERIFERIES` | `{Βόρειο Αιγαίο, Νότιο Αιγαίο, Κρήτη}` → aegean column |
| `LOCK_AMPELI_NORM` | Κατηγορίες που ενεργοποιούν col 7 (Αμπέλι >3yr) |
| `LOCK_TREES_NORM` | Κατηγορίες που κλειδώνουν cols 5 & 6 (δένδρα) |
| `FMZ_ZWIKI_NORM` | Ζωική παραγωγή → col 13 |
| `FMZ_MELISSES_NORM` | Μελίσσια/μεταξοσκώληκες → col 14 |
| `PARAGWGIKA_NORM` | Keywords παραγωγικών ζώων |
| `PARAGWGIKA_CAT_NORM` | Κατηγορίες παραγωγικών ζώων |
| `norm(text)` | Lowercase + strip + normalize |
| `in_norm_set(text, norm_set)` | Membership check με norm |
| `resource_path(relative_path)` | Absolute path (dev + frozen) |

---

## Πριν από αλλαγές σε υπάρχοντα symbols

Πριν αλλάξεις signature ή συμπεριφορά οποιουδήποτε υπάρχοντος symbol:

1. Τρέξε `Grep` για το όνομά του σε **όλο το project**.
2. Άνοιξε κάθε σημείο χρήσης — JS, Python, HTML.
3. Αν αλλάξεις signature, ενημέρωσε **όλα** τα σημεία χρήσης στην ίδια αλλαγή.

**Ισχύει για**: API routes, JS functions, DB schema, tuple shapes, CSS classes.

---

## Conventions & Rules

- **Python 3.x** — χωρίς Qt/PySide2
- **Vanilla JS** — χωρίς framework (React, Vue, κ.λπ.)
- **UI language: Greek** everywhere
- **CSS μόνο στα αρχεία `static/*.css`** (βλ. πίνακα CSS αρχείων) — χωρίς inline styles εκτός από δυναμικά (π.χ. toast, portal dropdown positioning)
- Read-only cells: background `var(--green-50)`
- Searchable comboboxes: **πάντα portal pattern** (dropdown στο `document.body`) για να μην κόβεται από table overflow
- Δεν γίνεται νέο API call για φιλτράρισμα — χρησιμοποιείται ο `_allProducers` cache
- Το export **πάντα διαβάζει από request body** (UI state) — ποτέ από DB
- Αλλαγές στο DB schema μόνο μέσω `_run_migrations()` + `_add_column_if_missing()`

## Avoid

- Μην εισάγεις calculated fields στο import (ΤΑ, totals) — ξαναυπολογίζονται πάντα
- Μην προσθέτεις timestamp logic στο `save_scenario_data` — το `save_producer_basics` το διαχειρίζεται
- Μην χρησιμοποιείς `position: absolute` μέσα στον πίνακα για dropdowns — χρησιμοποίησε portal pattern
- Μην κάνεις API call σε κάθε πάτημα πλήκτρου στα φίλτρα — φιλτράρισμα client-side μέσω cache

---

## Run

```bash
pip install -r requirements.txt
python server.py
# → http://127.0.0.1:5000
```

## Dependencies

- `Flask`
- `openpyxl`
- `utils/excel_loader.py` (φορτώνει `data/ta.xlsx` μέσω `openpyxl`)
