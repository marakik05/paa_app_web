# paa_app_moria — CLAUDE.md

## Project Overview

Desktop GUI application for Greek agricultural consultants ("γεωπόνοι μελετητές") supporting EU CAP subsidy applications for three interventions:
- **Π3-73-2.1** — Σχέδια Βελτίωσης Γεωργικών Εκμεταλλεύσεων
- **Π3-73-2.2** — Επενδύσεις εξοικονόμησης ύδατος
- **Π3-73-2.6** — Επενδύσεις κυκλικής οικονομίας & ενέργειας

UI strings, comments, and variable names are in Greek.

---

## Architecture

- **Framework**: Python 3.8 + PySide2 5.15.2.1 (Qt 5.15)
- **Navigation**: `QMainWindow` with `QStackedWidget` — 5 pages
- **Storage**: SQLite via `database_manager.py`; DB at `%LOCALAPPDATA%\OsdeCalculatorApp_3\osde_app_3.db`
- **Reference data**: `data/ta.xlsx` (typical yields) loaded at startup via `utils/excel_loader.py`
- **Styling**: CSS inside `.ui` files only — no inline Python styling except in delegates

### Page flow

```
main.py → MainWindow (main_window.py)
    ├── page_arxiki.py          — producer list (home, index 0)
    ├── page_0_ta.py            — initial state TA (ΤΑ αρχική)
    ├── page_mellontiki.py      — future state TA (ΤΑ μελλοντική)
    ├── page_1_epileximotita.py — eligibility questions (επιλεξιμότητα)
    └── page_moria.py           — scoring criteria & budget (μόρια)
```

`page_0_ta.py` and `page_mellontiki.py` both inherit from `pages/base_table.py`.

### Signal flow

```python
ta_page.totalChanged    → epi_page.update_lineEdit_7        # ΤΑ total → eligibility Q7
ta_page.totalChanged    → moria_page.update_lineEdit_2_1    # ΤΑ total → moria 2.1
ta_page.totalChanged    → moria_page.update_lineEdit_2_2    # ΤΑ total → moria 2.2
ta_page.biologicChanged → moria_page.update_lineEdit_1_2    # biologic % → moria 1.2
mel_page.set_source_table(ta_page)                          # future page sees initial for copy
ui.combo_periferia.currentTextChanged → on_periferia_changed
ta_page/mel_page.model.dataChanged/rowsInserted/rowsRemoved → mark_as_changed
ui.stackedWidget.currentChanged → _on_current_page_changed  # triggers pending TA/MEL warnings
```

### Important MainWindow flags

| Flag | Type | Purpose |
|------|------|---------|
| `has_unsaved_changes` | bool | Unsaved changes guard |
| `_marking_changes` | bool | Prevents multiple mark_as_changed calls |
| `_afm_focus_dialog_open` | bool | Prevents double dialog on lineEdit_afm |
| `_is_closing` | bool | closeEvent guard |
| `_current_loaded_afm` | str | Last loaded AFM (set lazily στο handle_search) |
| `search_or_edit_performed` | bool | True μετά από επιτυχές search/edit — gate για export & save validation |
| `_pending_ta_warning_message` | tuple/None | Deferred missing-categories warning για ta_page |
| `_pending_mel_warning_message` | tuple/None | Deferred missing-categories warning για mel_page |
| `_ta_categories_cache` | set | `(category, description)` pairs από ta.xlsx για import validation |
| `_valid_cats_cache` | set | Normalized category names — fast lookup στο import validation |
| `_valid_descs_cache` | set | Normalized description names — fast lookup στο import validation |
| `_canonical_cat_by_norm` | dict | `norm(cat) → canonical cat` από ta.xlsx — reverse lookup για import canonicalization |
| `_canonical_pair_by_norm` | dict | `(norm(cat), norm(desc)) → (canonical_cat, canonical_desc)` — reverse lookup για ζευγάρια |

### Basic workflow

1. User is on **Σελίδα 1** (arx_page) at startup
2. Types **ΑΦΜ** (9 digits, QRegExpValidator) → `on_afm_changed`:
   - Exists in DB → activates `searchbtn`
   - Does not exist → activates `savebtn`
3. **Search** (`handle_search`): loads all producer data
4. **Save** (`handle_save`): saves producer basics (+ `last_modified` timestamp) + initial/future TA + eligibility + μόρια. Μετά το save, η γραμμή του ΑΦΜ στην αρχική ανανεώνεται μέσω `arx_page.upsert_producer_row(afm)`.
5. **Region change** (`on_periferia_changed`): recalculates TA in both tables + updates eligibility
6. Unsaved changes: eventFilter on `lineEdit_afm` + `closeEvent` warn the user

