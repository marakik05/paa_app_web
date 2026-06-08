"""
Security/edge case tests για το import flow (CSV & Excel).
Δοκιμάζει κακόβουλα/malformed αρχεία, edge cases σε δεδομένα και
απόδοση σε μεγάλα αρχεία.

Καλεί απευθείας τις parse methods _read_csv_file και _read_excel_file
του MainWindow μέσω mock self (αποφεύγει QApplication boot).
"""
import os
import sys
import csv
import tempfile
import unittest
from unittest.mock import MagicMock

import openpyxl

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main_window import MainWindow
from utils.excel_loader import norm


# Πλήρες CSV header (όλες οι 9 υποχρεωτικές στήλες). Με το strict header validation
# στο import, λείπουσα στήλη → ValueError πριν καν διαβαστούν γραμμές.
CSV_HEADER_FULL = (
    "ΑΦΜ,ΟΝΟΜΑ,ΕΠΩΝΥΜΟ,ΚΑΤΗΓΟΡΙΑ,ΠΕΡΙΓΡΑΦΗ,ΕΚΤΑΣΗ_ΖΩΑ,"
    "ΔΕΝΤΡΑ_ΑΝΩ_4_ΕΤΩΝ,ΔΕΝΤΡΑ_ΚΑΤΩ_4_ΕΤΩΝ,ΑΜΠΕΛ_3_ΕΤΩΝ"
)
CSV_HEADER_FULL_SEMI = CSV_HEADER_FULL.replace(",", ";")


def _csv_row(afm="123456789", name="Maria", surname="Korre",
             cat="Cat", desc="Desc", qty="1",
             trees_over="", trees_under="", vine="", sep=","):
    """Παράγει μία γραμμή CSV με όλα τα 9 πεδία."""
    return sep.join([afm, name, surname, cat, desc, str(qty),
                     str(trees_over), str(trees_under), str(vine)])


def _make_mock_main_window(with_validation=False, with_canonicalize=False):
    """Δημιουργεί mock MainWindow αρκετό για να τρέξουν οι _read_*_file.

    Αν `with_validation=True`, δένει και το `_validate_import_row` ώστε να
    μπορούν τα tests να ελέγξουν και τους κανόνες validation. Αλλιώς το
    `_validate_import_row` παραμένει MagicMock no-op (πέρασμα όλων).

    Αν `with_canonicalize=True`, δένει το `_canonicalize_entry_row` με τα
    reverse-lookup caches από το ta.xlsx.
    """
    mock = MagicMock()
    mock._parse_csv_entry_row = MainWindow._parse_csv_entry_row.__get__(mock, MainWindow)

    needs_mapping = with_validation or with_canonicalize
    if needs_mapping:
        from utils.excel_loader import load_excel_data, resource_path
        mapping, value_mapping = load_excel_data(resource_path("data/ta.xlsx"))
    else:
        mapping = value_mapping = None

    if with_validation:
        mock._valid_cats_cache = {norm(k) for k in mapping.keys()}
        mock._valid_descs_cache = {
            norm(v) for variants in mapping.values() for v in variants
        }
        mock._ALLOWED_CERTS = MainWindow._ALLOWED_CERTS
        mock._ALLOWED_VINE_XLSX = MainWindow._ALLOWED_VINE_XLSX
        mock._ALLOWED_VINE_CSV = MainWindow._ALLOWED_VINE_CSV
        mock._MAX_QUANTITY = MainWindow._MAX_QUANTITY
        mock._MAX_INT_7 = MainWindow._MAX_INT_7
        mock._MAX_TEXT_LEN = MainWindow._MAX_TEXT_LEN
        mock._validate_import_row = MainWindow._validate_import_row.__get__(mock, MainWindow)

    if with_canonicalize:
        mock._canonical_cat_by_norm = {norm(k): k for k in mapping.keys()}
        mock._canonical_pair_by_norm = {
            (norm(cat), norm(desc)): (cat, desc)
            for cat, desc in value_mapping.keys()
        }
        mock._canonicalize_entry_row = MainWindow._canonicalize_entry_row.__get__(mock, MainWindow)

    return mock


def read_csv(path, with_validation=False):
    return MainWindow._read_csv_file(_make_mock_main_window(with_validation), path)


def read_excel(path, with_validation=False):
    return MainWindow._read_excel_file(_make_mock_main_window(with_validation), path)


