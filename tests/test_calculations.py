"""
Unit tests for base_table TA calculation formulas.
Tests: typiki_apodosi, ta_paragwgikwn, total_fzm routing, biologic %, eligibility Q7.
Formulas extracted as pure functions — no Qt dependency.
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.excel_loader import (
    norm, in_norm_set,
    LOCK_AMPELI_NORM, FMZ_ZWIKI_NORM, FMZ_MELISSES_NORM, ISLANDS
)


# ─── Extracted TA formulas ───────────────────────────────────────────

def typiki_apodosi(col_0, col_2, col_3, col_5, col_6, col_7):
    """
    Υπολογισμός ΤΑ ανά αγροτεμάχιο (στήλη 8).
    col_0: category, col_2: TA, col_3: area,
    col_5: trees>=4, col_6: trees<4, col_7: vine>3yr
    """
    if col_2 is None or col_3 is None:
        return None

    if in_norm_set(col_0, LOCK_AMPELI_NORM):
        if col_7 == "Ναι":
            return col_2 * col_3
        elif col_7 == "Όχι":
            return (col_2 / 2) * col_3
        else:  # empty or "--Επιλέξτε"
            return None
    else:
        if (col_5 is None or col_5 == 0) and (col_6 is None or col_6 == 0):
            return col_2 * col_3
        if col_5 is None or col_5 == 0:
            return (col_2 / 2) * col_3
        if col_6 is None or col_6 == 0:
            return col_2 * col_3
        total = col_5 + col_6
        return col_2 * (col_3 * (col_5 / total)) + (col_2 / 2) * (col_3 * (col_6 / total))


def ta_paragwgikwn(col_0, col_2, col_3, col_5, col_6, col_7):
    """
    Υπολογισμός ΤΑ παραγωγικών (μόνο παραγωγικά δένδρα).
    """
    if col_2 is None or col_3 is None:
        return None

    if in_norm_set(col_0, LOCK_AMPELI_NORM):
        if col_7 == "Ναι":
            return col_2 * col_3
        else:
            return None
    else:
        if (col_5 is None or col_5 == 0) and (col_6 is None or col_6 == 0):
            return col_2 * col_3
        if col_5 is None or col_5 == 0:
            return None
        if col_6 is None or col_6 == 0:
            return col_2 * col_3
        total = col_5 + col_6
        return col_2 * (col_3 * (col_5 / total))


def route_fzm(category):
    """
    Determines which TA column a category goes to.
    Returns 12 (φυτική), 13 (ζωική), or 14 (μελίσσια).
    """
    if in_norm_set(category, FMZ_ZWIKI_NORM):
        return 13
    elif in_norm_set(category, FMZ_MELISSES_NORM):
        return 14
    return 12


def eligibility_q7(region, ta):
    """
    Επιλεξιμότητα κριτηρίου Q7.
    ISLANDS (threshold 8000), others (threshold 12000).
    """
    if ta is None:
        return None
    if region in ISLANDS and ta >= 8000:
        return "ΕΠΙΛΕΞΙΜΟΣ"
    elif region not in ISLANDS and ta >= 12000:
        return "ΕΠΙΛΕΞΙΜΟΣ"
    return "ΜΗ ΕΠΙΛΕΞΙΜΟΣ"


def biologic_pct(rows_col4_col8, total_ta):
    """
    Υπολογισμός ποσοστού βιολογικών/συστημάτων ποιότητας.
    rows: list of (col4_text, col8_value)
    total_ta: float (col 10 value)
    Mirrors `baseTable.biologic`: μόνο τιμές στο INCLUDED set μετράνε.
    """
    INCLUDED = {"Βιολογικά", "Ολοκληρωμένη", "ΠΟΠ/ΠΓΕ"}
    if total_ta is None or total_ta == 0:
        return None

    total_bio = 0.0
    has_value = False
    for choice, value in rows_col4_col8:
        if choice not in INCLUDED:
            continue
        if value is not None:
            total_bio += value
            has_value = True

    if not has_value:
        return 0.0

    return (total_bio / total_ta) * 100


# ─── Tests: typiki_apodosi ───────────────────────────────────────────

class TestTypikiApodosi(unittest.TestCase):
    """""Κλάση για το τεστάρισμα της def υπολογισμού τυπικής απόδοσης"""

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
    """""Κλάση για το τεστάρισμα της def υπολογισμού τυπικής απόδοσης παραγωγικών"""
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
        result = typiki_apodosi("ΑΜΠΕΛΩΝΕΣ ΓΙΑ ΠΑΡΑΓΩΓΗ ΟΙΝΟΥ", 150.0, 2.0, None, None, "")
        self.assertIsNone(result)


# ─── Tests: route_fzm ────────────────────────────────────────────────

class TestRouteFzm(unittest.TestCase):
    """""Κλάση για το αν αθροίζονται σωστά οι ΤΑ φυτικής, ζωικής και μελισσιών/μεταξοσκώληκων"""

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


# ─── Tests: eligibility Q7 ──────────────────────────────────────────

class TestEligibilityQ7(unittest.TestCase):

    def test_island_above_8000(self):
        self.assertEqual(eligibility_q7("Νότιο Αιγαίο", 8000), "ΕΠΙΛΕΞΙΜΟΣ")
        self.assertEqual(eligibility_q7("Βόρειο Αιγαίο", 10000), "ΕΠΙΛΕΞΙΜΟΣ")
        self.assertEqual(eligibility_q7("Ιόνια Νησιά", 9000), "ΕΠΙΛΕΞΙΜΟΣ")

    def test_island_below_8000(self):
        self.assertEqual(eligibility_q7("Νότιο Αιγαίο", 7999.99), "ΜΗ ΕΠΙΛΕΞΙΜΟΣ")
        self.assertEqual(eligibility_q7("Βόρειο Αιγαίο", 4000), "ΜΗ ΕΠΙΛΕΞΙΜΟΣ")

    def test_mainland_above_12000(self):
        self.assertEqual(eligibility_q7("Αττική", 12000), "ΕΠΙΛΕΞΙΜΟΣ")
        self.assertEqual(eligibility_q7("Κρήτη", 15000), "ΕΠΙΛΕΞΙΜΟΣ")

    def test_mainland_below_12000(self):
        self.assertEqual(eligibility_q7("Αττική", 11999.99), "ΜΗ ΕΠΙΛΕΞΙΜΟΣ")
        self.assertEqual(eligibility_q7("Θεσσαλία", 5000), "ΜΗ ΕΠΙΛΕΞΙΜΟΣ")

    def test_none_ta(self):
        self.assertIsNone(eligibility_q7("Αττική", None))
        
    def test_none_all(self):
        self.assertIsNone(eligibility_q7(None, None))

    def test_zero_ta(self):
        self.assertEqual(eligibility_q7("Αττική", 0), "ΜΗ ΕΠΙΛΕΞΙΜΟΣ")

    def test_island_boundary(self):
        """Exactly at 8000 on island → ΕΠΙΛΕΞΙΜΟΣ."""
        self.assertEqual(eligibility_q7("Ιόνια Νησιά", 8000), "ΕΠΙΛΕΞΙΜΟΣ")

    def test_mainland_boundary(self):
        """Exactly at 12000 on mainland → ΕΠΙΛΕΞΙΜΟΣ."""
        self.assertEqual(eligibility_q7("Θεσσαλία", 12000), "ΕΠΙΛΕΞΙΜΟΣ")


# ─── Tests: biologic percentage ──────────────────────────────────────

class TestBiologicPct(unittest.TestCase):

    def test_all_biologic(self):
        rows = [("Βιολογικά", 500.0), ("Βιολογικά", 300.0)]
        result = biologic_pct(rows, 800.0)
        self.assertAlmostEqual(result, 100.0)

    def test_half_biologic(self):
        rows = [("Βιολογικά", 500.0), ("Συμβατικά", 500.0)]
        result = biologic_pct(rows, 1000.0)
        self.assertAlmostEqual(result, 50.0)

    def test_no_biologic(self):
        rows = [("Συμβατικά", 500.0), ("Συμβατικά", 300.0)]
        result = biologic_pct(rows, 800.0)
        self.assertAlmostEqual(result, 0.0)

    def test_mixed_systems(self):
        """Βιολογικά + ΠΟΠ/ΠΓΕ both count."""
        rows = [("Βιολογικά", 400.0), ("ΠΟΠ/ΠΓΕ", 200.0), ("Συμβατικά", 400.0)]
        result = biologic_pct(rows, 1000.0)
        self.assertAlmostEqual(result, 60.0)

    def test_zero_total(self):
        rows = [("Βιολογικά", 100.0)]
        result = biologic_pct(rows, 0)
        self.assertIsNone(result)

    def test_none_total(self):
        rows = [("Βιολογικά", 100.0)]
        result = biologic_pct(rows, None)
        self.assertIsNone(result)

    def test_empty_rows(self):
        """No rows with quality systems → 0%."""
        result = biologic_pct([], 1000.0)
        self.assertAlmostEqual(result, 0.0)

    def test_default_excluded(self):
        """--Επιλέξτε should be excluded."""
        rows = [("--Επιλέξτε", 500.0)]
        result = biologic_pct(rows, 500.0)
        self.assertAlmostEqual(result, 0.0)

    def test_oloklirwmeni(self):
        """Ολοκληρωμένη should count as quality system."""
        rows = [("Ολοκληρωμένη", 600.0)]
        result = biologic_pct(rows, 1000.0)
        self.assertAlmostEqual(result, 60.0)

    def test_unknown_value_not_counted(self):
        """Τιμή εκτός INCLUDED whitelist (π.χ. typo) → δεν προσμετράται."""
        rows = [("Βιολογικά", 500.0), ("Foo", 300.0)]
        result = biologic_pct(rows, 800.0)
        self.assertAlmostEqual(result, 62.5)  # 500/800

    def test_conventional_excluded(self):
        """Συμβατικά → εκτός INCLUDED → 0%."""
        rows = [("Συμβατικά", 1000.0)]
        result = biologic_pct(rows, 1000.0)
        self.assertAlmostEqual(result, 0.0)

    def test_pop_pge(self):
        """ΠΟΠ/ΠΓΕ should count."""
        rows = [("ΠΟΠ/ΠΓΕ", 400.0)]
        result = biologic_pct(rows, 1000.0)
        self.assertAlmostEqual(result, 40.0)


if __name__ == '__main__':
    unittest.main()
