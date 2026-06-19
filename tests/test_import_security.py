"""
Security/edge case tests για το import flow (xlsx — η web εφαρμογή δεν υποστηρίζει CSV).

Καλεί απευθείας τις συναρτήσεις του utils/import_utils.py
(read_excel_file, _validate_import_row, _canonicalize_entry_row,
build_canon_dicts, build_region_canon) — δηλ. τον πραγματικό κώδικα
που χρησιμοποιεί το /api/import/parse, χωρίς mocks του desktop MainWindow.
"""
import os
import sys
import tempfile
import unittest

import openpyxl

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.import_utils import (
    build_canon_dicts, build_region_canon,
    _canonicalize_entry_row, _validate_import_row, read_excel_file,
)
from utils.excel_loader import load_excel_data, resource_path, PERIFERIES, LOCK_AMPELI

SHEET_NAME = "Τυπική Απόδοση"

HEADERS = [
    "ΑΦΜ", "Όνομα", "Επώνυμο", "Περιφέρεια",
    "Κατηγορία ΟΣΔΕ", "Περιγραφή",
    "Έκταση/Αριθμός ζώων", "Βιολογικά",
    "Δένδρα >=4 ετών", "Δένδρα <4 ετών", "Αμπέλι >3 ετών",
]


def _row(afm="123456789", name="Maria", surname="Korre", region="Αττική",
         cat="Cat", desc="Desc", qty=1, cert="Συμβατικά",
         trees_over=None, trees_under=None, vine=None):
    """Μία γραμμή στη σειρά του HEADERS."""
    return [afm, name, surname, region, cat, desc, qty, cert,
            trees_over, trees_under, vine]


def _write_xlsx(rows, sheet_name=SHEET_NAME, headers=None):
    fd, path = tempfile.mkstemp(suffix=".xlsx")
    os.close(fd)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_name
    ws.append(headers if headers is not None else HEADERS)
    for row in rows:
        ws.append(row)
    wb.save(path)
    wb.close()
    return path


class _CanonMixin:
    """Φορτώνει τα reverse-lookup caches από το πραγματικό data/ta.xlsx."""

    @classmethod
    def setUpClass(cls):
        mapping, value_mapping = load_excel_data(resource_path("data/ta.xlsx"))
        cls.canon_pair, cls.canon_cat, cls.valid_cats, cls.valid_descs = (
            build_canon_dicts(value_mapping))
        cls.canon_region = build_region_canon(PERIFERIES)
        cls.sample_cat, cls.sample_desc = next(iter(value_mapping.keys()))

    def setUp(self):
        self._tmp_files = []

    def tearDown(self):
        for p in self._tmp_files:
            try:
                os.unlink(p)
            except OSError:
                pass

    def _track(self, path):
        self._tmp_files.append(path)
        return path

    def _read(self, path):
        with open(path, "rb") as f:
            file_bytes = f.read()
        return read_excel_file(
            file_bytes,
            self.canon_pair, self.canon_cat, self.valid_cats, self.valid_descs,
            self.canon_region,
        )


# ─────────────────────────────────────────────────────────────
# Magic bytes / sheet / header validation
# ─────────────────────────────────────────────────────────────