def _write_text(content, suffix=".csv", encoding="utf-8"):
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w", encoding=encoding, newline="") as f:
        f.write(content)
    return path


def _write_bytes(content, suffix=".csv"):
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "wb") as f:
        f.write(content)
    return path


def _write_xlsx(rows, sheet_name="TA Αρχικής", certification_default="Συμβατικά"):
    """Γράφει minimal XLSX με header + rows.
    Αν το cert column σε row είναι empty string, το συμπληρώνει με `certification_default`
    ώστε να περνάει το strict validation των Βιολογικών (μη-κενό whitelist).
    """
    fd, path = tempfile.mkstemp(suffix=".xlsx")
    os.close(fd)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_name
    headers = [
        "ΑΦΜ", "Όνομα", "Επώνυμο",
        "Κατηγορία ΟΣΔΕ", "Περιγραφή",
        "Έκταση/Αριθμός ζώων", "Βιολογικά",
        "Δένδρα >=4 ετών", "Δένδρα <4 ετών", "Αμπέλι >3 ετών",
    ]
    ws.append(headers)
    for row in rows:
        ws.append(row)
    wb.save(path)
    wb.close()
    return path


# ─────────────────────────────────────────────────────────────
# CSV — header validation (strict)
# ─────────────────────────────────────────────────────────────

class TestCSVHeaderValidation(unittest.TestCase):
    """Με το strict header validation, λείπουσα στήλη → ValueError πριν επεξεργαστούν γραμμές."""

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

    def test_empty_file_raises(self):
        """Κενό CSV → ValueError (κανένα header)."""
        path = self._track(_write_text(""))
        with self.assertRaises(ValueError):
            read_csv(path)

    def test_header_only_no_required_cols_raises(self):
        """Header με λίγες στήλες → ValueError."""
        path = self._track(_write_text("ΑΦΜ,ΟΝΟΜΑ,ΕΠΩΝΥΜΟ\n"))
        with self.assertRaises(ValueError):
            read_csv(path)

    def test_full_header_no_rows_returns_empty(self):
        """Πλήρες header χωρίς γραμμές → άδειο data, χωρίς exception."""
        path = self._track(_write_text(CSV_HEADER_FULL + "\n"))
        data, skipped = read_csv(path)
        self.assertEqual(data, [])
        self.assertEqual(skipped, [])

    def test_missing_one_required_col_raises(self):
        """Λείπει έστω και 1 από τις 9 υποχρεωτικές στήλες → ValueError."""
        # Λείπει η ΑΜΠΕΛ_3_ΕΤΩΝ
        header = (
            "ΑΦΜ,ΟΝΟΜΑ,ΕΠΩΝΥΜΟ,ΚΑΤΗΓΟΡΙΑ,ΠΕΡΙΓΡΑΦΗ,ΕΚΤΑΣΗ_ΖΩΑ,"
            "ΔΕΝΤΡΑ_ΑΝΩ_4_ΕΤΩΝ,ΔΕΝΤΡΑ_ΚΑΤΩ_4_ΕΤΩΝ"
        )
        path = self._track(_write_text(header + "\n"))
        with self.assertRaises(ValueError):
            read_csv(path)


# ─────────────────────────────────────────────────────────────
# CSV — edge cases σε δεδομένα γραμμών (πλήρες header)
# ─────────────────────────────────────────────────────────────