---

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point; high-DPI setup |
| `main_window.py` | Central controller, page wiring, save/search (~1890 lines) |
| `database_manager.py` | All SQLite operations (~610 lines) |
| `pages/base_table.py` | Base for TA table pages (~1050 lines) |
| `pages/page_arxiki.py` | Producer list — add, edit, delete (~495 lines) |
| `pages/page_0_ta.py` | Initial state TA data entry |
| `pages/page_mellontiki.py` | Future state TA data entry |
| `pages/page_1_epileximotita.py` | 9 eligibility questions (q1..q9) + ΤΑ + result |
| `pages/page_moria.py` | 16 scoring criteria + budget (~700 lines) |
| `delegates/delegates_dlt.py` | Custom Qt delegates: delete/edit buttons, searchable combos, number validators |
| `utils/excel_loader.py` | Loads ta.xlsx; exposes `norm()`, `resource_path()`, region/category constants |
| `utils/decimal_utils.py` | Helpers ακριβούς δεκαδικής αριθμητικής: `to_decimal()`, `q2()`, `fmt2()` (ROUND_HALF_UP, 2 δεκαδικά) |
| `utils/message.py` | Toast messages, conflict dialogs, missing-category warnings |
| `widgets/clearable_tableview.py` | QTableView με clipboard copy/paste/clear, custom arrow-key navigation, hover-block στις combo στήλες (0,1,4,7) |
| `ui/` | Qt Designer `.ui` files and generated `ui_*.py` wrappers |
| `data/ta.xlsx` | Reference data — crops, varieties, typical yields |
| `tests/` | Unit tests (unittest) — calculations, DB, excel_loader, moria scoring, import security |
| `installer/Sxedia_installer.iss` | Inno Setup script — παράγει `Sxedia_vX.Y_Setup.exe` |

---

## base_table Column Structure

Both TA pages (initial & future) share these columns:

| # | Column | Delegate | Fill |
|---|--------|----------|------|
| 0 | Κατηγορία ΟΣΔΕ | SearchableComboDelegate | User |
| 1 | Περιγραφή Είδους/Ποικιλίας/Ζώων | SearchableDynamicComboDelegate | User (depends on col 0) |
| 2 | Τυπική Απόδοση | Read-only, bg `#E3F2FD` | Auto from ta.xlsx + region |
| 3 | Έκταση / Αριθμός ζώων | Double2DecimalDelegate | User |
| 4 | Βιολογικά/Ολοκληρωμένη/ΠΟΠ-ΠΓΕ | NoWheelComboDelegate | User |
| 5 | Δένδρα >=4 ετών | IntOnlyDelegate | User (locked for LOCK_TREES_NORM) |
| 6 | Δένδρα <4 ετών | IntOnlyDelegate | User (locked for LOCK_TREES_NORM) |
| 7 | Αμπέλι >3 ετών | NoWheelComboDelegate (Ναι/Όχι) | User (active only for LOCK_AMPELI_NORM) |
| 8 | Τυπική απόδοση ανά επιλογή | Read-only, bg `#E3F2FD` | Auto: `typiki_apodosi()` |
| 9 | — | DeleteButtonDelegate | Delete row button |
| 10 | Σύνολο τυπικής απόδοσης | Read-only | Auto: sum of col 8 |
| 11 | ΤΑ Παραγωγικών | Read-only | Auto: `paragwgikwn()` |
| 12 | ΤΑ Φυτικής | Read-only | Auto: `total_fzm()` |
| 13 | ΤΑ Ζωικής | Read-only | Auto: `total_fzm()` |
| 14 | ΤΑ Μελίσσια/Μεταξοσκώληκες | Read-only | Auto: `total_fzm()` |

### Key calculations

**`typiki_apodosi(row)` → col 8:**
- Category ∈ `LOCK_AMPELI_NORM`:
  - "Ναι" → `ΤΑ × Έκταση`
  - "Όχι" → `(ΤΑ / 2) × Έκταση`
  - Empty → `None`
- Otherwise:
  - No trees → `ΤΑ × Έκταση`
  - Only young (<4yr) → `(ΤΑ / 2) × Έκταση`
  - Only productive (>=4yr) → `ΤΑ × Έκταση`
  - Mixed → `ΤΑ × (area × prod/total) + (ΤΑ/2) × (area × young/total)`

**`total_fzm()` → cols 12, 13, 14:**
- `FMZ_ZWIKI_NORM` → col 13 (Ζωικής)
- `FMZ_MELISSES_NORM` → col 14 (Μελισσιών)
- Rest → col 12 (Φυτικής)

**`paragwgikwn()` → col 11:**
- If category ∈ `PARAGWGIKA_CAT_NORM` **and** description contains keyword from `PARAGWGIKA_NORM` → adds col 8 value
- Otherwise → uses `ta_paragwgikwn(row)` (productive trees only)