class TestFileAndHeaderValidation(_CanonMixin, unittest.TestCase):

    def test_non_xlsx_bytes_raises(self):
        """Μη-xlsx bytes (λάθος magic number) → ValueError, καμία επεξεργασία."""
        with self.assertRaises(ValueError):
            read_excel_file(b"NOT A VALID XLSX \x00\x01\x02\xff",
                             self.canon_pair, self.canon_cat,
                             self.valid_cats, self.valid_descs, self.canon_region)

    def test_missing_sheet_raises(self):
        path = self._track(_write_xlsx([], sheet_name="WrongSheet"))
        with self.assertRaises(ValueError) as ctx:
            self._read(path)
        self.assertIn("Τυπική Απόδοση", str(ctx.exception))

    def test_missing_required_column_raises(self):
        """Λείπει η στήλη Περιφέρεια → ValueError με αναφορά στη λείπουσα στήλη."""
        headers = [h for h in HEADERS if h != "Περιφέρεια"]
        path = self._track(_write_xlsx([], headers=headers))
        with self.assertRaises(ValueError) as ctx:
            self._read(path)
        self.assertIn("Περιφέρεια", str(ctx.exception))

    def test_empty_sheet_returns_empty(self):
        """Header μόνο, καμία γραμμή δεδομένων → άδειο αποτέλεσμα, καμία exception."""
        path = self._track(_write_xlsx([]))
        producers, skipped = self._read(path)
        self.assertEqual(producers, [])
        self.assertEqual(skipped, [])


# ─────────────────────────────────────────────────────────────
# AFM validation & grouping
# ─────────────────────────────────────────────────────────────

class TestAfmValidationAndGrouping(_CanonMixin, unittest.TestCase):

    def test_valid_afm_accepted(self):
        path = self._track(_write_xlsx([_row(afm="123456789")]))
        producers, skipped = self._read(path)
        self.assertEqual(len(producers), 1)
        self.assertEqual(producers[0]["afm"], "123456789")
        self.assertEqual(skipped, [])

    def test_afm_too_short_skipped(self):
        path = self._track(_write_xlsx([_row(afm="123")]))
        producers, skipped = self._read(path)
        self.assertEqual(producers, [])
        self.assertIn("123", skipped)

    def test_afm_too_long_skipped(self):
        path = self._track(_write_xlsx([_row(afm="123456789012")]))
        producers, skipped = self._read(path)
        self.assertEqual(producers, [])
        self.assertEqual(len(skipped), 1)

    def test_empty_afm_skipped(self):
        path = self._track(_write_xlsx([_row(afm="")]))
        producers, skipped = self._read(path)
        self.assertEqual(producers, [])

    def test_duplicate_afm_groups_rows(self):
        """Ίδιο ΑΦΜ σε πολλές γραμμές → ομαδοποιούνται κάτω από έναν παραγωγό."""
        rows = [
            _row(afm="123456789", cat="Cat1", desc="Desc1", qty=1),
            _row(afm="123456789", cat="Cat2", desc="Desc2", qty=2),
            _row(afm="123456789", cat="Cat3", desc="Desc3", qty=3),
        ]
        path = self._track(_write_xlsx(rows))
        producers, skipped = self._read(path)
        self.assertEqual(len(producers), 1)
        self.assertEqual(len(producers[0]["rows"]), 3)

    def test_mixed_valid_and_invalid_afms(self):
        rows = [
            _row(afm="abc"),
            _row(afm=""),
            _row(afm="123456789"),
        ]
        path = self._track(_write_xlsx(rows))
        producers, skipped = self._read(path)
        self.assertEqual(len(producers), 1)
        self.assertEqual(producers[0]["afm"], "123456789")
        self.assertEqual(len(skipped), 2)


# ─────────────────────────────────────────────────────────────
# Region validation (υποχρεωτική στήλη, norm-based canon)
# ─────────────────────────────────────────────────────────────

class TestRegionValidation(_CanonMixin, unittest.TestCase):

    def test_valid_region_canonicalized(self):
        path = self._track(_write_xlsx([_row(region="Αττική")]))
        producers, _ = self._read(path)
        self.assertEqual(producers[0]["region"], "Αττική")

    def test_region_case_and_accent_insensitive(self):
        path = self._track(_write_xlsx([_row(region="κρητη")]))
        producers, _ = self._read(path)
        self.assertEqual(producers[0]["region"], "Κρήτη")

    def test_empty_region_defaults_to_select(self):
        """Κενό κελί περιφέρειας → '--Επιλέξτε' (έγκυρο μέλος του PERIFERIES)."""
        path = self._track(_write_xlsx([_row(region="")]))
        producers, _ = self._read(path)
        self.assertEqual(producers[0]["region"], "--Επιλέξτε")

    def test_invalid_region_raises(self):
        """Περιφέρεια που δεν ταιριάζει με καμία επιλογή → ValueError, ολόκληρο το αρχείο άκυρο."""
        path = self._track(_write_xlsx([_row(region="Ανύπαρκτη Περιφέρεια Χ")]))
        with self.assertRaises(ValueError):
            self._read(path)