class TestCSVImportEdgeCases(unittest.TestCase):

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

    def test_binary_garbage(self):
        """Binary garbage → είτε ValueError (header missing) είτε γρήγορη αποτυχία, καμία injection."""
        path = self._track(_write_bytes(b"\x00\x01\x02\xff\xfe\xfd random binary"))
        # Με όλα τα encodings να αποτυγχάνουν να βρουν headers, αναμένουμε ValueError
        try:
            data, skipped = read_csv(path)
            # Αν δεν σήκωσε exception, τουλάχιστον δεν crashάρει και δίνει lists
            self.assertIsInstance(data, list)
            self.assertIsInstance(skipped, list)
        except (ValueError, csv.Error):
            pass  # acceptable fail-safe behavior

    def test_invalid_afm_short(self):
        """ΑΦΜ < 9 ψηφία → skipped, όχι crash."""
        content = CSV_HEADER_FULL + "\n" + _csv_row(afm="123") + "\n"
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(data, [])
        self.assertIn("123", skipped)

    def test_invalid_afm_long(self):
        """ΑΦΜ > 9 ψηφία → skipped."""
        content = CSV_HEADER_FULL + "\n" + _csv_row(afm="123456789012") + "\n"
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(data, [])
        self.assertEqual(len(skipped), 1)

    def test_valid_afm_passes(self):
        """Έγκυρος 9ψήφιος ΑΦΜ → καταχωρείται."""
        content = CSV_HEADER_FULL + "\n" + _csv_row(
            afm="123456789", name="Μαρία", surname="Κορρέ",
            cat="ΟΠΩΡΟΦΟΡΑ", desc="Πορτοκαλιά", qty="2.5"
        ) + "\n"
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["afm"], "123456789")

    def test_sql_injection_strings(self):
        """SQL-injection-like strings σε fields → δεν εκτελούνται, αποθηκεύονται ως text."""
        injection = "'; DROP TABLE producers; --"
        content = CSV_HEADER_FULL + "\n" + _csv_row(
            afm="123456789", name=injection, surname="Korre"
        ) + "\n"
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], injection)

    def test_path_traversal_strings(self):
        """Path-traversal-like strings σε fields → απλό text."""
        traversal = "../../../etc/passwd"
        content = CSV_HEADER_FULL + "\n" + _csv_row(
            afm="123456789", name="Maria", surname=traversal
        ) + "\n"
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["surname"], traversal)

    def test_extremely_long_field(self):
        """Field με 100KB string → δεν crashάρει."""
        long_value = "α" * (100 * 1024)
        # Quote το long field για να μη σπάσει το CSV parsing
        content = (
            CSV_HEADER_FULL + "\n"
            + '123456789,Maria,Korre,Cat,"' + long_value + '",1,,,\n'
        )
        path = self._track(_write_text(content))
        # Default csv field size limit μπορεί να είναι μικρό — sanity bump
        try:
            csv.field_size_limit(2 ** 31 - 1)
        except OverflowError:
            csv.field_size_limit(10 * 1024 * 1024)
        data, skipped = read_csv(path)
        self.assertIsInstance(data, list)

    def test_many_rows_performance(self):
        """10k γραμμές → επεξεργάζονται γρήγορα και σωστά."""
        rows = "\n".join(
            _csv_row(afm=str(100000000 + i).zfill(9),
                     name="Name{}".format(i),
                     surname="Surname{}".format(i))
            for i in range(10000)
        )
        content = CSV_HEADER_FULL + "\n" + rows + "\n"
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(len(data), 10000)
        self.assertEqual(skipped, [])

    def test_cp1253_encoding(self):
        """Greek CP1253 encoding → fallback λειτουργεί."""
        content = CSV_HEADER_FULL + "\n" + _csv_row(
            afm="123456789", name="Μαρία", surname="Κορρέ"
        ) + "\n"
        path = self._track(_write_text(content, encoding="cp1253"))
        data, skipped = read_csv(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["afm"], "123456789")

    def test_iso_8859_7_encoding(self):
        """ISO-8859-7 (Greek) encoding → fallback λειτουργεί."""
        content = CSV_HEADER_FULL + "\n" + _csv_row(
            afm="123456789", name="Νίκος", surname="Παπαδόπουλος"
        ) + "\n"
        path = self._track(_write_text(content, encoding="iso-8859-7"))
        data, skipped = read_csv(path)
        self.assertEqual(len(data), 1)

    def test_semicolon_delimiter(self):
        """CSV με ; delimiter (Excel Greek default) → auto-detection."""
        content = CSV_HEADER_FULL_SEMI + "\n" + _csv_row(
            afm="123456789", sep=";"
        ) + "\n"
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["afm"], "123456789")

    def test_decimal_comma_in_quantity(self):
        """Quantity με κόμμα ως decimal → μετατρέπεται σε τελεία."""
        content = CSV_HEADER_FULL_SEMI + "\n" + _csv_row(
            afm="123456789", qty="2,5", sep=";"
        ) + "\n"
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["rows"][0]["quantity"], "2.5")

    def test_epispora_yes_skips_row(self):
        """ΕΠΙΣΠΟΡΗ=ΝΑΙ → η γραμμή παραλείπεται."""
        # Προσθέτουμε στήλη ΕΠΙΣΠΟΡΗ extra (δεν ανήκει στις 9 υποχρεωτικές αλλά διαβάζεται)
        header = CSV_HEADER_FULL + ",ΕΠΙΣΠΟΡΗ"
        row_yes = _csv_row(afm="123456789", cat="Cat1", desc="Desc1", qty="1") + ",ΝΑΙ"
        row_no = _csv_row(afm="123456789", cat="Cat2", desc="Desc2", qty="2") + ",ΟΧΙ"
        content = header + "\n" + row_yes + "\n" + row_no + "\n"
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(len(data[0]["rows"]), 1)  # μόνο η ΟΧΙ

    def test_vine_over_3_mapping(self):
        """ΑΜΠΕΛ_3_ΕΤΩΝ: 1→'Ναι', 0→'Όχι'."""
        content = (
            CSV_HEADER_FULL + "\n"
            + _csv_row(afm="123456789", cat="Αμπέλι", desc="Σταφύλι", qty="1", vine="1") + "\n"
            + _csv_row(afm="123456789", cat="Αμπέλι", desc="Σταφύλι2", qty="2", vine="0") + "\n"
        )
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(data[0]["rows"][0]["vine_over_3"], "Ναι")
        self.assertEqual(data[0]["rows"][1]["vine_over_3"], "Όχι")

    def test_null_bytes_in_content(self):
        """Null bytes στο περιεχόμενο → handled gracefully."""
        # Πλήρες header σε bytes + γραμμή με null byte στο όνομα
        path = self._track(_write_bytes(
            b"\xef\xbb\xbf"  # UTF-8 BOM
            + CSV_HEADER_FULL.encode("utf-8") + b"\n"
            + b"123456789,Mar\x00ia,Korre,Cat,Desc,1,,,\n"
        ))
        try:
            data, skipped = read_csv(path)
            self.assertIsInstance(data, list)
        except (csv.Error, ValueError):
            pass  # acceptable

    def test_unicode_emojis_in_fields(self):
        """Unicode emojis/symbols → handled."""
        content = CSV_HEADER_FULL + "\n" + _csv_row(
            afm="123456789", name="😀🎉", surname="💀⚡"
        ) + "\n"
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "😀🎉")

    def test_duplicate_afm_groups_rows(self):
        """Ίδιος ΑΦΜ σε πολλές γραμμές → ομαδοποιούνται."""
        content = (
            CSV_HEADER_FULL + "\n"
            + _csv_row(afm="123456789", cat="Cat1", desc="Desc1", qty="1") + "\n"
            + _csv_row(afm="123456789", cat="Cat2", desc="Desc2", qty="2") + "\n"
            + _csv_row(afm="123456789", cat="Cat3", desc="Desc3", qty="3") + "\n"
        )
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(len(data[0]["rows"]), 3)

    def test_nonexistent_file(self):
        """Path που δεν υπάρχει → δεν crashάρει, επιστρέφει empty."""
        data, skipped = read_csv("C:\\does\\not\\exist\\file.csv")
        self.assertEqual(data, [])


