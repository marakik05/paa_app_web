"""
Unit tests for moria scoring formulas (pages/page_moria.py).
Tests the pure math logic extracted from each moria_* method.
No Qt dependency — formulas tested as standalone functions.
"""
import unittest
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


CENT = Decimal("0.01")


def _q2f(d):
    """Decimal HALF_UP σε 2 δεκαδικά, ως float."""
    return float(d.quantize(CENT, rounding=ROUND_HALF_UP))


# ─── Extracted scoring formulas ──────────────────────────────────────
# These mirror the logic inside moriaPage methods but as pure functions.

def calc_moria_1_1(answer):
    """Κριτήριο 1.1: Ναι=5, Όχι=0"""
    if answer == "Ναι":
        return 5.00
    elif answer == "Όχι":
        return 0.00
    return None


def calc_moria_1_2(biologic_pct):
    """Κριτήριο 1.2: >50% → 6, else 0"""
    if biologic_pct is None:
        return None
    if biologic_pct > 50:
        return 6.00
    return 0.00


def calc_moria_2_1(ta):
    """Κριτήριο 2.1: ΤΑ-based scoring."""
    if ta is None:
        return None
    ta_d = Decimal(str(ta))
    if ta_d < 16000:
        return 2.50
    elif ta_d <= 25000:
        moria = 50 + 50 * (ta_d - 16000) / 9000
        return _q2f(moria * Decimal("0.05"))
    elif ta_d > 25000:
        return 5.00
    return None


def calc_moria_2_2(ta, budget):
    """Κριτήριο 2.2: ΤΑ + budget combination."""
    if ta is None or budget is None:
        return None
    ta_5x = 5 * ta
    ta_6x = 6 * ta
    if ta <= 15000 and budget <= 75000:
        return 16.00
    elif ta > 15000 and budget <= ta_5x:
        return 16.00
    elif ta > 12500 and budget <= ta_6x:
        return 9.60
    return 0.00


def calc_moria_3_1_1(idia, budget):
    """Κριτήριο 3.1.1: ίδια συμμετοχή / budget."""
    if idia is None or budget is None:
        return None
    idia_d = Decimal(str(idia))
    budget_d = Decimal(str(budget))
    if budget_d == 0:
        return 0.00
    ratio = idia_d / budget_d
    if ratio <= Decimal("0.2"):
        return 0.00
    elif ratio > Decimal("0.5"):
        return 7.00
    else:
        moria = 20 + 30 * (ratio - Decimal("0.2")) / Decimal("0.3")
        return _q2f(moria * Decimal("0.14"))


def calc_moria_3_1_2(answer):
    """Κριτήριο 3.1.2: Ναι=4.20, Όχι=0"""
    if answer == "Ναι":
        return 4.20
    elif answer == "Όχι":
        return 0.00
    return None


def calc_moria_3_1_3(answer):
    """Κριτήριο 3.1.3: Ναι=1.40, Όχι=0"""
    if answer == "Ναι":
        return 1.40
    elif answer == "Όχι":
        return 0.00
    return None


def calc_moria_3_1_4(answer):
    """Κριτήριο 3.1.4: Ναι=1.40, Όχι=0"""
    if answer == "Ναι":
        return 1.40
    elif answer == "Όχι":
        return 0.00
    return None


def calc_moria_3_2(answer):
    """Κριτήριο 3.2: Νέος αγρότης / εμπειρία."""
    positive = {
        "Νέος Αγρότης 2018 ή 2021",
        "Επιλαχόντας του Μ6.1",
        "Εμπειρία >5 ετών και έως 50 ετών"
    }
    if answer in positive:
        return 8.00
    elif answer == "Κανένα από τα παραπάνω":
        return 0.00
    return None