**Eligibility Q7 threshold:**
- Region ∈ `ISLANDS` (`{Νότιο Αιγαίο, Βόρειο Αιγαίο, Ιόνια Νησιά}`) **and** ΤΑ ≥ 8,000 → ΕΠΙΛΕΞΙΜΟΣ
- Region ∉ `ISLANDS` **and** ΤΑ ≥ 12,000 → ΕΠΙΛΕΞΙΜΟΣ
- Otherwise → ΜΗ ΕΠΙΛΕΞΙΜΟΣ

**Regional TA lookup:**
- Region ∈ `AEGEAN_PERIFERIES` `{Βόρειο Αιγαίο, Νότιο Αιγαίο, Κρήτη}` → column E of ta.xlsx (`aegean`)
- Otherwise → column D (`default`)

---

## Moria scoring (`pages/page_moria.py`)

### Decimal arithmetic & rounding

**Όλοι** οι υπολογισμοί στο moria χρησιμοποιούν `Decimal` (μέσω `utils/decimal_utils.py`) — **όχι float**. Στρογγυλοποίηση **πάντα `ROUND_HALF_UP`** σε 2 δεκαδικά (`q2()` / `fmt2()`). Αυτό αποφεύγει banker's rounding (`ROUND_HALF_EVEN`, default του Python) που θα έκανε `2.675 → 2.67` αντί για το σωστό `2.68`. Επιβεβαιώνεται από τα tests `test_2_1_half_up_at_675` και `test_3_1_1_half_up_at_675`.

| Helper | Χρήση |
|--------|-------|
| `to_decimal(text)` | Cast string σε `Decimal` με ανοχή σε `,`/κενά. None αν άκυρο. |
| `q2(value)` | Quantize σε 2 δεκαδικά με ROUND_HALF_UP. |
| `fmt2(value)` | String formatting `"#.##"` με ROUND_HALF_UP. Άδειο string αν None. |

### Validators

Στα `lineEdit_3_1_1` (ίδια συμμετοχή), `lineEdit_4_1`, `lineEdit_5_1`, `lineEdit_budget` χρησιμοποιείται `QRegExpValidator` με pattern `^\d{0,7}(?:[.]\d{0,2})?$` — μέχρι 7 ψηφία ακέραιο μέρος + 2 δεκαδικά. Στο `editingFinished` καλείται `_format_lineEdit()` που τα μορφοποιεί με `fmt2()`.

### 16 κριτήρια μοριοδότησης

| Κριτήριο | Είσοδος | Κανόνας |
|----------|---------|---------|
| **1.1** | combo (Ναι/Όχι) | Ναι→5.00, Όχι→0 |
| **1.2** | βιολογικά % (auto από TA) | >50→6.00, αλλιώς 0 |
| **2.1** | ΤΑ αρχικής (auto) | <16000→2.50, 16000–25000→γραμμική (`50+50·(ΤΑ−16000)/9000`)·0.05, >25000→5.00 |
| **2.2** | ΤΑ μελλοντικής (auto) + budget | ΤΑ≤15000 ∧ budget≤75000 → 16.00; ΤΑ>15000 ∧ budget≤5·ΤΑ → 16.00; ΤΑ>12500 ∧ budget≤6·ΤΑ → 9.60; αλλιώς 0 |
| **3.1.1** | ίδια συμμετοχή + budget | ratio=ίδια/budget — ≤0.2→0; >0.5→7.00; γραμμική (`20+30·(ratio−0.2)/0.3`)·0.14 |
| **3.1.2** | combo (Ναι/Όχι) | Ναι→4.20 |
| **3.1.3** | combo (Ναι/Όχι) | Ναι→1.40 |
| **3.1.4** | combo (Ναι/Όχι) | Ναι→1.40 |
| **3.2** | combo (4 επιλογές) | "Νέος Αγρότης 2018/2021" / "Επιλαχόντας Μ6.1" / "Εμπειρία >5 ετών έως 50" → 8.00 |
| **3.3** | combo (4 επιλογές) | "Πτυχίο >=6,7,8" → 3.50; "Γεωτεχνικό >=6,7,8" → 5.00; "Γεωτεχνικό =<3,4,5" → 3.50 |
| **3.4** | combo (5 επιλογές) | "ΟΠ/Ομ.Π με μέλη>10" → 2.40; "ΑΣ" → 3.60; "ΑΣ+ΟΠ" ή "Αναγκαστικός Συνεταιρισμός" → 6.00 |
| **3.5** | combo (Ναι/Όχι) | Ναι→2.00 |
| **4.1** | ποσό + budget | ratio — ≤0.1→0; >0.6→12.00; γραμμική (`10+90·(ratio−0.1)/0.5`)·0.12 |
| **5.1** | ποσό + budget | ratio — ≤0.05→0; >0.2→12.00; γραμμική (`10+90·(ratio−0.05)/0.15`)·0.08 |
| **6.1** | combo (Ναι/Όχι) | Ναι→13.00 |
| **7.1** | combo (Ναι/Όχι) | Ναι→3.00 |