# ─────────────────────────────────────────────────────────────
# XLSX — edge cases
# ─────────────────────────────────────────────────────────────

class TestExcelImportEdgeCases(unittest.TestCase):

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

    def test_empty_xlsx(self):
        """XLSX μόνο με header → άδεια data, χωρίς crash."""
        path = self._track(_write_xlsx([]))
        data, skipped = read_excel(path)
        self.assertEqual(data, [])

    def test_valid_single_row(self):
        """Έγκυρη μία γραμμή → καταχωρείται."""
        rows = [
            ["123456789", "Μαρία", "Κορρέ", "ΟΠΩΡΟΦΟΡΑ", "Πορτοκαλιά",
             2.5, "Συμβατικά", 5, 0, ""]
        ]
        path = self._track(_write_xlsx(rows))
        data, skipped = read_excel(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["afm"], "123456789")

    def test_invalid_afm_skipped(self):
        """Invalid ΑΦΜ → skipped."""
        rows = [
            ["123", "Maria", "Korre", "X", "Y", "", "Συμβατικά", "", "", ""],
            ["12345678901234", "Other", "Person", "X", "Y", "", "Συμβατικά", "", "", ""],
            ["123456789", "Valid", "One", "X", "Y", 1, "Συμβατικά", "", "", ""],
        ]
        path = self._track(_write_xlsx(rows))
        data, skipped = read_excel(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["afm"], "123456789")
        self.assertEqual(len(skipped), 2)

    def test_missing_sheet_name(self):
        """XLSX χωρίς το sheet 'TA Αρχικής' → exception."""
        path = self._track(_write_xlsx([], sheet_name="WrongName"))
        with self.assertRaises(Exception) as ctx:
            read_excel(path)
        self.assertIn("TA Αρχικής", str(ctx.exception))

    def test_corrupted_xlsx(self):
        """Binary garbage με .xlsx extension → exception (magic bytes check)."""
        path = self._track(_write_bytes(
            b"NOT A VALID XLSX FILE \x00\x01\x02\xff",
            suffix=".xlsx"
        ))
        with self.assertRaises(Exception):
            read_excel(path)

    def test_unicode_in_fields(self):
        """Greek + emoji → preserved σωστά."""
        rows = [
            ["123456789", "Νίκος😀", "Παπαδόπουλος🎉", "Cat", "Desc",
             1, "Συμβατικά", "", "", ""]
        ]
        path = self._track(_write_xlsx(rows))
        data, skipped = read_excel(path)
        self.assertEqual(data[0]["name"], "Νίκος😀")
        self.assertEqual(data[0]["surname"], "Παπαδόπουλος🎉")

    def test_sql_injection_in_xlsx(self):
        """SQL injection strings σε XLSX → απλό text."""
        injection = "Robert'); DROP TABLE Students;--"
        rows = [
            ["123456789", injection, "Tables", "Cat", "Desc",
             1, "Συμβατικά", "", "", ""]
        ]
        path = self._track(_write_xlsx(rows))
        data, skipped = read_excel(path)
        self.assertEqual(data[0]["name"], injection)

    def test_many_rows_performance_xlsx(self):
        """5k γραμμές XLSX → επεξεργάζονται κανονικά."""
        rows = [
            [str(100000000 + i).zfill(9), "N{}".format(i), "S{}".format(i),
             "Cat", "Desc", 1, "Συμβατικά", "", "", ""]
            for i in range(5000)
        ]
        path = self._track(_write_xlsx(rows))
        data, skipped = read_excel(path)
        self.assertEqual(len(data), 5000)

    def test_calculated_fields_always_empty(self):
        """Τα calculated fields πρέπει να είναι ΠΑΝΤΑ '' (security: never trust input)."""
        rows = [
            ["123456789", "Maria", "Korre", "Cat", "Desc",
             1, "Συμβατικά", "", "", ""]
        ]
        path = self._track(_write_xlsx(rows))
        data, skipped = read_excel(path)
        entry = data[0]["rows"][0]
        for calc_field in ("typical_output", "output_per_choice", "total_output",
                           "ta_productive", "ta_plant", "ta_animal", "ta_bees"):
            self.assertEqual(
                entry[calc_field], "",
                "{} πρέπει να είναι κενό (recalculated by code)".format(calc_field)
            )

    def test_region_always_default(self):
        """Region πρέπει πάντα να είναι '--Επιλέξτε' (όχι imported)."""
        rows = [
            ["123456789", "Maria", "Korre", "Cat", "Desc",
             1, "Συμβατικά", "", "", ""]
        ]
        path = self._track(_write_xlsx(rows))
        data, skipped = read_excel(path)
        self.assertEqual(data[0]["region"], "--Επιλέξτε")

    def test_xlsx_with_only_invalid_afms(self):
        """XLSX με μόνο invalid AFMs → άδειο data, όλοι skipped."""
        rows = [
            ["abc", "X", "Y", "", "", "", "Συμβατικά", "", "", ""],
            ["", "X", "Y", "", "", "", "Συμβατικά", "", "", ""],
            ["12345", "X", "Y", "", "", "", "Συμβατικά", "", "", ""],
        ]
        path = self._track(_write_xlsx(rows))
        data, skipped = read_excel(path)
        self.assertEqual(data, [])
        self.assertEqual(len(skipped), 3)

    def test_missing_required_column_raises(self):
        """XLSX χωρίς όλες τις υποχρεωτικές στήλες → ValueError."""
        # Δημιουργούμε XLSX με header λείπει η στήλη "Αμπέλι >3 ετών"
        fd, path = tempfile.mkstemp(suffix=".xlsx")
        os.close(fd)
        self._track(path)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "TA Αρχικής"
        ws.append([
            "ΑΦΜ", "Όνομα", "Επώνυμο", "Κατηγορία ΟΣΔΕ", "Περιγραφή",
            "Έκταση/Αριθμός ζώων", "Βιολογικά", "Δένδρα >=4 ετών", "Δένδρα <4 ετών",
            # απουσιάζει "Αμπέλι >3 ετών"
        ])
        wb.save(path)
        wb.close()

        with self.assertRaises(Exception):
            read_excel(path)