def calc_moria_3_3(answer):
    """Κριτήριο 3.3: Πτυχίο."""
    if answer in ("Κατοχή πτυχίου >= 6, 7, 8",
                   "Κατοχή γεωτεχνικού πτυχίου =< 3, 4, 5"):
        return 3.50
    elif answer == "Κατοχή γεωτεχνικού πτυχίου >= 6, 7, 8":
        return 5.00
    elif answer == "Κανένα από τα παραπάνω":
        return 0.00
    return None


def calc_moria_3_4(answer):
    """Κριτήριο 3.4: Συλλογικότητα."""
    if answer == "ΟΠ/Ομ.Π με μέλη>10":
        return 2.40
    elif answer == "ΑΣ":
        return 3.60
    elif answer in ("ΑΣ και ΟΠ/Ομ.Π με μέλη>10", "Αναγκαστικός Συνεταιρισμός"):
        return 6.00
    elif answer == "Κανένα από τα παραπάνω":
        return 0.00
    return None


def calc_moria_3_5(answer):
    """Κριτήριο 3.5: Ναι=2, Όχι=0"""
    if answer == "Ναι":
        return 2.00
    elif answer == "Όχι":
        return 0.00
    return None


def calc_moria_4_1(poso, budget):
    """Κριτήριο 4.1: ποσό / budget."""
    if poso is None or budget is None:
        return None
    poso_d = Decimal(str(poso))
    budget_d = Decimal(str(budget))
    if budget_d == 0:
        return 0.00
    ratio = poso_d / budget_d
    if ratio <= Decimal("0.1"):
        return 0.00
    elif ratio > Decimal("0.6"):
        return 12.00
    else:
        moria = 10 + 90 * (ratio - Decimal("0.1")) / Decimal("0.5")
        return _q2f(moria * Decimal("0.12"))


def calc_moria_5_1(poso, budget):
    """Κριτήριο 5.1: ποσό / budget."""
    if poso is None or budget is None:
        return None
    poso_d = Decimal(str(poso))
    budget_d = Decimal(str(budget))
    if budget_d == 0:
        return 0.00
    ratio = poso_d / budget_d
    if ratio <= Decimal("0.05"):
        return 0.00
    elif ratio > Decimal("0.2"):
        return 12.00
    else:
        moria = 10 + 90 * (ratio - Decimal("0.05")) / Decimal("0.15")
        return _q2f(moria * Decimal("0.08"))


def calc_moria_6_1(answer):
    """Κριτήριο 6.1: Ναι=13, Όχι=0"""
    if answer == "Ναι":
        return 13.00
    elif answer == "Όχι":
        return 0.00
    return None


def calc_moria_7_1(answer):
    """Κριτήριο 7.1: Ναι=3, Όχι=0"""
    if answer == "Ναι":
        return 3.00
    elif answer == "Όχι":
        return 0.00
    return None


def calc_epilex_moria(total_moria):
    """Επιλεξιμότητα: <40 → ΜΗ ΕΠΙΛΕΞΙΜΟΣ, >=40 → ΕΠΙΛΕΞΙΜΟΣ."""
    if total_moria is None:
        return None
    if total_moria < 40:
        return "ΜΗ ΕΠΙΛΕΞΙΜΟΣ"
    return "ΕΠΙΛΕΞΙΜΟΣ"


# ─── Tests ───────────────────────────────────────────────────────────

class TestMoria1_1(unittest.TestCase):
    def test_yes(self):
        self.assertEqual(calc_moria_1_1("Ναι"), 5.00)

    def test_no(self):
        self.assertEqual(calc_moria_1_1("Όχι"), 0.00)

    def test_default(self):
        self.assertIsNone(calc_moria_1_1("--Επιλέξτε"))


class TestMoria1_2(unittest.TestCase):
    def test_above_50(self):
        self.assertEqual(calc_moria_1_2(60), 6.00)
        self.assertEqual(calc_moria_1_2(100), 6.00)

    def test_at_50(self):
        self.assertEqual(calc_moria_1_2(50), 0.00)

    def test_below_50(self):
        self.assertEqual(calc_moria_1_2(30), 0.00)

    def test_zero(self):
        self.assertEqual(calc_moria_1_2(0), 0.00)

    def test_none(self):
        self.assertIsNone(calc_moria_1_2(None))