# ─────────────────────────────────────────────────────────────
# Security: injection-like strings stored as plain text
# ─────────────────────────────────────────────────────────────

class TestInjectionStringsStoredAsText(_CanonMixin, unittest.TestCase):

    def test_sql_injection_in_name(self):
        injection = "'; DROP TABLE producers; --"
        path = self._track(_write_xlsx([_row(name=injection)]))
        producers, _ = self._read(path)
        self.assertEqual(producers[0]["name"], injection)

    def test_sql_injection_in_category(self):
        injection = "Robert'); DROP TABLE Students;--"
        path = self._track(_write_xlsx([_row(cat=injection)]))
        producers, _ = self._read(path)
        self.assertEqual(producers[0]["rows"][0]["category_osde"], injection)

    def test_path_traversal_in_surname(self):
        traversal = "../../../etc/passwd"
        path = self._track(_write_xlsx([_row(surname=traversal)]))
        producers, _ = self._read(path)
        self.assertEqual(producers[0]["surname"], traversal)

    def test_unicode_emoji_preserved(self):
        path = self._track(_write_xlsx([_row(name="Νίκος😀", surname="Παπαδόπουλος🎉")]))
        producers, _ = self._read(path)
        self.assertEqual(producers[0]["name"], "Νίκος😀")
        self.assertEqual(producers[0]["surname"], "Παπαδόπουλος🎉")


# ─────────────────────────────────────────────────────────────
# Calculated fields are never trusted from the import file
# ─────────────────────────────────────────────────────────────

class TestCalculatedFieldsAlwaysEmpty(_CanonMixin, unittest.TestCase):

    def test_calculated_fields_blank_regardless_of_input(self):
        path = self._track(_write_xlsx([_row()]))
        producers, _ = self._read(path)
        entry = producers[0]["rows"][0]
        for field in ("typical_output", "output_per_choice", "total_output",
                      "ta_productive", "ta_plant", "ta_animal", "ta_bees"):
            self.assertEqual(entry[field], "",
                             "{} πρέπει να είναι κενό (recalculated server-side)".format(field))


# ─────────────────────────────────────────────────────────────
# Performance — πολλές γραμμές/παραγωγοί
# ─────────────────────────────────────────────────────────────

class TestPerformance(_CanonMixin, unittest.TestCase):

    def test_many_rows_many_producers(self):
        rows = [
            _row(afm=str(100000000 + i).zfill(9), name="N{}".format(i),
                 surname="S{}".format(i), qty=1)
            for i in range(2000)
        ]
        path = self._track(_write_xlsx(rows))
        producers, skipped = self._read(path)
        self.assertEqual(len(producers), 2000)
        self.assertEqual(skipped, [])


# ─────────────────────────────────────────────────────────────
# _validate_import_row — strict validation rules
# ─────────────────────────────────────────────────────────────