# ─────────────────────────────────────────────────────────────
# _validate_import_row — strict validation rules
# ─────────────────────────────────────────────────────────────

class TestValidateImportRow(unittest.TestCase):
    """Tests για το strict validation της κάθε εισαγόμενης γραμμής."""

    def setUp(self):
        # Real validation με caches από ta.xlsx
        self.mock = _make_mock_main_window(with_validation=True)
        self.validate = self.mock._validate_import_row

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

    # — Quantity range/precision —

    def test_quantity_negative_raises(self):
        with self.assertRaises(ValueError):
            self.validate(self._row(quantity='-1'), 'csv')

    def test_quantity_over_max_raises(self):
        with self.assertRaises(ValueError):
            self.validate(self._row(quantity='99999999'), 'csv')

    def test_quantity_three_decimals_raises(self):
        with self.assertRaises(ValueError):
            self.validate(self._row(quantity='1.234'), 'csv')

    def test_quantity_two_decimals_ok(self):
        # δεν σηκώνει
        self.validate(self._row(quantity='12.34'), 'csv')

    def test_quantity_comma_decimal_ok(self):
        self.validate(self._row(quantity='12,34'), 'csv')

    def test_quantity_non_numeric_raises(self):
        with self.assertRaises(ValueError):
            self.validate(self._row(quantity='abc'), 'csv')

    def test_quantity_empty_ok(self):
        self.validate(self._row(quantity=''), 'csv')

    # — Trees: integer-only —

    def test_trees_decimal_raises(self):
        with self.assertRaises(ValueError):
            self.validate(self._row(trees_over_4='12.5'), 'csv')

    def test_trees_integer_ok(self):
        self.validate(self._row(trees_over_4='12', trees_under_4='3'), 'csv')

    def test_trees_excel_float_int_ok(self):
        """Excel μπορεί να περάσει 12.0 — γίνεται δεκτό."""
        self.validate(self._row(trees_over_4='12.0'), 'excel')

    def test_trees_negative_raises(self):
        with self.assertRaises(ValueError):
            self.validate(self._row(trees_over_4='-5'), 'csv')

    def test_trees_over_max_raises(self):
        with self.assertRaises(ValueError):
            self.validate(self._row(trees_over_4='99999999'), 'csv')

    # — Excel certification (whitelist) —

    def test_excel_cert_empty_raises(self):
        with self.assertRaises(ValueError):
            self.validate(self._row(certification=''), 'excel')

    def test_excel_cert_invalid_raises(self):
        with self.assertRaises(ValueError):
            self.validate(self._row(certification='ΑΛΛΟ'), 'excel')

    def test_excel_cert_valid_ok(self):
        for c in ("--Επιλέξτε", "Συμβατικά", "Βιολογικά", "Ολοκληρωμένη", "ΠΟΠ/ΠΓΕ"):
            self.validate(self._row(certification=c), 'excel')

    def test_csv_cert_not_validated(self):
        """Στο CSV, η certification δεν είναι required (default '')."""
        # Δεν σηκώνει — ο κανόνας ισχύει μόνο για excel
        self.validate(self._row(certification=''), 'csv')

    # — Vine values —

    def test_csv_vine_invalid_raw_raises(self):
        """CSV: raw_vine_csv εκτός {'1','0'} → ValueError όταν cat ∈ AMPELI."""
        from utils.excel_loader import LOCK_AMPELI
        cat = next(iter(LOCK_AMPELI))
        with self.assertRaises(ValueError):
            self.validate(self._row(category_osde=cat), 'csv', raw_vine_csv='maybe')

    def test_csv_vine_valid_raw_ok(self):
        from utils.excel_loader import LOCK_AMPELI
        cat = next(iter(LOCK_AMPELI))
        self.validate(self._row(category_osde=cat), 'csv', raw_vine_csv='1')
        self.validate(self._row(category_osde=cat), 'csv', raw_vine_csv='0')

    def test_excel_vine_invalid_raises(self):
        from utils.excel_loader import LOCK_AMPELI
        cat = next(iter(LOCK_AMPELI))
        with self.assertRaises(ValueError):
            self.validate(self._row(category_osde=cat, vine_over_3='maybe'), 'excel')

    def test_excel_vine_valid_ok(self):
        from utils.excel_loader import LOCK_AMPELI
        cat = next(iter(LOCK_AMPELI))
        for v in ("--Επιλέξτε", "Ναι", "Όχι"):
            self.validate(self._row(category_osde=cat, vine_over_3=v), 'excel')

    # — Text length on unknown category/description —

    def test_unknown_category_under_max_len_ok(self):
        """Άγνωστη κατηγορία αλλά ≤200 χαρ → ΔΕΝ σηκώνει (μόνο warn flow αλλού)."""
        self.validate(self._row(category_osde='ΆΓΝΩΣΤΗ ΚΑΤΗΓΟΡΙΑ ΧΧΧ' * 5), 'csv')

    def test_unknown_category_over_max_len_raises(self):
        self.validate  # silence linter
        with self.assertRaises(ValueError):
            self.validate(self._row(category_osde='X' * 201), 'csv')

    def test_unknown_description_over_max_len_raises(self):
        with self.assertRaises(ValueError):
            self.validate(self._row(description='Y' * 201), 'csv')