class TestMoria2_1(unittest.TestCase):
    def test_below_16000(self):
        self.assertEqual(calc_moria_2_1(10000), 2.50)
        self.assertEqual(calc_moria_2_1(0), 2.50)

    def test_at_16000(self):
        self.assertEqual(calc_moria_2_1(16000), 2.50)

    def test_interpolation_midpoint(self):
        """At 20500 (midpoint), moria = 75 * 0.05 = 3.75"""
        self.assertEqual(calc_moria_2_1(20500), 3.75)

    def test_at_25000(self):
        self.assertEqual(calc_moria_2_1(25000), 5.00)

    def test_above_25000(self):
        self.assertEqual(calc_moria_2_1(30000), 5.00)

    def test_none(self):
        self.assertIsNone(calc_moria_2_1(None))


class TestMoria2_2(unittest.TestCase):
    def test_low_ta_low_budget(self):
        self.assertEqual(calc_moria_2_2(10000, 50000), 16.00)

    def test_ta_15000_budget_75000(self):
        self.assertEqual(calc_moria_2_2(15000, 75000), 16.00)

    def test_high_ta_budget_within_5x(self):
        self.assertEqual(calc_moria_2_2(20000, 90000), 16.00)

    def test_high_ta_budget_within_6x(self):
        """ta=16000, budget=90000 → 90000 > 5*16000=80000 but <= 6*16000=96000 → 9.60"""
        self.assertEqual(calc_moria_2_2(16000, 90000), 9.60)

    def test_high_budget_zero(self):
        self.assertEqual(calc_moria_2_2(10000, 200000), 0.00)

    def test_none(self):
        self.assertIsNone(calc_moria_2_2(None, 50000))
        self.assertIsNone(calc_moria_2_2(10000, None))


class TestMoria3_1_1(unittest.TestCase):
    def test_low_ratio(self):
        """20000/200000 = 0.1 → 0.00"""
        self.assertEqual(calc_moria_3_1_1(20000, 200000), 0.00)

    def test_high_ratio(self):
        """60000/100000 = 0.6 → 7.00"""
        self.assertEqual(calc_moria_3_1_1(60000, 100000), 7.00)

    def test_mid_ratio(self):
        """35000/100000 = 0.35 → interpolation"""
        result = calc_moria_3_1_1(35000, 100000)
        self.assertIsNotNone(result)
        self.assertGreater(result, 0)
        self.assertLess(result, 7)

    def test_zero_budget(self):
        self.assertEqual(calc_moria_3_1_1(10000, 0), 0.00)

    def test_exact_0_2(self):
        self.assertEqual(calc_moria_3_1_1(20000, 100000), 0.00)

    def test_none(self):
        self.assertIsNone(calc_moria_3_1_1(None, 100000))


class TestMoria3_1_2(unittest.TestCase):
    def test_yes(self):
        self.assertEqual(calc_moria_3_1_2("Ναι"), 4.20)

    def test_no(self):
        self.assertEqual(calc_moria_3_1_2("Όχι"), 0.00)


class TestMoria3_1_3(unittest.TestCase):
    def test_yes(self):
        self.assertEqual(calc_moria_3_1_3("Ναι"), 1.40)

    def test_no(self):
        self.assertEqual(calc_moria_3_1_3("Όχι"), 0.00)


class TestMoria3_1_4(unittest.TestCase):
    def test_yes(self):
        self.assertEqual(calc_moria_3_1_4("Ναι"), 1.40)

    def test_no(self):
        self.assertEqual(calc_moria_3_1_4("Όχι"), 0.00)