class TestValidateImportRow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _, value_mapping = load_excel_data(resource_path("data/ta.xlsx"))
        _, _, cls.valid_cats, cls.valid_descs = build_canon_dicts(value_mapping)

    def _row(self, **kwargs):
        defaults = {
            'category_osde': 'Cat',
            'description': 'Desc',
            'quantity': '1',
            'trees_over_4': '',
            'trees_under_4': '',
            'vine_over_3': '',
            'certification': 'Συμβατικά',
        }
        defaults.update(kwargs)
        return defaults

    def _validate(self, row):
        _validate_import_row(row, self.valid_cats, self.valid_descs)

    # — Quantity range/precision —

    def test_quantity_negative_raises(self):
        with self.assertRaises(ValueError):
            self._validate(self._row(quantity='-1'))

    def test_quantity_over_max_raises(self):
        with self.assertRaises(ValueError):
            self._validate(self._row(quantity='99999999'))

    def test_quantity_three_decimals_raises(self):
        with self.assertRaises(ValueError):
            self._validate(self._row(quantity='1.234'))

    def test_quantity_two_decimals_ok(self):
        self._validate(self._row(quantity='12.34'))  # δεν σηκώνει

    def test_quantity_comma_decimal_ok(self):
        self._validate(self._row(quantity='12,34'))

    def test_quantity_non_numeric_raises(self):
        with self.assertRaises(ValueError):
            self._validate(self._row(quantity='abc'))

    def test_quantity_empty_ok(self):
        self._validate(self._row(quantity=''))

    # — Trees: integer-only —

    def test_trees_decimal_raises(self):
        with self.assertRaises(ValueError):
            self._validate(self._row(trees_over_4='12.5'))

    def test_trees_integer_ok(self):
        self._validate(self._row(trees_over_4='12', trees_under_4='3'))

    def test_trees_excel_float_int_ok(self):
        """Excel μπορεί να περάσει 12.0 (float χωρίς δεκαδικό μέρος) — γίνεται δεκτό."""
        self._validate(self._row(trees_over_4='12.0'))

    def test_trees_negative_raises(self):
        with self.assertRaises(ValueError):
            self._validate(self._row(trees_over_4='-5'))

    def test_trees_over_max_raises(self):
        with self.assertRaises(ValueError):
            self._validate(self._row(trees_over_4='99999999'))

    # — Certification (whitelist, πάντα ελέγχεται) —

    def test_cert_empty_raises(self):
        with self.assertRaises(ValueError):
            self._validate(self._row(certification=''))

    def test_cert_invalid_raises(self):
        with self.assertRaises(ValueError):
            self._validate(self._row(certification='ΑΛΛΟ'))

    def test_cert_valid_ok(self):
        for c in ("--Επιλέξτε", "Συμβατικά", "Βιολογικά", "Ολοκληρωμένη", "ΠΟΠ/ΠΓΕ"):
            self._validate(self._row(certification=c))

    # — Vine values (μόνο για LOCK_AMPELI κατηγορίες) —

    def test_vine_invalid_raises_for_ampeli_category(self):
        cat = next(iter(LOCK_AMPELI))
        with self.assertRaises(ValueError):
            self._validate(self._row(category_osde=cat, vine_over_3='maybe'))

    def test_vine_valid_ok_for_ampeli_category(self):
        cat = next(iter(LOCK_AMPELI))
        for v in ("--Επιλέξτε", "Ναι", "Όχι"):
            self._validate(self._row(category_osde=cat, vine_over_3=v))

    def test_vine_not_checked_for_non_ampeli_category(self):
        """Εκτός LOCK_AMPELI, οποιαδήποτε τιμή vine_over_3 περνάει (δεν ελέγχεται)."""
        self._validate(self._row(category_osde='ΕΛΑΙΩΝΕΣ', vine_over_3='garbage'))

    # — Text length on unknown category/description —

    def test_unknown_category_under_max_len_ok(self):
        self._validate(self._row(category_osde='ΆΓΝΩΣΤΗ ΚΑΤΗΓΟΡΙΑ' * 5))

    def test_unknown_category_over_max_len_raises(self):
        with self.assertRaises(ValueError):
            self._validate(self._row(category_osde='X' * 201))

    def test_unknown_description_over_max_len_raises(self):
        with self.assertRaises(ValueError):
            self._validate(self._row(description='Y' * 201))


# ─────────────────────────────────────────────────────────────
# _canonicalize_entry_row — reverse lookup σε ta.xlsx
# ─────────────────────────────────────────────────────────────