# ─────────────────────────────────────────────────────────────
# _canonicalize_entry_row — reverse lookup σε ta.xlsx
# ─────────────────────────────────────────────────────────────

class TestCanonicalizeEntryRow(unittest.TestCase):
    """Tests για το canonical mapping cat/desc μέσω norm() reverse lookup."""

    @classmethod
    def setUpClass(cls):
        from utils.excel_loader import load_excel_data, resource_path
        mapping, value_mapping = load_excel_data(resource_path("data/ta.xlsx"))
        cls.mapping = mapping
        cls.value_mapping = value_mapping
        # Πάρε ένα γνωστό ζευγάρι (cat, desc) από το ta.xlsx για χρήση στα tests
        cls.sample_cat, cls.sample_desc = next(iter(value_mapping.keys()))

    def setUp(self):
        self.mock = _make_mock_main_window(with_canonicalize=True)
        self.canon = self.mock._canonicalize_entry_row

    def test_empty_cat_no_op(self):
        """Κενή Κατηγορία → δεν αλλάζει τίποτα."""
        row = {'category_osde': '', 'description': 'whatever'}
        self.canon(row)
        self.assertEqual(row['category_osde'], '')
        self.assertEqual(row['description'], 'whatever')

    def test_canonical_pair_unchanged(self):
        """(cat, desc) ήδη κανονικό → παραμένει."""
        row = {'category_osde': self.sample_cat, 'description': self.sample_desc}
        self.canon(row)
        self.assertEqual(row['category_osde'], self.sample_cat)
        self.assertEqual(row['description'], self.sample_desc)

    def test_lowercase_pair_canonicalized(self):
        """Lowercase εκδοχή ζευγαριού → γίνεται κανονική."""
        row = {
            'category_osde': self.sample_cat.lower(),
            'description': self.sample_desc.lower(),
        }
        self.canon(row)
        self.assertEqual(row['category_osde'], self.sample_cat)
        self.assertEqual(row['description'], self.sample_desc)

    def test_accentless_pair_canonicalized(self):
        """Χωρίς τόνους → norm() ταιριάζει → canonical replacement."""
        import unicodedata
        def strip_accents(s):
            return ''.join(
                c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn'
            )
        row = {
            'category_osde': strip_accents(self.sample_cat),
            'description': strip_accents(self.sample_desc),
        }
        self.canon(row)
        self.assertEqual(row['category_osde'], self.sample_cat)
        self.assertEqual(row['description'], self.sample_desc)

    def test_whitespace_padding_canonicalized(self):
        """Extra whitespace → norm() ταιριάζει → canonical."""
        row = {
            'category_osde': '  ' + self.sample_cat + '   ',
            'description': self.sample_desc,
        }
        self.canon(row)
        self.assertEqual(row['category_osde'], self.sample_cat)

    def test_unknown_pair_unchanged(self):
        """Άγνωστο ζευγάρι → καμία αλλαγή."""
        row = {'category_osde': 'XXX_UNKNOWN', 'description': 'YYY_UNKNOWN'}
        self.canon(row)
        self.assertEqual(row['category_osde'], 'XXX_UNKNOWN')
        self.assertEqual(row['description'], 'YYY_UNKNOWN')

    def test_known_cat_unknown_desc_canonicalizes_cat_only(self):
        """Γνωστή cat + άγνωστο desc → μόνο η cat γίνεται canonical."""
        row = {
            'category_osde': self.sample_cat.lower(),
            'description': 'UNKNOWN_VARIETY',
        }
        self.canon(row)
        self.assertEqual(row['category_osde'], self.sample_cat)
        self.assertEqual(row['description'], 'UNKNOWN_VARIETY')  # αμετάβλητο

    def test_empty_desc_canonicalizes_cat(self):
        """Κενή desc + γνωστή cat → canonical cat (μέσω cat-only lookup)."""
        row = {'category_osde': self.sample_cat.lower(), 'description': ''}
        self.canon(row)
        self.assertEqual(row['category_osde'], self.sample_cat)


