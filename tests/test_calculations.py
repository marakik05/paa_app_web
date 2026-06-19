"""
Unit tests for utils/ta_calculations.py — οι πραγματικές pure-Python
συναρτήσεις υπολογισμού ΤΑ που χρησιμοποιεί το server.py (calc_row, calc_totals).
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.ta_calculations import (
    typiki_apodosi, ta_paragwgikwn, route_fzm, paragwgikwn,
    lookup_typical_output, calc_row, calc_totals, to_float, to_int,
)


# ─── Tests: typiki_apodosi ───────────────────────────────────────────

class TestTypikiApodosi(unittest.TestCase):
    """Κλάση για το τεστάρισμα της def υπολογισμού τυπικής απόδοσης (στήλη 8)."""

    def test_no_trees_no_vine(self):
        """Simple: TA * area."""
        result = typiki_apodosi("ΣΚΛΗΡΟΣ ΣΙΤΟΣ", 100.0, 5.0, None, None, "")
        self.assertEqual(result, 500.0)

    def test_no_trees_zeros(self):
        """Trees both 0 → TA * area."""
        result = typiki_apodosi("ΕΣΠΕΡΙΔΟΕΙΔΗ", 100.0, 5.0, 0, 0, "")
        self.assertEqual(result, 500.0)

    def test_only_productive_trees(self):
        """Only col_5 (>=4yr) → TA * area."""
        result = typiki_apodosi("ΕΛΑΙΩΝΕΣ", 200.0, 3.0, 50, 0, "")
        self.assertEqual(result, 600.0)

    def test_only_young_trees(self):
        """Only col_6 (<4yr) → (TA/2) * area."""
        result = typiki_apodosi("ΕΛΑΙΩΝΕΣ", 200.0, 3.0, 0, 50, "")
        self.assertEqual(result, 300.0)

    def test_mixed_trees(self):
        """Both productive and young → weighted average."""
        # 200 * (3 * 60/100) + 100 * (3 * 40/100) = 360 + 120 = 480
        result = typiki_apodosi("ΕΛΑΙΩΝΕΣ", 200.0, 3.0, 60, 40, "")
        self.assertAlmostEqual(result, 480.0, places=2)

    def test_vine_yes(self):
        """Ampeli with Ναι → TA * area."""
        result = typiki_apodosi("ΑΜΠΕΛΩΝΕΣ ΓΙΑ ΠΑΡΑΓΩΓΗ ΟΙΝΟΥ", 150.0, 2.0, None, None, "Ναι")
        self.assertEqual(result, 300.0)

    def test_vine_no(self):
        """Ampeli with Όχι → (TA/2) * area."""
        result = typiki_apodosi("ΑΜΠΕΛΩΝΕΣ ΓΙΑ ΠΑΡΑΓΩΓΗ ΟΙΝΟΥ", 150.0, 2.0, None, None, "Όχι")
        self.assertEqual(result, 150.0)

    def test_vine_empty(self):
        """Ampeli with no selection → None."""
        result = typiki_apodosi("ΑΜΠΕΛΩΝΕΣ ΓΙΑ ΠΑΡΑΓΩΓΗ ΟΙΝΟΥ", 150.0, 2.0, None, None, "")
        self.assertIsNone(result)

    def test_vine_default(self):
        """Ampeli with --Επιλέξτε → None."""
        result = typiki_apodosi("ΑΜΠΕΛΩΝΕΣ ΓΙΑ ΠΑΡΑΓΩΓΗ ΟΙΝΟΥ", 150.0, 2.0, None, None, "--Επιλέξτε")
        self.assertIsNone(result)

    def test_missing_ta(self):
        result = typiki_apodosi("ΣΚΛΗΡΟΣ ΣΙΤΟΣ", None, 5.0, None, None, "")
        self.assertIsNone(result)

    def test_missing_area(self):
        result = typiki_apodosi("ΣΚΛΗΡΟΣ ΣΙΤΟΣ", 100.0, None, None, None, "")
        self.assertIsNone(result)

    def test_equal_trees(self):
        """50/50 split → TA*area*(0.5) + (TA/2)*area*(0.5)."""
        # 100 * (10 * 0.5) + 50 * (10 * 0.5) = 500 + 250 = 750
        result = typiki_apodosi("ΕΛΑΙΩΝΕΣ", 100.0, 10.0, 50, 50, "")
        self.assertAlmostEqual(result, 750.0, places=2)


# ─── Tests: ta_paragwgikwn ───────────────────────────────────────────

class TestTaParagwgikwn(unittest.TestCase):
    """Κλάση για το τεστάρισμα της def υπολογισμού ΤΑ παραγωγικών δένδρων."""

    def test_no_trees(self):
        """No trees → TA * area (all productive)."""
        result = ta_paragwgikwn("ΣΚΛΗΡΟΣ ΣΙΤΟΣ", 100.0, 5.0, None, None, "")
        self.assertEqual(result, 500.0)

    def test_only_young(self):
        """Only young trees → None (no productive)."""
        result = ta_paragwgikwn("ΕΛΑΙΩΝΕΣ", 200.0, 3.0, 0, 50, "")
        self.assertIsNone(result)

    def test_only_productive(self):
        """Only productive trees → TA * area."""
        result = ta_paragwgikwn("ΕΛΑΙΩΝΕΣ", 200.0, 3.0, 50, 0, "")
        self.assertEqual(result, 600.0)

    def test_mixed(self):
        """Mixed → only productive portion."""
        # 200 * (3 * 60/100) = 360
        result = ta_paragwgikwn("ΕΛΑΙΩΝΕΣ", 200.0, 3.0, 60, 40, "")
        self.assertAlmostEqual(result, 360.0, places=2)

    def test_vine_yes(self):
        """Ampeli Ναι → full TA * area (productive)."""
        result = ta_paragwgikwn("ΑΜΠΕΛΩΝΕΣ ΓΙΑ ΠΑΡΑΓΩΓΗ ΟΙΝΟΥ", 150.0, 2.0, None, None, "Ναι")
        self.assertEqual(result, 300.0)

    def test_vine_no(self):
        """Ampeli Όχι → None (not productive)."""
        result = ta_paragwgikwn("ΑΜΠΕΛΩΝΕΣ ΓΙΑ ΠΑΡΑΓΩΓΗ ΟΙΝΟΥ", 150.0, 2.0, None, None, "Όχι")
        self.assertIsNone(result)

    def test_vine_empty(self):
        """Ampeli with no selection → None."""
        result = ta_paragwgikwn("ΑΜΠΕΛΩΝΕΣ ΓΙΑ ΠΑΡΑΓΩΓΗ ΟΙΝΟΥ", 150.0, 2.0, None, None, "")
        self.assertIsNone(result)


# ─── Tests: route_fzm ────────────────────────────────────────────────

class TestRouteFzm(unittest.TestCase):
    """Κλάση για το routing ΤΑ φυτικής/ζωικής/μελισσιών (στήλες 12/13/14)."""

    def test_zwiki(self):
        self.assertEqual(route_fzm("ΑΙΓΟΠΡΟΒΑΤΑ"), 13)
        self.assertEqual(route_fzm("ΒΟΟΕΙΔΗ"), 13)
        self.assertEqual(route_fzm("ΧΟΙΡΟΙ"), 13)

    def test_melisses(self):
        self.assertEqual(route_fzm("ΚΥΨΕΛΕΣ ΜΕΛΙΣΣΩΝ - ΜΕΛΛΙΣΟΣΜΗΝΗ"), 14)
        self.assertEqual(route_fzm("ΜΕΤΑΞΟΣΚΩΛΗΚΕΣ"), 14)

    def test_fytiki(self):
        self.assertEqual(route_fzm("ΣΚΛΗΡΟΣ ΣΙΤΟΣ"), 12)
        self.assertEqual(route_fzm("ΕΛΑΙΩΝΕΣ"), 12)
        self.assertEqual(route_fzm("ΓΕΩΜΗΛΑ"), 12)


# ─── Tests: paragwgikwn (στήλη 11 — ΤΑ Παραγωγικών) ──────────────────

class TestParagwgikwn(unittest.TestCase):

    def test_paragwgika_cat_and_keyword_uses_output_per_choice(self):
        """ΑΙΓΟΠΡΟΒΑΤΑ + περιγραφή με 'ΑΙΓΕΣ' → επιστρέφει το output_per_choice."""
        result = paragwgikwn("ΑΙΓΟΠΡΟΒΑΤΑ", "ΑΙΓΕΣ ΓΑΛΑΚΤΟΠΑΡΑΓΩΓΗΣ", 500.0, 0.0)
        self.assertEqual(result, 500.0)

    def test_non_paragwgika_cat_uses_productive_value(self):
        """Κατηγορία εκτός PARAGWGIKA_CAT → επιστρέφει το productive_value (π.χ. ta_paragwgikwn)."""
        result = paragwgikwn("ΕΛΑΙΩΝΕΣ", "Οποιαδήποτε", 500.0, 300.0)
        self.assertEqual(result, 300.0)

    def test_paragwgika_cat_without_keyword_uses_productive_value(self):
        """ΑΙΓΟΠΡΟΒΑΤΑ αλλά περιγραφή χωρίς keyword (π.χ. 'ΤΡΑΓΟΙ') → productive_value."""
        result = paragwgikwn("ΑΙΓΟΠΡΟΒΑΤΑ", "ΤΡΑΓΟΙ", 500.0, 300.0)
        self.assertEqual(result, 300.0)


# ─── Tests: lookup_typical_output (στήλη 2) ──────────────────────────

class TestLookupTypicalOutput(unittest.TestCase):

    def setUp(self):
        self.value_mapping = {
            ("CAT", "DESC"): {"default": 100.0, "aegean": 150.0},
        }

    def test_no_region_selected(self):
        self.assertIsNone(lookup_typical_output(self.value_mapping, "CAT", "DESC", ""))
        self.assertIsNone(lookup_typical_output(self.value_mapping, "CAT", "DESC", "--Επιλέξτε"))

    def test_unknown_pair_returns_none(self):
        self.assertIsNone(lookup_typical_output(self.value_mapping, "X", "Y", "Αττική"))

    def test_default_region_uses_default_column(self):
        result = lookup_typical_output(self.value_mapping, "CAT", "DESC", "Αττική")
        self.assertEqual(result, 100.0)

    def test_aegean_region_uses_aegean_column(self):
        result = lookup_typical_output(self.value_mapping, "CAT", "DESC", "Κρήτη")
        self.assertEqual(result, 150.0)
        result = lookup_typical_output(self.value_mapping, "CAT", "DESC", "Νότιο Αιγαίο")
        self.assertEqual(result, 150.0)


# ─── Tests: calc_row / calc_totals (server.py /api/ta/recalculate) ───

class TestCalcRow(unittest.TestCase):

    def setUp(self):
        self.value_mapping = {
            ("ΕΛΑΙΩΝΕΣ", "Desc"): {"default": 100.0, "aegean": 120.0},
            ("ΑΙΓΟΠΡΟΒΑΤΑ", "ΑΙΓΕΣ"): {"default": 200.0, "aegean": 220.0},
        }

    def test_calc_row_basic(self):
        """ΕΛΑΙΩΝΕΣ (tree crop) δεν είναι σε LOCK_TREES → οι στήλες δένδρων είναι ενεργές."""
        result = calc_row(self.value_mapping, "Αττική", "ΕΛΑΙΩΝΕΣ", "Desc", 5.0, None, None, "")
        self.assertEqual(result["typical_output"], 100.0)
        self.assertEqual(result["output_per_choice"], 500.0)
        self.assertEqual(result["route"], 12)
        self.assertFalse(result["lock_ampeli"])
        self.assertFalse(result["lock_trees"])

    def test_calc_row_locks_for_ampeli(self):
        result = calc_row(self.value_mapping, "Αττική", "ΑΜΠΕΛΩΝΕΣ ΓΙΑ ΠΑΡΑΓΩΓΗ ΟΙΝΟΥ", "Desc", 2.0, None, None, "Ναι")
        self.assertTrue(result["lock_ampeli"])

    def test_calc_row_locks_trees_for_animals(self):
        result = calc_row(self.value_mapping, "Αττική", "ΑΙΓΟΠΡΟΒΑΤΑ", "ΑΙΓΕΣ", 10.0, None, None, "")
        self.assertTrue(result["lock_trees"])
        self.assertEqual(result["route"], 13)
        # ΑΙΓΟΠΡΟΒΑΤΑ + ΑΙΓΕΣ → productive = output_per_choice
        self.assertEqual(result["productive"], result["output_per_choice"])


class TestCalcTotals(unittest.TestCase):

    def test_totals_sum_by_route(self):
        rows_calc = [
            {"output_per_choice": 100.0, "productive": 100.0, "route": 12},
            {"output_per_choice": 200.0, "productive": None, "route": 13},
            {"output_per_choice": 50.0, "productive": 50.0, "route": 14},
        ]
        totals = calc_totals(rows_calc)
        self.assertEqual(totals["total_output"], 350.0)
        self.assertEqual(totals["ta_productive"], 150.0)
        self.assertEqual(totals["ta_plant"], 100.0)
        self.assertEqual(totals["ta_animal"], 200.0)
        self.assertEqual(totals["ta_bees"], 50.0)

    def test_totals_empty_rows_returns_none(self):
        totals = calc_totals([])
        self.assertIsNone(totals["total_output"])
        self.assertIsNone(totals["ta_productive"])
        self.assertIsNone(totals["ta_plant"])
        self.assertIsNone(totals["ta_animal"])
        self.assertIsNone(totals["ta_bees"])

    def test_totals_ignores_none_values(self):
        rows_calc = [
            {"output_per_choice": None, "productive": None, "route": 12},
            {"output_per_choice": 100.0, "productive": 100.0, "route": 12},
        ]
        totals = calc_totals(rows_calc)
        self.assertEqual(totals["total_output"], 100.0)


# ─── Tests: to_float / to_int (input parsing helpers) ────────────────

class TestToFloat(unittest.TestCase):

    def test_empty_and_none(self):
        self.assertIsNone(to_float(""))
        self.assertIsNone(to_float(None))

    def test_comma_decimal(self):
        self.assertEqual(to_float("1,5"), 1.5)

    def test_dot_decimal(self):
        self.assertEqual(to_float("3.5"), 3.5)

    def test_invalid_returns_none(self):
        self.assertIsNone(to_float("abc"))


class TestToInt(unittest.TestCase):

    def test_empty_and_none(self):
        self.assertIsNone(to_int(""))
        self.assertIsNone(to_int(None))

    def test_valid_int_string(self):
        self.assertEqual(to_int("3"), 3)

    def test_decimal_string_returns_none(self):
        """to_int δεν κάνει round — δεκαδικό string αποτυγχάνει στο int()."""
        self.assertIsNone(to_int("1,5"))

    def test_invalid_returns_none(self):
        self.assertIsNone(to_int("abc"))


if __name__ == '__main__':
    unittest.main()