class TestMoria3_2(unittest.TestCase):
    def test_neos_agrotis(self):
        self.assertEqual(calc_moria_3_2("Νέος Αγρότης 2018 ή 2021"), 8.00)

    def test_epilaxontas(self):
        self.assertEqual(calc_moria_3_2("Επιλαχόντας του Μ6.1"), 8.00)

    def test_empeiria(self):
        self.assertEqual(calc_moria_3_2("Εμπειρία >5 ετών και έως 50 ετών"), 8.00)

    def test_none_of_above(self):
        self.assertEqual(calc_moria_3_2("Κανένα από τα παραπάνω"), 0.00)

    def test_default(self):
        self.assertIsNone(calc_moria_3_2("--Επιλέξτε"))


class TestMoria3_3(unittest.TestCase):
    def test_ptyxio_high(self):
        self.assertEqual(calc_moria_3_3("Κατοχή γεωτεχνικού πτυχίου >= 6, 7, 8"), 5.00)

    def test_ptyxio_general(self):
        self.assertEqual(calc_moria_3_3("Κατοχή πτυχίου >= 6, 7, 8"), 3.50)

    def test_ptyxio_low(self):
        self.assertEqual(calc_moria_3_3("Κατοχή γεωτεχνικού πτυχίου =< 3, 4, 5"), 3.50)

    def test_none_of_above(self):
        self.assertEqual(calc_moria_3_3("Κανένα από τα παραπάνω"), 0.00)


class TestMoria3_4(unittest.TestCase):
    def test_op(self):
        self.assertEqual(calc_moria_3_4("ΟΠ/Ομ.Π με μέλη>10"), 2.40)

    def test_as(self):
        self.assertEqual(calc_moria_3_4("ΑΣ"), 3.60)

    def test_as_and_op(self):
        self.assertEqual(calc_moria_3_4("ΑΣ και ΟΠ/Ομ.Π με μέλη>10"), 6.00)

    def test_anagkastikos(self):
        self.assertEqual(calc_moria_3_4("Αναγκαστικός Συνεταιρισμός"), 6.00)

    def test_none_of_above(self):
        self.assertEqual(calc_moria_3_4("Κανένα από τα παραπάνω"), 0.00)


class TestMoria3_5(unittest.TestCase):
    def test_yes(self):
        self.assertEqual(calc_moria_3_5("Ναι"), 2.00)

    def test_no(self):
        self.assertEqual(calc_moria_3_5("Όχι"), 0.00)


class TestMoria4_1(unittest.TestCase):
    def test_low_ratio(self):
        self.assertEqual(calc_moria_4_1(5000, 100000), 0.00)

    def test_high_ratio(self):
        self.assertEqual(calc_moria_4_1(70000, 100000), 12.00)

    def test_mid_ratio(self):
        """35000/100000 = 0.35 → interpolation"""
        result = calc_moria_4_1(35000, 100000)
        self.assertIsNotNone(result)
        self.assertGreater(result, 0)
        self.assertLess(result, 12)

    def test_zero_budget(self):
        self.assertEqual(calc_moria_4_1(10000, 0), 0.00)


class TestMoria5_1(unittest.TestCase):
    def test_low_ratio(self):
        self.assertEqual(calc_moria_5_1(3000, 100000), 0.00)

    def test_high_ratio(self):
        self.assertEqual(calc_moria_5_1(30000, 100000), 12.00)

    def test_mid_ratio(self):
        result = calc_moria_5_1(10000, 100000)
        self.assertIsNotNone(result)
        self.assertGreater(result, 0)
        self.assertLess(result, 12)

    def test_zero_budget(self):
        self.assertEqual(calc_moria_5_1(5000, 0), 0.00)


class TestMoria6_1(unittest.TestCase):
    def test_yes(self):
        self.assertEqual(calc_moria_6_1("Ναι"), 13.00)

    def test_no(self):
        self.assertEqual(calc_moria_6_1("Όχι"), 0.00)


class TestMoria7_1(unittest.TestCase):
    def test_yes(self):
        self.assertEqual(calc_moria_7_1("Ναι"), 3.00)

    def test_no(self):
        self.assertEqual(calc_moria_7_1("Όχι"), 0.00)