### Συνολική επιλεξιμότητα μοριοδότησης

`sum_total_moria()` → άθροισμα `Decimal` των 16 κριτηρίων. Αν **όλα** τα πεδία είναι κενά → άδειο string + clear `epilex_moria`.

`epilex_moria()` → χρωματισμένο badge:
- Κάποιο από τα 16 + το `budget` λείπει → άδειο (μπλε background)
- Total < 40 → **ΜΗ ΕΠΙΛΕΞΙΜΟΣ** (κόκκινο)
- Total ≥ 40 → **ΕΠΙΛΕΞΙΜΟΣ** (πράσινο)

---

## Database

### `database_manager.py` functions

| Function | Usage |
|----------|-------|
| `setup_database()` | Create tables + run migrations — called in MainWindow `__init__` |
| `_now_iso()` | Private helper: τρέχον timestamp σε ISO 8601 (`YYYY-MM-DD HH:MM:SS`) |
| `save_producer_basics(afm, name, surname, region)` | Insert or update producer + αυτόματα ανανεώνει `last_modified` |
| `save_scenario_data(afm, scenario, data)` | Save TA table (`'initial'` or `'future'`) |
| `save_eligibility_data(afm, data)` | Save eligibility answers (11-tuple: 10 πεδία + `eligibility_result`) |
| `save_moria_data(afm, data)` | Save moria answers (19-tuple: 16 ερωτήσεις + `budget_val` + `moria_val` + `moria_epileximos`) |
| `fetch_producer(afm)` | Returns `(name, surname, region)` or None |
| `fetch_entries(afm, scenario)` | Returns TA rows for a scenario |
| `fetch_eligibility(afm)` | Returns 11-tuple eligibility data |
| `fetch_moria(afm)` | Returns 19-tuple moria data |
| `fetch_all_producers()` | Returns all producers + `last_modified` (for arx_page & import conflict check). **ORDER BY p.afm ASC** — η αρχική στηρίζεται σε αυτή τη σειρά |
| `fetch_single_producer_row(afm)` | Same shape ως `fetch_all_producers` για 1 ΑΦΜ (χρήση: `upsert_producer_row`) |
| `delete_producer(afm)` | Διαγραφή παραγωγού — cascade σβήνει osde_entries / eligibility / moria |
| `delete_producer_entries(cursor, afm, scenario_type='initial')` | Helper: σβήνει `osde_entries` ενός παραγωγού για συγκεκριμένο scenario (χρησιμοποιείται στο _replace branch του import) |
| `import_producers_batch_transaction(data, progress_callback)` | Batch import με error recovery + αυτόματη ενημέρωση `last_modified` (INSERT για νέους, UPDATE για _replace) → returns `{total_success, failed}` |
| `to_float_or_empty(value)` / `to_int_or_empty(value)` | Helpers για ασφαλή cast από Excel/CSV cells σε number ή `""` |

### Schema

```sql
CREATE TABLE producers (
    afm           TEXT PRIMARY KEY,   -- ΑΦΜ (9 digits)
    first_name    TEXT,
    last_name     TEXT,
    region        TEXT,
    last_modified TEXT                -- ISO 8601 'YYYY-MM-DD HH:MM:SS' — timestamp τελευταίας αποθήκευσης/import
)

CREATE TABLE osde_entries (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    producer_afm      TEXT,    -- FK → producers.afm
    scenario_type     TEXT,    -- 'initial' or 'future'
    category_osde     TEXT,    -- col 0
    description       TEXT,    -- col 1
    typical_output    REAL,    -- col 2
    quantity          REAL,    -- col 3
    certification     TEXT,    -- col 4
    trees_over_4      INTEGER, -- col 5
    trees_under_4     INTEGER, -- col 6
    vine_over_3       INTEGER, -- col 7
    output_per_choice REAL,    -- col 8
    total_output      REAL,    -- col 10
    ta_productive     REAL,    -- col 11
    ta_plant          REAL,    -- col 12
    ta_animal         REAL,    -- col 13
    ta_bees           REAL,    -- col 14
    FOREIGN KEY (producer_afm) REFERENCES producers(afm) ON DELETE CASCADE
)

CREATE TABLE eligibility (
    producer_afm       TEXT PRIMARY KEY,
    q1 INTEGER, q2 TEXT, q3 TEXT, q4 TEXT, q5 TEXT, q6 TEXT, q7 TEXT, q8 TEXT, q9 TEXT,
    typical_output_val REAL,
    eligibility_result TEXT,   -- 'ΕΠΙΛΕΞΙΜΟΣ' / 'ΜΗ ΕΠΙΛΕΞΙΜΟΣ' / '' (combined result)
    FOREIGN KEY (producer_afm) REFERENCES producers(afm) ON DELETE CASCADE
)

CREATE TABLE moria (
    producer_afm TEXT PRIMARY KEY,
    q1_1 TEXT, q1_2 TEXT, q2_1 REAL, q2_2 REAL,
    q3_1_1 REAL, q3_1_2 TEXT, q3_1_3 TEXT, q3_1_4 TEXT,
    q3_2 TEXT, q3_3 TEXT, q3_4 TEXT, q3_5 TEXT,
    q4_1 REAL, q5_1 REAL, q6_1 TEXT, q7_1 TEXT,
    budget_val       REAL,
    moria_val        REAL,
    moria_epileximos TEXT,   -- 'ΕΠΙΛΕΞΙΜΟΣ' / 'ΜΗ ΕΠΙΛΕΞΙΜΟΣ' / ''
    FOREIGN KEY (producer_afm) REFERENCES producers(afm) ON DELETE CASCADE
)
```

