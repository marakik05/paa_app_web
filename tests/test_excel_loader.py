"""
Unit tests for utils/excel_loader.py
Tests: norm(), in_norm_set(), contains_norm_keyword(), resource_path(), constants.
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.excel_loader import (
    norm, in_norm_set, contains_norm_keyword, resource_path,
    PERIFERIES, AEGEAN_PERIFERIES, ISLANDS, DEFAULT,
    FMZ_ZWIKI_NORM, FMZ_MELISSES_NORM,
    LOCK_AMPELI_NORM, LOCK_TREES_NORM,
    PARAGWGIKA_NORM, PARAGWGIKA_CAT_NORM, NORM_YES,
    load_excel_data
)


# ─── norm() ──────────────────────────────────────────────────────────

class TestNorm(unittest.TestCase):

    def test_basic_lowercase(self):
        self.assertEqual(norm("ΑΙΓΟΠΡΟΒΑΤΑ"), norm("αιγοπροβατα"))

    def test_strip_whitespace(self):
        self.assertEqual(norm("  ΒΟΟΕΙΔΗ  "), norm("ΒΟΟΕΙΔΗ"))

    def test_accent_removal(self):
        """Accented Greek letters should match unaccented."""
        self.assertEqual(norm("Κρήτη"), norm("Κρητη"))
        self.assertEqual(norm("Αττική"), norm("Αττικη"))

    def test_final_sigma(self):
        """ς and σ should be normalized to the same character."""
        self.assertEqual(norm("ΜΕΤΑΞΟΣΚΩΛΗΚΕΣ"), norm("ΜΕΤΑΞΟΣΚΩΛΗΚΕΣ"))
        result = norm("ς")
        self.assertEqual(result, norm("σ"))

    def test_latin_to_greek(self):
        """Latin characters that look like Greek should be converted."""
        # 'o' (latin) → 'ο' (greek)
        result = norm("BOΟΕΙΔΗ")  # first O is latin, second is greek
        self.assertIn("ο", result)

    def test_empty_string(self):
        self.assertEqual(norm(""), "")

    def test_none_input(self):
        self.assertEqual(norm(None), "")

    def test_multiple_spaces_collapsed(self):
        self.assertEqual(norm("A   B   C"), norm("A B C"))


# ─── in_norm_set() ───────────────────────────────────────────────────

class TestInNormSet(unittest.TestCase):

    def test_exact_match(self):
        test_set = {norm("ΑΙΓΟΠΡΟΒΑΤΑ"), norm("ΒΟΟΕΙΔΗ")}
        self.assertTrue(in_norm_set("ΑΙΓΟΠΡΟΒΑΤΑ", test_set))
        self.assertTrue(in_norm_set("αιγοπροβατα", test_set))

    def test_no_match(self):
        test_set = {norm("ΑΙΓΟΠΡΟΒΑΤΑ")}
        self.assertFalse(in_norm_set("ΧΟΙΡΟΙ", test_set))

    def test_with_accents(self):
        test_set = {norm("Κρήτη")}
        self.assertTrue(in_norm_set("ΚΡΗΤΗ", test_set))
        self.assertTrue(in_norm_set("Κρήτη", test_set))

    def test_empty_value(self):
        test_set = {norm("ΑΙΓΟΠΡΟΒΑΤΑ")}
        self.assertFalse(in_norm_set("", test_set))


# ─── contains_norm_keyword() ─────────────────────────────────────────

class TestContainsNormKeyword(unittest.TestCase):

    def test_keyword_found(self):
        keywords = {norm("ΕΡΙΦΙΑ"), norm("ΑΙΓΕΣ")}
        self.assertTrue(contains_norm_keyword("ΕΡΙΦΙΑ ΘΗΛΥΚΑ", keywords))

    def test_keyword_not_found(self):
        keywords = {norm("ΕΡΙΦΙΑ")}
        self.assertFalse(contains_norm_keyword("ΒΟΟΕΙΔΗ", keywords))

    def test_partial_match(self):
        """Keyword should be found inside a longer string."""
        keywords = {norm("ΑΙΓΕΣ")}
        self.assertTrue(contains_norm_keyword("ΑΙΓΕΣ ΓΑΛΑΚΤΟΠΑΡΑΓΩΓΗΣ", keywords))

    def test_case_insensitive(self):
        keywords = {norm("ΠΡΟΒΑΤΙΝΕΣ")}
        self.assertTrue(contains_norm_keyword("προβατινες", keywords))

    def test_empty_value(self):
        keywords = {norm("ΕΡΙΦΙΑ")}
        self.assertFalse(contains_norm_keyword("", keywords))


# ─── Constants validation ────────────────────────────────────────────

class TestConstants(unittest.TestCase):

    def test_periferies_is_list(self):
        self.assertIsInstance(PERIFERIES, list)

    def test_periferies_starts_with_default(self):
        self.assertEqual(PERIFERIES[0], DEFAULT)

    def test_periferies_count(self):
        """Should have 14 entries (1 default + 13 regions)."""
        self.assertEqual(len(PERIFERIES), 14)

    def test_default_value(self):
        self.assertEqual(DEFAULT, "--Επιλέξτε")

    def test_aegean_periferies(self):
        self.assertIn("Κρήτη", AEGEAN_PERIFERIES)
        self.assertIn("Νότιο Αιγαίο", AEGEAN_PERIFERIES)
        self.assertIn("Βόρειο Αιγαίο", AEGEAN_PERIFERIES)
        self.assertEqual(len(AEGEAN_PERIFERIES), 3)

    def test_islands(self):
        self.assertIn("Νότιο Αιγαίο", ISLANDS)
        self.assertIn("Βόρειο Αιγαίο", ISLANDS)
        self.assertIn("Ιόνια Νησιά", ISLANDS)
        self.assertEqual(len(ISLANDS), 3)

    def test_norm_yes(self):
        self.assertEqual(NORM_YES, norm("ΝΑΙ"))

    def test_fmz_zwiki_norm_not_empty(self):
        self.assertTrue(len(FMZ_ZWIKI_NORM) > 0)

    def test_fmz_melisses_norm_not_empty(self):
        self.assertTrue(len(FMZ_MELISSES_NORM) > 0)

    def test_lock_ampeli_norm_not_empty(self):
        self.assertTrue(len(LOCK_AMPELI_NORM) > 0)

    def test_lock_trees_contains_non_tree_categories(self):
        """LOCK_TREES should contain animal/vine categories that lock tree columns."""
        self.assertTrue(in_norm_set("ΑΙΓΟΠΡΟΒΑΤΑ", LOCK_TREES_NORM))
        self.assertTrue(in_norm_set("ΒΟΟΕΙΔΗ", LOCK_TREES_NORM))

    def test_paragwgika_cat_norm(self):
        self.assertTrue(in_norm_set("ΑΙΓΟΠΡΟΒΑΤΑ", PARAGWGIKA_CAT_NORM))

    def test_paragwgika_norm_keywords(self):
        self.assertTrue(in_norm_set("ΕΡΙΦΙΑ ΘΗΛΥΚΑ", PARAGWGIKA_NORM))
        self.assertTrue(in_norm_set("ΑΙΓΕΣ", PARAGWGIKA_NORM))
        self.assertTrue(in_norm_set("ΠΡΟΒΑΤΙΝΕΣ", PARAGWGIKA_NORM))

    def test_norm_sets_are_all_normalized(self):
        """Every element in norm sets should equal norm() of itself."""
        for s in (FMZ_ZWIKI_NORM, FMZ_MELISSES_NORM, LOCK_AMPELI_NORM,
                  LOCK_TREES_NORM, PARAGWGIKA_NORM, PARAGWGIKA_CAT_NORM):
            for item in s:
                self.assertEqual(item, norm(item),
                                 msg="{} is not normalized".format(item))

    def test_aegean_and_islands_overlap(self):
        """Βόρειο & Νότιο Αιγαίο should be in both sets."""
        overlap = AEGEAN_PERIFERIES & ISLANDS
        self.assertIn("Νότιο Αιγαίο", overlap)
        self.assertIn("Βόρειο Αιγαίο", overlap)

    def test_islands_not_subset_of_aegean(self):
        """Ιόνια Νησιά is in ISLANDS but not in AEGEAN_PERIFERIES."""
        self.assertIn("Ιόνια Νησιά", ISLANDS)
        self.assertNotIn("Ιόνια Νησιά", AEGEAN_PERIFERIES)


# ─── resource_path() ─────────────────────────────────────────────────

class TestResourcePath(unittest.TestCase):

    def test_returns_string(self):
        result = resource_path("data/ta.xlsx")
        self.assertIsInstance(result, str)

    def test_contains_relative_part(self):
        result = resource_path("data/ta.xlsx")
        self.assertTrue(result.endswith("data/ta.xlsx") or
                        result.endswith("data\\ta.xlsx"))

    def test_is_absolute(self):
        result = resource_path("data/ta.xlsx")
        self.assertTrue(os.path.isabs(result))


# ─── load_excel_data() ───────────────────────────────────────────────

class TestLoadExcelData(unittest.TestCase):

    def setUp(self):
        self.excel_path = resource_path("data/ta.xlsx")

    def test_loads_without_error(self):
        if not os.path.exists(self.excel_path):
            self.skipTest("ta.xlsx not found at {}".format(self.excel_path))
        mapping, value_mapping = load_excel_data(self.excel_path)
        self.assertIsInstance(mapping, dict)
        self.assertIsInstance(value_mapping, dict)

    def test_mapping_has_entries(self):
        if not os.path.exists(self.excel_path):
            self.skipTest("ta.xlsx not found")
        mapping, _ = load_excel_data(self.excel_path)
        self.assertTrue(len(mapping) > 0)

    def test_value_mapping_has_default_and_aegean(self):
        if not os.path.exists(self.excel_path):
            self.skipTest("ta.xlsx not found")
        _, value_mapping = load_excel_data(self.excel_path)
        for key, val in list(value_mapping.items())[:5]:
            self.assertIn("default", val)
            self.assertIn("aegean", val)

    def test_mapping_values_are_sorted_lists(self):
        if not os.path.exists(self.excel_path):
            self.skipTest("ta.xlsx not found")
        mapping, _ = load_excel_data(self.excel_path)
        for crop, variants in list(mapping.items())[:5]:
            self.assertIsInstance(variants, list)
            self.assertEqual(variants, sorted(variants))


if __name__ == '__main__':
    unittest.main()