class TestCanonicalizeEntryRow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _, value_mapping = load_excel_data(resource_path("data/ta.xlsx"))
        cls.canon_pair, cls.canon_cat, _, _ = build_canon_dicts(value_mapping)
        cls.sample_cat, cls.sample_desc = next(iter(value_mapping.keys()))

    def _canon(self, row):
        _canonicalize_entry_row(row, self.canon_pair, self.canon_cat)
        return row

    def test_empty_cat_no_op(self):
        row = self._canon({'category_osde': '', 'description': 'whatever'})
        self.assertEqual(row['category_osde'], '')
        self.assertEqual(row['description'], 'whatever')

    def test_canonical_pair_unchanged(self):
        row = self._canon({'category_osde': self.sample_cat, 'description': self.sample_desc})
        self.assertEqual(row['category_osde'], self.sample_cat)
        self.assertEqual(row['description'], self.sample_desc)

    def test_lowercase_pair_canonicalized(self):
        row = self._canon({
            'category_osde': self.sample_cat.lower(),
            'description': self.sample_desc.lower(),
        })
        self.assertEqual(row['category_osde'], self.sample_cat)
        self.assertEqual(row['description'], self.sample_desc)

    def test_accentless_pair_canonicalized(self):
        import unicodedata

        def strip_accents(s):
            return ''.join(
                c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn'
            )
        row = self._canon({
            'category_osde': strip_accents(self.sample_cat),
            'description': strip_accents(self.sample_desc),
        })
        self.assertEqual(row['category_osde'], self.sample_cat)
        self.assertEqual(row['description'], self.sample_desc)

    def test_whitespace_padding_canonicalized(self):
        row = self._canon({
            'category_osde': '  ' + self.sample_cat + '   ',
            'description': self.sample_desc,
        })
        self.assertEqual(row['category_osde'], self.sample_cat)

    def test_unknown_pair_unchanged(self):
        row = self._canon({'category_osde': 'XXX_UNKNOWN', 'description': 'YYY_UNKNOWN'})
        self.assertEqual(row['category_osde'], 'XXX_UNKNOWN')
        self.assertEqual(row['description'], 'YYY_UNKNOWN')

    def test_known_cat_unknown_desc_canonicalizes_cat_only(self):
        row = self._canon({
            'category_osde': self.sample_cat.lower(),
            'description': 'UNKNOWN_VARIETY',
        })
        self.assertEqual(row['category_osde'], self.sample_cat)
        self.assertEqual(row['description'], 'UNKNOWN_VARIETY')

    def test_empty_desc_canonicalizes_cat(self):
        row = self._canon({'category_osde': self.sample_cat.lower(), 'description': ''})
        self.assertEqual(row['category_osde'], self.sample_cat)


# ─────────────────────────────────────────────────────────────
# Canonicalization integrated στο read_excel_file flow
# ─────────────────────────────────────────────────────────────

class TestCanonicalizationInImport(_CanonMixin, unittest.TestCase):

    def test_lowercase_cat_desc_canonicalized_via_import(self):
        path = self._track(_write_xlsx([
            _row(cat=self.sample_cat.lower(), desc=self.sample_desc.lower())
        ]))
        producers, _ = self._read(path)
        self.assertEqual(producers[0]["rows"][0]["category_osde"], self.sample_cat)
        self.assertEqual(producers[0]["rows"][0]["description"], self.sample_desc)


# ─────────────────────────────────────────────────────────────
# build_region_canon
# ─────────────────────────────────────────────────────────────

class TestBuildRegionCanon(unittest.TestCase):

    def test_maps_norm_to_canonical(self):
        canon = build_region_canon(PERIFERIES)
        for region in PERIFERIES:
            self.assertEqual(canon[_norm_region(region)], region)


def _norm_region(region):
    from utils.excel_loader import norm
    return norm(region)


if __name__ == "__main__":
    unittest.main(verbosity=2)