> **Schema migrations**: Το `SCHEMA_VERSION = 0` (baseline). Για ασφαλείς αλλαγές (π.χ. προσθήκη στήλης) χρησιμοποιείται ο μηχανισμός `_run_migrations()` + `_add_column_if_missing()`. Bump `SCHEMA_VERSION` **μόνο** όταν προσθέσεις νέο migration step.

`fetch_entries` row order: `[id, producer_afm, scenario_type, category_osde, description, typical_output, quantity, certification, trees_over_4, trees_under_4, vine_over_3, output_per_choice, total_output, ta_productive, ta_plant, ta_animal, ta_bees]` (index 0–16)

Loading into table: `[[r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], "", r[12], r[13], r[14], r[15], r[16]] for r in rows]`

`fetch_all_producers` / `fetch_single_producer_row` row shape (9-tuple, index 0–8):
`(afm, first_name, last_name, moria_val, region, initial_ta, future_ta, combined_eligibility, last_modified)`

`fetch_eligibility` row shape (11-tuple): `(q1..q9, typical_output_val, eligibility_result)`

`fetch_moria` row shape (19-tuple): `(q1_1, q1_2, q2_1, q2_2, q3_1_1..q3_1_4, q3_2..q3_5, q4_1, q5_1, q6_1, q7_1, budget_val, moria_val, moria_epileximos)`

### Συμμετρία get/set/save/fetch

Τόσο για eligibility όσο και για moria, τα `get_*_data` (στη σελίδα), `set_*_data` (στη σελίδα), `save_*_data` (DB), και `fetch_*` (DB) χειρίζονται **το ίδιο tuple shape** (11 για eligibility, 19 για moria). Το τελευταίο πεδίο (`eligibility_result` / `moria_epileximos`) ξαναυπολογίζεται πάντα από signals μέσω `recalculate_all_results()` / `recalculate_all_results_moria()` όταν γίνει search/load, αλλά αποθηκεύεται στη βάση για να μπορεί το `fetch_all_producers` να συνδυάσει eligibility + moria σε ένα `combined_eligibility` (στήλη 7 της αρχικής).

---

## Πίνακας αρχικής σελίδας (`page_arxiki`)

11 στήλες:

| # | Header | Delegate / Fill |
|---|--------|-----------------|
| 0 | ΑΦΜ | `fetch_all_producers()[0]` |
| 1 | Όνομα | `[1]` |
| 2 | Επώνυμο | `[2]` |
| 3 | Περιφέρεια | `[4]` (NULLIF '--Επιλέξτε') |
| 4 | Αρχική ΤΑ | `[5]` (MAX total_output scenario='initial') |
| 5 | Μελλοντική ΤΑ | `[6]` (MAX total_output scenario='future') |
| 6 | Μόρια | `[3]` (moria.moria_val) |
| 7 | Επιλεξιμότητα | `[7]` (combined: eligibility_result + moria_epileximos) — bold/χρωματισμός στα 'ΕΠΙΛΕΞΙΜΟΣ' (#2E7D32) / 'ΜΗ ΕΠΙΛΕΞΙΜΟΣ' (#C62828) |
| 8 | Τελευταία Επεξεργασία | `[8]` (last_modified) — formatted via `_format_timestamp()` από `YYYY-MM-DD HH:MM:SS` → `DD/MM/YYYY HH:MM` |
| 9 | Επ/σία | `EditButtonDelegate` |
| 10 | Διαγραφή | `DeleteButtonDelegate` |

- **`load_producers()`**: πλήρες reset του model (clear + bulk append με blocked signals).
- **`upsert_producer_row(afm)`**: στοχευμένη ανανέωση 1 γραμμής — καλείται μετά από `handle_save` αποφεύγοντας πλήρες reload. Για **νέο** AFM γίνεται **sorted insert** (lexicographic compare 9-ψήφιων ΑΦΜ) ώστε να διατηρείται η αύξουσα σειρά του `fetch_all_producers`.

---

## Constants (`utils/excel_loader.py`)

| Constant | Usage |
|----------|-------|
| `PERIFERIES` | Region list for combo_periferia |
| `AEGEAN_PERIFERIES` | `{Βόρειο Αιγαίο, Νότιο Αιγαίο, Κρήτη}` — selects aegean column of ta.xlsx |
| `ISLANDS` | `{Νότιο Αιγαίο, Βόρειο Αιγαίο, Ιόνια Νησιά}` — eligibility Q7 threshold 8000 |
| `LOCK_AMPELI_NORM` | Categories that enable col 7 (vine >3yr) |
| `LOCK_TREES_NORM` | Categories that lock cols 5 & 6 (trees) |
| `FMZ_ZWIKI_NORM` | Animal production categories → col 13 |
| `FMZ_MELISSES_NORM` | Bee/silkworm categories → col 14 |
| `PARAGWGIKA_NORM` | Productive animal subcategories |
| `PARAGWGIKA_CAT_NORM` | Productive animal categories |
| `DEFAULT` | Default combobox value ("--Επιλέξτε") |
| `NORM_YES` | Normalized "ναι" — used in CSV import for ΕΠΙΣΠΟΡΗ |
| `norm(text)` | Normalizes text (lowercase, strip, etc.) |
| `in_norm_set(text, norm_set)` | Checks if text belongs to a normalized set |
| `resource_path(relative_path)` | Returns absolute path — works in both dev and frozen PyInstaller exe |

---

## Import / Export

### Import (`import_data_from_file`)
- Formats: **Excel (.xlsx)** or **CSV**
- Loads: producer info (page 1) + initial TA (μόνο sheet "TA Αρχικής")
- Checks for AFM conflicts → `ImportConflictDialog`
- After import checks if crops exist in ta.xlsx → `MissingCategoriesDialog`
- `_pending_ta_warning_message` / `_pending_mel_warning_message` shown when user navigates to page 2 / 3
- **Calculated fields** (ΤΑ, totals) are NOT imported — always recalculated from code
- **Canonicalization** (`_canonicalize_entry_row`): πριν την validation, οι τιμές `category_osde` / `description` ελέγχονται σε normalized μορφή (`norm()`) έναντι των ζευγαριών του ta.xlsx. Αν βρεθεί match (πρώτα ολόκληρο pair, fallback μόνο cat), αντικαθιστώνται in-place με την κανονική γραφή — επιτρέπει στο χρήστη να έχει διαφορές σε case/κενά/τόνους στο αρχείο import χωρίς να σπάει η αντιστοίχιση με την `value_mapping`.
- **Security validation** (`_validate_import_row`):
  - Magic-bytes check για .xlsx (αρχίζει με `PK\x03\x04`) — αποτρέπει spoofed extensions
  - Max 200 χαρακτήρες σε `category_osde` / `description` (constants `_MAX_TEXT_LEN`)
  - `quantity` ∈ [0, 9999999.99] με max 2 δεκαδικά
  - `trees_over_4` / `trees_under_4` ∈ [0, 9999999], **όχι δεκαδικά** (12.0 ΟΚ από Excel, 12.5 fail)
  - `certification` ∈ `_ALLOWED_CERTS = {"--Επιλέξτε", "Συμβατικά", "Βιολογικά", "Ολοκληρωμένη", "ΠΟΠ/ΠΓΕ"}` (μόνο Excel, υποχρεωτικό)
  - `vine_over_3` ∈ `{"--Επιλέξτε", "Ναι", "Όχι"}` (Excel) ή `{"1", "0"}` (CSV) — μόνο για `LOCK_AMPELI_NORM`
  - Σφάλμα → `ValueError("Μη έγκυρα δεδομένα")` και η γραμμή απορρίπτεται

**CSV specifics:**
- Encoding auto-detect: `utf-8-sig`, `utf-8`, `cp1253`, `iso-8859-7`, `latin1`
- Delimiter auto-detect: `,` or `;`
- `ΕΠΙΣΠΟΡΗ` validation: accepts μόνο `''` / `ΝΑΙ` / `ΟΧΙ`. Γραμμές με `ΝΑΙ` παραλείπονται (επισπορά). Οποιαδήποτε άλλη τιμή → `ValueError("Μη έγκυρα δεδομένα")` και απορρίπτεται όλο το import.
- CSV column mapping: `ΑΦΜ`, `ΟΝΟΜΑ`, `ΕΠΩΝΥΜΟ`, `ΚΑΤΗΓΟΡΙΑ`, `ΠΕΡΙΓΡΑΦΗ`, `ΕΚΤΑΣΗ_ΖΩΑ`, `ΔΕΝΤΡΑ_ΑΝΩ_4_ΕΤΩΝ`, `ΔΕΝΤΡΑ_ΚΑΤΩ_4_ΕΤΩΝ`, `ΑΜΠΕΛ_3_ΕΤΩΝ` (`1`→"Ναι", `0`→"Όχι")

### Export ΤΑ παραγωγού (`export_table_to_excel` στο `main_window.py`)
- Excel with **3 sheets**: "TA Αρχικής", "ΤΑ Μελλοντικής", "Επιλεξιμότητα"
- Col 7 (vine) exported only for `LOCK_AMPELI_NORM`, otherwise empty
- Numeric columns (2,3,5,6,8,9,10,11,12,13,14) → float or None
- The same file can be re-imported (bidirectional format)

### Export λίστας παραγωγών (`export_table_to_xlsx` στο `page_arxiki.py`)
- Single sheet "Εγγραφές" με header A1 (ημερομηνία εκτύπωσης) + bold headers γραμμή 3
- Στήλες εξαγωγής: **ΑΦΜ, Όνομα, Επώνυμο, Περιφέρεια, Αρχική ΤΑ, Μελλοντική ΤΑ, Μόρια, Επιλεξιμότητα, Τελευταία Επεξεργασία** (0–8 του model)
- Numeric cols (4, 5, 6 — δηλ. Αρχική/Μελλοντική ΤΑ & Μόρια) → float 2 δεκαδικών
- Το `Τελευταία Επεξεργασία` εξάγεται ως string στη μορφή UI (`DD/MM/YYYY HH:MM`)

---

## Πριν από αλλαγές σε υπάρχοντα symbols

Πριν αλλάξεις signature ή συμπεριφορά οποιουδήποτε υπάρχοντος symbol:

1. Τρέξε `Grep` για το όνομά του σε **όλο το project** (όχι μόνο στα αρχεία που σου έδωσε ο χρήστης).
2. Άνοιξε κάθε σημείο όπου χρησιμοποιείται και κατάλαβε τι περιμένει από αυτό.
3. Αν αλλάξεις signature (π.χ. προσθαφαίρεση παραμέτρου), ενημέρωσε **όλα** τα σημεία χρήσης στην ίδια αλλαγή.
4. Αν αλλάξεις συμπεριφορά (τι κάνει εσωτερικά), εξέτασε ξεχωριστά κάθε σημείο χρήσης για το αν εξαρτιόταν από την παλιά συμπεριφορά.

**Ισχύει για**: functions, methods, classes, constants, signal connections, table column indices, DB schema, tuple shapes που επιστρέφουν τα `fetch_*` helpers.

---

## Conventions & Rules

- **Python 3.8 only** — no `match/case`, no 3.10+ syntax or type hints
- **PySide2 only** — never PyQt5/PyQt6/PySide6
- **CSS styling only inside `.ui` files** — no inline Python styling except where required (e.g. delegates)
- **UI language: Greek** everywhere
- Read-only/auto cells: background `#E3F2FD`
- Always use `blockSignals(True/False)` during bulk updates
- Always use `resource_path()` for all file paths
- Minimum window size: 900×650 (`_setup_minimum_sizes`)
- `lineEdit_afm` has `QRegExpValidator` accepting only 0–9 digits (max 9)
- **Σύντομα σχόλια** στον κώδικα — μέχρι 1 γραμμή. Αποφυγή πολυσέλιδων docstrings ή multi-line comment blocks.

## Avoid

- Do not use Python features beyond 3.8
- Do not replace PySide2 with another GUI library
- Do not install new libraries without asking first
- Do not modify the database schema without discussion
- Do not use absolute paths — always `resource_path()`
- Do not ignore `_updating` flags or `blockSignals` in calculations — causes infinite loops
- Do not add calculated fields to import (ΤΑ, totals) — they are always recalculated from code
- Do not update the `producers` table (name/surname/region) during import replace — when the user chooses "Αντικατάσταση" for a conflicting AFM, only the `osde_entries` are deleted and re-imported; the producer's basic info intentionally stays unchanged. This is by design.
- **Εξαίρεση**: το `last_modified` **ενημερώνεται** και στο _replace branch του import — η αντικατάσταση είναι μια τροποποίηση και πρέπει να καταγραφεί. Βλ. `import_producers_batch_transaction`.
- Do not add timestamp logic to `save_eligibility_data` / `save_moria_data` / `save_scenario_data` — το `handle_save` καλεί πάντα πρώτα `save_producer_basics` που ενημερώνει μόνο του το `last_modified`. Μία πηγή αλήθειας.
- **ΜΗΝ χρησιμοποιείς `float` στους moria υπολογισμούς** — η σελίδα δουλεύει αποκλειστικά με `Decimal` μέσω `utils/decimal_utils.py`. Το default `round()` της Python και το `Decimal.quantize` χωρίς `rounding=ROUND_HALF_UP` δίνουν banker's rounding (π.χ. `2.675 → 2.67` αντί `2.68`). Πάντα `q2()` / `fmt2()`.
- **ΜΗΝ αφαιρέσεις το `viewportEvent` override στο `ClearableTableView`** — μπλοκάρει hover-only mouse moves στις combo στήλες `(0, 1, 4, 7)`. Χωρίς αυτό, τα persistent combos σε αυτές τις στήλες χάνουν focus όταν ο cursor διασχίζει το gridline και ο χρήστης πληκτρολογεί σε λάθος γραμμή. Drag events (button held) και events σε col 9 (delete btn) **πρέπει** να περνάνε — αλλιώς χαλάει το hover effect του button (State_MouseOver μένει stuck). Το `setMouseTracking(True)` εξαρτάται από αυτό το filter — αν προστεθούν νέες combo στήλες, βάλε τις στη blocklist.

---

## Run & Build

```bash
# Install dependencies
pip install -r requirements.txt

# Run in development
python main.py

# Build Windows executable
pyinstaller Sxedia_v1.5.spec

# Build Windows installer (μετά το pyinstaller)
ISCC.exe installer\Sxedia_installer.iss
# ή άνοιξε το .iss στον Inno Setup Compiler και πάτα F9
# → output: installer\output\Sxedia_vX.Y_Setup.exe
```

### Versioning installer

Όταν κάνεις νέα έκδοση (v1.6, v2.0, ...), στο [installer/Sxedia_installer.iss](installer/Sxedia_installer.iss) **άλλαξε ΜΟΝΟ**:
- `MyAppVersion` (π.χ. `"2.0.0"`)
- `MyAppExeName` (π.χ. `"Sxedia_v2.0.exe"`)
- `OutputBaseFilename` (π.χ. `"Sxedia_v2.0_Setup"`)

**ΜΗΝ αλλάξεις ΠΟΤΕ το `AppId`** — είναι το μοναδικό identifier της εφαρμογής στο Windows registry. Αν αλλάξει, οι χρήστες θα έχουν παράλληλα v1 + v2 εγκατεστημένες.

Η βάση SQLite (`%LOCALAPPDATA%\OsdeCalculatorApp_3\osde_app_3.db`) **δεν** διαχειρίζεται από τον installer — παραμένει μεταξύ install/uninstall. Schema migrations γίνονται μέσω `_run_migrations()` στο [database_manager.py](database_manager.py).

## Dependencies

See `requirements.txt`:
- `PySide2==5.15.2.1` (+ `shiboken2==5.15.2.1`)
- `openpyxl==3.1.5` (+ `et_xmlfile==2.0.0`)
- `pyinstaller==6.18.0` (+ `pyinstaller-hooks-contrib==2026.0`, `altgraph`, `pefile`, `pywin32-ctypes`)
- Standard transitive: `importlib_metadata`, `packaging`, `zipp`

## Testing

Unit tests στον φάκελο `tests/` (πλαίσιο: `unittest` της βιβλιοθήκης). Τα formulas (TA & moria scoring) είναι extracted ως pure functions χωρίς Qt dependency, ώστε να τρέχουν χωρίς QApplication boot.

| File | Σκοπός |
|------|--------|
| `tests/test_calculations.py` | TA formulas: `typiki_apodosi`, `ta_paragwgikwn`, `total_fzm` routing, biologic %, eligibility Q7 |
| `tests/test_moria_scoring.py` | Pure functions για κάθε `moria_*` κριτήριο + HALF_UP rounding regression tests |
| `tests/test_database_manager.py` | CRUD, migrations, batch import (temp SQLite μέσω `_TempDBMixin`) |
| `tests/test_excel_loader.py` | `norm`, `in_norm_set`, `contains_norm_keyword`, `resource_path`, σταθερές |
| `tests/test_import_security.py` | Edge/security cases για CSV & Excel parse μέσω mock του `MainWindow` + canonicalization tests (`TestCanonicalizeEntryRow`, `TestCanonicalizationInImport`) |

```bash
# Run all tests
python -m unittest discover tests

# Run a single file
python -m unittest tests.test_calculations
```

Σημείωση: για UI/integration σενάρια εξακολουθεί να γίνεται manual testing στην εφαρμογή.