# ─────────────────────────────────────────────────────────────
# Canonicalization integrated στο import flow (CSV + Excel)
# ─────────────────────────────────────────────────────────────

class TestCanonicalizationInImport(unittest.TestCase):
    """Επιβεβαιώνει ότι το import καλεί το _canonicalize_entry_row."""

    @classmethod
    def setUpClass(cls):
        from utils.excel_loader import load_excel_data, resource_path
        _, value_mapping = load_excel_data(resource_path("data/ta.xlsx"))
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

    def _read_csv_with_canon(self, path):
        return MainWindow._read_csv_file(
            _make_mock_main_window(with_canonicalize=True), path
        )

    def _read_excel_with_canon(self, path):
        return MainWindow._read_excel_file(
            _make_mock_main_window(with_canonicalize=True), path
        )

    def test_csv_lowercase_cat_desc_canonicalized(self):
        """CSV με lowercase cat/desc → το import τα φέρνει σε κανονική γραφή."""
        content = CSV_HEADER_FULL + "\n" + _csv_row(
            afm="123456789",
            cat=self.sample_cat.lower(),
            desc=self.sample_desc.lower(),
            qty="1",
        ) + "\n"
        path = self._track(_write_text(content))
        data, _ = self._read_csv_with_canon(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["rows"][0]["category_osde"], self.sample_cat)
        self.assertEqual(data[0]["rows"][0]["description"], self.sample_desc)

    def test_excel_lowercase_cat_desc_canonicalized(self):
        """Excel με lowercase cat/desc → canonical γραφή μετά το import."""
        rows = [[
            "123456789", "Maria", "Korre",
            self.sample_cat.lower(), self.sample_desc.lower(),
            1, "Συμβατικά", "", "", "",
        ]]
        path = self._track(_write_xlsx(rows))
        data, _ = self._read_excel_with_canon(path)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["rows"][0]["category_osde"], self.sample_cat)
        self.assertEqual(data[0]["rows"][0]["description"], self.sample_desc)


# ─────────────────────────────────────────────────────────────
# Property: ΑΦΜ validation contract
# ─────────────────────────────────────────────────────────────

class TestAfmValidationContract(unittest.TestCase):
    """Επιβεβαιώνει ότι ΜΟΝΟ 9-ψήφιοι ΑΦΜ περνούν."""

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

    def test_afm_lengths_csv(self):
        for length in [0, 1, 5, 8, 10, 15, 20]:
            with self.subTest(length=length):
                afm = "1" * length
                content = CSV_HEADER_FULL + "\n" + _csv_row(afm=afm) + "\n"
                path = self._track(_write_text(content))
                data, skipped = read_csv(path)
                self.assertEqual(data, [], "length={} should be skipped".format(length))

    def test_afm_exactly_9_csv(self):
        afm = "9" * 9
        content = CSV_HEADER_FULL + "\n" + _csv_row(afm=afm) + "\n"
        path = self._track(_write_text(content))
        data, skipped = read_csv(path)
        self.assertEqual(len(data), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