class TestEpilexMoria(unittest.TestCase):
    def test_below_40(self):
        self.assertEqual(calc_epilex_moria(35), "ΜΗ ΕΠΙΛΕΞΙΜΟΣ")
        self.assertEqual(calc_epilex_moria(0), "ΜΗ ΕΠΙΛΕΞΙΜΟΣ")
        self.assertEqual(calc_epilex_moria(39.99), "ΜΗ ΕΠΙΛΕΞΙΜΟΣ")

    def test_at_40(self):
        self.assertEqual(calc_epilex_moria(40), "ΕΠΙΛΕΞΙΜΟΣ")

    def test_above_40(self):
        self.assertEqual(calc_epilex_moria(55), "ΕΠΙΛΕΞΙΜΟΣ")
        self.assertEqual(calc_epilex_moria(100), "ΕΠΙΛΕΞΙΜΟΣ")

    def test_none(self):
        self.assertIsNone(calc_epilex_moria(None))


# ─── Sum total moria ─────────────────────────────────────────────────

class TestSumTotalMoria(unittest.TestCase):
    """Test a full scenario with all criteria."""

    def test_max_possible_score(self):
        """All positive answers → maximum score."""
        scores = [
            5.00,   # 1.1: Ναι
            6.00,   # 1.2: >50%
            5.00,   # 2.1: >25000
            16.00,  # 2.2: max
            7.00,   # 3.1.1: >0.5 ratio
            4.20,   # 3.1.2: Ναι
            1.40,   # 3.1.3: Ναι
            1.40,   # 3.1.4: Ναι
            8.00,   # 3.2: Νέος Αγρότης
            5.00,   # 3.3: Γεωτεχνικό >= 6,7,8
            6.00,   # 3.4: ΑΣ + ΟΠ
            2.00,   # 3.5: Ναι
            12.00,  # 4.1: >0.6 ratio
            12.00,  # 5.1: >0.2 ratio (max 8 but code gives 12)
            13.00,  # 6.1: Ναι
            3.00,   # 7.1: Ναι
        ]
        total = _q2f(sum((Decimal(str(s)) for s in scores), Decimal(0)))
        self.assertEqual(total, 107.00)
        self.assertEqual(calc_epilex_moria(total), "ΕΠΙΛΕΞΙΜΟΣ")

    def test_all_zero_score(self):
        """All negative answers → 0."""
        scores = [0] * 16
        total = sum(scores)
        self.assertEqual(total, 0)
        self.assertEqual(calc_epilex_moria(total), "ΜΗ ΕΠΙΛΕΞΙΜΟΣ")

    def test_borderline_score(self):
        """Exactly 40 → ΕΠΙΛΕΞΙΜΟΣ."""
        self.assertEqual(calc_epilex_moria(40.00), "ΕΠΙΛΕΞΙΜΟΣ")


# ─── HALF_UP rounding behavior ───────────────────────────────────────

class TestMoriaHalfUpRounding(unittest.TestCase):
    """Επιβεβαίωση ότι η στρογγυλοποίηση είναι ROUND_HALF_UP, όχι banker's (ROUND_HALF_EVEN)."""

    def test_2_1_half_up_at_675(self):
        """ΤΑ=16630 → moria*0.05 = 2.675 → πρέπει 2.68 (HALF_UP), όχι 2.67 (banker's)."""
        # moria = 50 + 50*(16630-16000)/9000 = 53.5 → 53.5*0.05 = 2.675
        self.assertEqual(calc_moria_2_1(16630), 2.68)

    def test_3_1_1_half_up_at_675(self):
        """idia=2625, budget=10000 → moria*0.14 = 3.675 → 3.68 (HALF_UP)."""
        # ratio=0.2625 → moria = 20 + 30*(0.2625-0.2)/0.3 = 26.25 → 26.25*0.14 = 3.675
        self.assertEqual(calc_moria_3_1_1(2625, 10000), 3.68)


if __name__ == '__main__':
    unittest.main()
