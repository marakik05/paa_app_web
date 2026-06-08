"""
Unit tests for database_manager.py
Tests: setup, CRUD operations, migrations, batch import, helper functions.
"""
import unittest
import sqlite3
import os
import tempfile
import shutil
from unittest.mock import patch

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import database_manager as db


class _TempDBMixin:
    """Mixin: redirects DB_PATH to a temp file, cleaned up after each test."""

    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()
        self._tmp_db = os.path.join(self._tmp_dir, 'test.db')
        self._orig_path = db.DB_PATH
        db.DB_PATH = self._tmp_db

    def tearDown(self):
        db.DB_PATH = self._orig_path
        shutil.rmtree(self._tmp_dir, ignore_errors=True)


# ─── Setup & Schema ─────────────────────────────────────────────────

class TestSetupDatabase(_TempDBMixin, unittest.TestCase):

    def test_creates_all_tables(self):
        db.setup_database()
        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = {r[0] for r in cur.fetchall()}
        conn.close()
        for t in ('producers', 'osde_entries', 'eligibility', 'moria'):
            self.assertIn(t, tables)

    def test_schema_version_set(self):
        db.setup_database()
        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        cur.execute("PRAGMA user_version")
        version = cur.fetchone()[0]
        conn.close()
        self.assertEqual(version, db.SCHEMA_VERSION)

    def test_setup_idempotent(self):
        """Calling setup_database twice should not fail."""
        db.setup_database()
        db.setup_database()

    def test_foreign_keys_cascade(self):
        """Deleting a producer cascades to osde_entries."""
        db.setup_database()
        db.save_producer_basics('111111111', 'Test', 'User', 'Αττική')
        db.save_scenario_data('111111111', 'initial', [
            ('111111111', 'initial', 'CAT', 'DESC', 100.0, 5.0,
             'Συμβατικά', 0, 0, '', 500.0, 500.0, 500.0, 0, 0, 0)
        ])
        entries_before = db.fetch_entries('111111111', 'initial')
        self.assertTrue(len(entries_before) > 0)

        db.delete_producer('111111111')

        entries_after = db.fetch_entries('111111111', 'initial')
        self.assertEqual(len(entries_after), 0)


# ─── Migrations ──────────────────────────────────────────────────────

class TestMigrations(_TempDBMixin, unittest.TestCase):

    def test_migration_upgrades_version(self):
        """Fresh DB (user_version=0) → μετά από setup_database με bumped SCHEMA_VERSION,
        το user_version ανεβαίνει στη νέα έκδοση."""
        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        cur.execute("PRAGMA user_version")
        self.assertEqual(cur.fetchone()[0], 0)
        conn.close()

        # Προσομοίωση future release με bumped SCHEMA_VERSION
        with patch.object(db, 'SCHEMA_VERSION', 5):
            db.setup_database()

        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        cur.execute("PRAGMA user_version")
        self.assertEqual(cur.fetchone()[0], 5)
        conn.close()

    def test_migration_skipped_if_current(self):
        """If user_version >= SCHEMA_VERSION, _run_migrations is a no-op."""
        db.setup_database()
        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        cur.execute("PRAGMA user_version = 999")
        conn.commit()
        conn.close()

        # Should not fail
        db.setup_database()

        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        cur.execute("PRAGMA user_version")
        self.assertEqual(cur.fetchone()[0], 999)
        conn.close()


# ─── Column helpers ──────────────────────────────────────────────────

class TestColumnHelpers(_TempDBMixin, unittest.TestCase):

    def test_column_exists_true(self):
        db.setup_database()
        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        self.assertTrue(db._column_exists(cur, 'producers', 'afm'))
        conn.close()

    def test_column_exists_false(self):
        db.setup_database()
        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        self.assertFalse(db._column_exists(cur, 'producers', 'nonexistent_col'))
        conn.close()

    def test_add_column_if_missing(self):
        db.setup_database()
        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        self.assertFalse(db._column_exists(cur, 'producers', 'test_col'))
        db._add_column_if_missing(cur, 'producers', 'test_col', 'TEXT')
        self.assertTrue(db._column_exists(cur, 'producers', 'test_col'))
        conn.close()

    def test_add_column_if_missing_no_duplicate(self):
        """Adding a column that already exists should not fail."""
        db.setup_database()
        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        db._add_column_if_missing(cur, 'producers', 'afm', 'TEXT')  # already exists
        conn.close()


# ─── Producer CRUD ───────────────────────────────────────────────────

class TestProducerCRUD(_TempDBMixin, unittest.TestCase):

    def setUp(self):
        super().setUp()
        db.setup_database()

    def test_save_and_fetch_producer(self):
        db.save_producer_basics('123456789', 'Γιάννης', 'Παπαδόπουλος', 'Αττική')
        result = db.fetch_producer('123456789')
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'Γιάννης')
        self.assertEqual(result[1], 'Παπαδόπουλος')
        self.assertEqual(result[2], 'Αττική')

    def test_fetch_nonexistent_producer(self):
        result = db.fetch_producer('000000000')
        self.assertIsNone(result)

    def test_save_producer_update(self):
        """INSERT OR REPLACE updates existing producer."""
        db.save_producer_basics('123456789', 'Γιάννης', 'Παπαδόπουλος', 'Αττική')
        db.save_producer_basics('123456789', 'Νίκος', 'Παπαδόπουλος', 'Κρήτη')
        result = db.fetch_producer('123456789')
        self.assertEqual(result[0], 'Νίκος')
        self.assertEqual(result[2], 'Κρήτη')

    def test_delete_producer(self):
        db.save_producer_basics('123456789', 'Γιάννης', 'Παπαδόπουλος', 'Αττική')
        success = db.delete_producer('123456789')
        self.assertTrue(success)
        result = db.fetch_producer('123456789')
        self.assertIsNone(result)

    def test_delete_nonexistent_producer(self):
        """Deleting a non-existent producer should still return True (no error)."""
        success = db.delete_producer('999999999')
        self.assertTrue(success)

    def test_fetch_all_producers(self):
        db.save_producer_basics('111111111', 'A', 'A', 'Αττική')
        db.save_producer_basics('222222222', 'B', 'B', 'Κρήτη')
        results = db.fetch_all_producers()
        afms = [r[0] for r in results]
        self.assertIn('111111111', afms)
        self.assertIn('222222222', afms)

    def test_fetch_all_producers_empty(self):
        results = db.fetch_all_producers()
        self.assertEqual(len(results), 0)

    def test_fetch_all_producers_ordered_by_afm_asc(self):
        """Η αρχική στηρίζεται στο ORDER BY p.afm ASC — μη το αλλάξεις."""
        db.save_producer_basics('300000000', 'C', 'C', 'Αττική')
        db.save_producer_basics('100000000', 'A', 'A', 'Αττική')
        db.save_producer_basics('200000000', 'B', 'B', 'Αττική')
        afms = [r[0] for r in db.fetch_all_producers()]
        self.assertEqual(afms, ['100000000', '200000000', '300000000'])


# ─── Scenario Data (osde_entries) ────────────────────────────────────

class TestScenarioData(_TempDBMixin, unittest.TestCase):

    def setUp(self):
        super().setUp()
        db.setup_database()
        db.save_producer_basics('123456789', 'Test', 'User', 'Αττική')

    def _make_entry(self, cat='CAT1', desc='DESC1', ta=100.0, qty=5.0):
        return ('123456789', 'initial', cat, desc, ta, qty,
                'Συμβατικά', 0, 0, '', ta * qty, ta * qty, ta * qty, 0, 0, 0)

    def test_save_and_fetch_entries(self):
        db.save_scenario_data('123456789', 'initial', [self._make_entry()])
        rows = db.fetch_entries('123456789', 'initial')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][3], 'CAT1')  # category_osde
        self.assertEqual(rows[0][4], 'DESC1')  # description

    def test_save_replaces_old_entries(self):
        """Saving scenario data should delete old entries for that scenario."""
        db.save_scenario_data('123456789', 'initial', [self._make_entry(cat='OLD')])
        db.save_scenario_data('123456789', 'initial', [self._make_entry(cat='NEW')])
        rows = db.fetch_entries('123456789', 'initial')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][3], 'NEW')

    def test_different_scenarios_independent(self):
        db.save_scenario_data('123456789', 'initial', [self._make_entry(cat='INIT')])
        entry_fut = ('123456789', 'future', 'FUT', 'DESC1', 100.0, 5.0,
                     'Συμβατικά', 0, 0, '', 500.0, 500.0, 500.0, 0, 0, 0)
        db.save_scenario_data('123456789', 'future', [entry_fut])
        initial = db.fetch_entries('123456789', 'initial')
        future = db.fetch_entries('123456789', 'future')
        self.assertEqual(len(initial), 1)
        self.assertEqual(len(future), 1)
        self.assertEqual(initial[0][3], 'INIT')
        self.assertEqual(future[0][3], 'FUT')

    def test_multiple_entries(self):
        entries = [self._make_entry(cat='C1'), self._make_entry(cat='C2')]
        db.save_scenario_data('123456789', 'initial', entries)
        rows = db.fetch_entries('123456789', 'initial')
        self.assertEqual(len(rows), 2)

    def test_fetch_empty_entries(self):
        rows = db.fetch_entries('123456789', 'initial')
        self.assertEqual(len(rows), 0)

    def test_empty_strings_saved_as_null_not_text(self):
        """Regression: empty strings στις numeric στήλες πρέπει να γίνονται NULL,
        όχι να αποθηκεύονται ως TEXT ''. Αλλιώς το MAX(REAL, '') επιστρέφει ''
        (TEXT > REAL) και κενώνει τις στήλες ΤΑ στην αρχική για multi-row AFMs.
        """
        row_with_value = ('123456789', 'initial', 'CAT', 'DESC',
                          50.0, 10.0, 'Συμβατικά', 0, 0, '',
                          500.0, 500.0, 500.0, '', '', '')
        row_all_empty = ('123456789', 'initial', '', '',
                         '', '', '', '', '', '',
                         '', '', '', '', '', '')
        db.save_scenario_data('123456789', 'initial', [row_with_value, row_all_empty])

        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        numeric_cols = ['typical_output', 'quantity', 'trees_over_4', 'trees_under_4',
                        'output_per_choice', 'total_output', 'ta_productive',
                        'ta_plant', 'ta_animal', 'ta_bees']
        for col in numeric_cols:
            cur.execute("SELECT COUNT(*) FROM osde_entries WHERE typeof({})='text'".format(col))  # nosec B608 only for testing
            self.assertEqual(cur.fetchone()[0], 0,
                             "Column {} still contains TEXT values".format(col))

        cur.execute("""
            SELECT MAX(total_output) FROM osde_entries
            WHERE producer_afm='123456789' AND scenario_type='initial'
        """)
        self.assertEqual(cur.fetchone()[0], 500.0)
        conn.close()


# ─── Eligibility ─────────────────────────────────────────────────────

class TestEligibility(_TempDBMixin, unittest.TestCase):

    def setUp(self):
        super().setUp()
        db.setup_database()
        db.save_producer_basics('123456789', 'Test', 'User', 'Αττική')

    def test_save_and_fetch_eligibility(self):
        data = (1, 'Ναι', 'Όχι', 'Ναι', 'Ναι', 'Όχι', 'Ναι', 'Όχι', 'Ναι', 15000.0, 'ΕΠΙΛΕΞΙΜΟΣ')
        db.save_eligibility_data('123456789', data)
        result = db.fetch_eligibility('123456789')
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 1)                    # q1 (INTEGER)
        self.assertEqual(result[2], 'Όχι')                # q3
        self.assertEqual(result[9], 15000.0)              # typical_output_val
        self.assertEqual(result[10], 'ΕΠΙΛΕΞΙΜΟΣ')        # eligibility_result

    def test_fetch_nonexistent_eligibility(self):
        result = db.fetch_eligibility('000000000')
        self.assertIsNone(result)

    def test_save_eligibility_update(self):
        data1 = (1, 'Ναι', 'Ναι', 'Ναι', 'Ναι', 'Ναι', 'Ναι', 'Ναι', 'Ναι', 10000.0, 'ΕΠΙΛΕΞΙΜΟΣ')
        data2 = (0, 'Όχι', 'Όχι', 'Όχι', 'Όχι', 'Όχι', 'Όχι', 'Όχι', 'Όχι', 20000.0, 'ΜΗ ΕΠΙΛΕΞΙΜΟΣ')
        db.save_eligibility_data('123456789', data1)
        db.save_eligibility_data('123456789', data2)
        result = db.fetch_eligibility('123456789')
        self.assertEqual(result[0], 0)                    # q1 (INTEGER)
        self.assertEqual(result[9], 20000.0)
        self.assertEqual(result[10], 'ΜΗ ΕΠΙΛΕΞΙΜΟΣ')    # eligibility_result


# ─── Moria Data ──────────────────────────────────────────────────────

class TestMoriaData(_TempDBMixin, unittest.TestCase):

    def setUp(self):
        super().setUp()
        db.setup_database()
        db.save_producer_basics('123456789', 'Test', 'User', 'Αττική')

    def _make_moria_data(self, moria_val=55.0, budget=100000.0, epileximos='ΕΠΙΛΕΞΙΜΟΣ'):
        return (
            'Ναι', '60.00%',             # q1_1, q1_2
            20000.0, 18000.0,             # q2_1, q2_2
            30000.0, 'Ναι', 'Όχι', 'Ναι', # q3_1_1..q3_1_4
            'Νέος Αγρότης 2018 ή 2021',  # q3_2
            'Κανένα από τα παραπάνω',     # q3_3
            'ΑΣ', 'Ναι',                 # q3_4, q3_5
            50000.0, 10000.0,             # q4_1, q5_1
            'Ναι', 'Όχι',               # q6_1, q7_1
            budget, moria_val,            # budget_val, moria_val
            epileximos                    # moria_epileximos
        )

    def test_save_and_fetch_moria(self):
        data = self._make_moria_data()
        db.save_moria_data('123456789', data)
        result = db.fetch_moria('123456789')
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'Ναι')                # q1_1
        self.assertEqual(result[16], 100000.0)            # budget_val
        self.assertEqual(result[17], 55.0)                # moria_val
        self.assertEqual(result[18], 'ΕΠΙΛΕΞΙΜΟΣ')        # moria_epileximos

    def test_fetch_nonexistent_moria(self):
        result = db.fetch_moria('000000000')
        self.assertIsNone(result)

    def test_save_moria_update(self):
        data1 = self._make_moria_data(moria_val=40.0, epileximos='ΜΗ ΕΠΙΛΕΞΙΜΟΣ')
        data2 = self._make_moria_data(moria_val=70.0, epileximos='ΕΠΙΛΕΞΙΜΟΣ')
        db.save_moria_data('123456789', data1)
        db.save_moria_data('123456789', data2)
        result = db.fetch_moria('123456789')
        self.assertEqual(result[17], 70.0)
        self.assertEqual(result[18], 'ΕΠΙΛΕΞΙΜΟΣ')


# ─── Batch Import ────────────────────────────────────────────────────

class TestBatchImport(_TempDBMixin, unittest.TestCase):

    def setUp(self):
        super().setUp()
        db.setup_database()

    def test_import_new_producers(self):
        data = [
            {
                'afm': '111111111',
                'name': 'A',
                'surname': 'A',
                'region': 'Αττική',
                'rows': [
                    {'category_osde': 'CAT', 'description': 'DESC',
                     'typical_output': '100', 'quantity': '5',
                     'certification': 'Συμβατικά', 'trees_over_4': '',
                     'trees_under_4': '', 'vine_over_3': '',
                     'output_per_choice': '500', 'total_output': '500',
                     'ta_productive': '500', 'ta_plant': '500',
                     'ta_animal': '', 'ta_bees': ''}
                ]
            }
        ]
        result = db.import_producers_batch_transaction(data)
        self.assertEqual(result['total_success'], 1)
        self.assertEqual(result['total_failed'], 0)

        producer = db.fetch_producer('111111111')
        self.assertIsNotNone(producer)
        entries = db.fetch_entries('111111111', 'initial')
        self.assertEqual(len(entries), 1)

    def test_import_replace_mode(self):
        """Replace should delete old entries and insert new ones."""
        db.save_producer_basics('111111111', 'A', 'A', 'Αττική')
        db.save_scenario_data('111111111', 'initial', [
            ('111111111', 'initial', 'OLD', 'OLD', 100, 1, '', 0, 0, '', 100, 100, 100, 0, 0, 0)
        ])

        data = [
            {
                'afm': '111111111',
                '_replace': True,
                'name': 'A',
                'surname': 'A',
                'rows': [
                    {'category_osde': 'NEW', 'description': 'NEW',
                     'typical_output': '200', 'quantity': '3',
                     'certification': '', 'trees_over_4': '',
                     'trees_under_4': '', 'vine_over_3': '',
                     'output_per_choice': '', 'total_output': '',
                     'ta_productive': '', 'ta_plant': '',
                     'ta_animal': '', 'ta_bees': ''}
                ]
            }
        ]
        result = db.import_producers_batch_transaction(data)
        self.assertEqual(result['total_success'], 1)

        entries = db.fetch_entries('111111111', 'initial')
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0][3], 'NEW')

    def test_import_duplicate_afm_fails(self):
        """Importing an AFM that already exists (without _replace) should fail."""
        db.save_producer_basics('111111111', 'A', 'A', 'Αττική')
        data = [
            {
                'afm': '111111111',
                'name': 'B',
                'surname': 'B',
                'rows': []
            }
        ]
        result = db.import_producers_batch_transaction(data)
        self.assertEqual(result['total_failed'], 1)

    def test_import_progress_callback(self):
        calls = []
        data = [
            {'afm': '111111111', 'name': 'A', 'surname': 'A', 'rows': []},
            {'afm': '222222222', 'name': 'B', 'surname': 'B', 'rows': []},
        ]
        db.import_producers_batch_transaction(data, progress_callback=lambda i, t: calls.append((i, t)))
        # Should be called for each item + final
        self.assertTrue(len(calls) >= 2)
        self.assertEqual(calls[-1], (2, 2))

    def test_import_empty_list(self):
        result = db.import_producers_batch_transaction([])
        self.assertEqual(result['total_success'], 0)
        self.assertEqual(result['total_failed'], 0)

    def test_import_result_has_replace_count(self):
        """Το result dict περιλαμβάνει 'replace' με τον αριθμό των _replace."""
        db.save_producer_basics('111111111', 'A', 'A', 'Αττική')
        data = [
            {'afm': '111111111', '_replace': True, 'name': 'A', 'surname': 'A', 'rows': []},
            {'afm': '222222222', 'name': 'B', 'surname': 'B', 'rows': []},
        ]
        result = db.import_producers_batch_transaction(data)
        self.assertIn('replace', result)
        self.assertEqual(result['replace'], 1)
        self.assertEqual(result['total_success'], 2)

    def test_import_replace_clears_moria_eligibility_future(self):
        """_replace καθαρίζει moria.moria_val/moria_epileximos, eligibility.eligibility_result,
        και osde_entries.total_output του future scenario — διατηρεί όμως τις γραμμές."""
        db.save_producer_basics('111111111', 'A', 'A', 'Αττική')
        # Pre-existing μόρια & eligibility & future entry
        db.save_moria_data('111111111', (
            'Ναι', '50.00%', 10000.0, 10000.0,
            5000.0, 'Ναι', 'Όχι', 'Ναι',
            'Νέος Αγρότης 2018 ή 2021', 'Κανένα από τα παραπάνω', 'ΑΣ', 'Ναι',
            5000.0, 5000.0, 'Ναι', 'Όχι',
            50000.0, 60.0, 'ΕΠΙΛΕΞΙΜΟΣ'
        ))
        db.save_eligibility_data('111111111', (
            1, 'Ναι', 'Ναι', 'Ναι', 'Ναι', 'Ναι', 'Ναι', 'Ναι', 'Ναι',
            15000.0, 'ΕΠΙΛΕΞΙΜΟΣ'
        ))
        db.save_scenario_data('111111111', 'future', [
            ('111111111', 'future', 'C', 'D', 100.0, 5.0, '',
             0, 0, '', 500.0, 500.0, 500.0, 0, 0, 0)
        ])

        data = [{
            'afm': '111111111', '_replace': True,
            'name': 'IGNORED', 'surname': 'IGNORED',
            'rows': [{'category_osde': 'NEW', 'description': 'NEW',
                      'typical_output': '', 'quantity': '1',
                      'certification': '', 'trees_over_4': '',
                      'trees_under_4': '', 'vine_over_3': '',
                      'output_per_choice': '', 'total_output': '',
                      'ta_productive': '', 'ta_plant': '',
                      'ta_animal': '', 'ta_bees': ''}]
        }]
        db.import_producers_batch_transaction(data)

        # moria.moria_val & moria_epileximos → NULL
        moria = db.fetch_moria('111111111')
        self.assertIsNone(moria[17])  # moria_val
        self.assertIsNone(moria[18])  # moria_epileximos
        # eligibility.eligibility_result → NULL
        elig = db.fetch_eligibility('111111111')
        self.assertIsNone(elig[10])
        # future osde_entries.total_output → NULL (αλλά η γραμμή υπάρχει)
        future = db.fetch_entries('111111111', 'future')
        self.assertEqual(len(future), 1)
        self.assertIsNone(future[0][12])  # total_output index


# ─── Helper Functions ────────────────────────────────────────────────

class TestHelperFunctions(unittest.TestCase):

    def test_to_float_or_empty_valid(self):
        self.assertEqual(db.to_float_or_empty('123.45'), 123.45)
        self.assertEqual(db.to_float_or_empty('100'), 100.0)
        self.assertEqual(db.to_float_or_empty(42.5), 42.5)

    def test_to_float_or_empty_comma(self):
        self.assertEqual(db.to_float_or_empty('123,45'), 123.45)

    def test_to_float_or_empty_empty(self):
        self.assertIsNone(db.to_float_or_empty(''))
        self.assertIsNone(db.to_float_or_empty(None))
        self.assertIsNone(db.to_float_or_empty('NULL'))

    def test_to_float_or_empty_invalid(self):
        self.assertIsNone(db.to_float_or_empty('abc'))

    def test_to_int_or_empty_valid(self):
        self.assertEqual(db.to_int_or_empty('42'), 42)
        self.assertEqual(db.to_int_or_empty(7), 7)

    def test_to_int_or_empty_empty(self):
        self.assertIsNone(db.to_int_or_empty(''))
        self.assertIsNone(db.to_int_or_empty(None))
        self.assertIsNone(db.to_int_or_empty('NULL'))

    def test_to_int_or_empty_invalid(self):
        self.assertIsNone(db.to_int_or_empty('abc'))
        self.assertIsNone(db.to_int_or_empty('12.5'))


# ─── Delete Producer Entries ─────────────────────────────────────────

class TestDeleteProducerEntries(_TempDBMixin, unittest.TestCase):

    def setUp(self):
        super().setUp()
        db.setup_database()
        db.save_producer_basics('123456789', 'Test', 'User', 'Αττική')

    def test_delete_entries_only_target_scenario(self):
        entry_initial = ('123456789', 'initial', 'C1', 'D1', 100, 5, '', 0, 0, '', 500, 500, 500, 0, 0, 0)
        entry_future = ('123456789', 'future', 'C2', 'D2', 200, 3, '', 0, 0, '', 600, 600, 600, 0, 0, 0)
        db.save_scenario_data('123456789', 'initial', [entry_initial])
        db.save_scenario_data('123456789', 'future', [entry_future])

        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        db.delete_producer_entries(cur, '123456789', scenario_type='initial')
        conn.commit()
        conn.close()

        initial = db.fetch_entries('123456789', 'initial')
        future = db.fetch_entries('123456789', 'future')
        self.assertEqual(len(initial), 0)
        self.assertEqual(len(future), 1)


# ─── Last Modified timestamp ─────────────────────────────────────────

class TestLastModified(_TempDBMixin, unittest.TestCase):

    def setUp(self):
        super().setUp()
        db.setup_database()

    def test_now_iso_format(self):
        """_now_iso returns YYYY-MM-DD HH:MM:SS format."""
        ts = db._now_iso()
        self.assertRegex(ts, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')

    def test_save_producer_basics_sets_timestamp(self):
        """save_producer_basics populates last_modified."""
        with patch('database_manager._now_iso', return_value='2026-04-23 10:00:00'):
            db.save_producer_basics('111111111', 'A', 'B', 'Αττική')
        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        cur.execute("SELECT last_modified FROM producers WHERE afm = ?", ('111111111',))
        ts = cur.fetchone()[0]
        conn.close()
        self.assertEqual(ts, '2026-04-23 10:00:00')

    def test_save_producer_basics_updates_timestamp(self):
        """Re-saving the same AFM refreshes last_modified."""
        with patch('database_manager._now_iso', return_value='2026-01-01 10:00:00'):
            db.save_producer_basics('111111111', 'A', 'B', 'Αττική')
        with patch('database_manager._now_iso', return_value='2026-04-23 15:30:00'):
            db.save_producer_basics('111111111', 'A', 'B', 'Κρήτη')
        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        cur.execute("SELECT last_modified FROM producers WHERE afm = ?", ('111111111',))
        ts = cur.fetchone()[0]
        conn.close()
        self.assertEqual(ts, '2026-04-23 15:30:00')

    def test_fetch_all_producers_returns_9_tuple(self):
        """fetch_all_producers returns 9-tuple with last_modified at index 8."""
        with patch('database_manager._now_iso', return_value='2026-04-23 12:00:00'):
            db.save_producer_basics('111111111', 'A', 'B', 'Αττική')
        results = db.fetch_all_producers()
        self.assertEqual(len(results), 1)
        row = results[0]
        self.assertEqual(len(row), 9)
        self.assertEqual(row[0], '111111111')                 # afm
        self.assertEqual(row[8], '2026-04-23 12:00:00')       # last_modified

    def test_fetch_single_producer_row_returns_9_tuple(self):
        """fetch_single_producer_row returns 9-tuple with last_modified at index 8."""
        with patch('database_manager._now_iso', return_value='2026-04-23 12:00:00'):
            db.save_producer_basics('111111111', 'A', 'B', 'Αττική')
        row = db.fetch_single_producer_row('111111111')
        self.assertIsNotNone(row)
        self.assertEqual(len(row), 9)
        self.assertEqual(row[0], '111111111')
        self.assertEqual(row[8], '2026-04-23 12:00:00')

    def test_fetch_single_producer_row_nonexistent(self):
        self.assertIsNone(db.fetch_single_producer_row('000000000'))

    def _save_elig(self, afm, result):
        data = (1, 'Ναι', 'Ναι', 'Ναι', 'Ναι', 'Ναι', 'Ναι', 'Ναι', 'Ναι', 0.0, result)
        db.save_eligibility_data(afm, data)

    def _save_moria(self, afm, result):
        data = ('Ναι', '0%', 0, 0, 0, 'Ναι', 'Ναι', 'Ναι',
                'Κανένα από τα παραπάνω', 'Κανένα από τα παραπάνω', 'ΑΣ', 'Ναι',
                0, 0, 'Ναι', 'Όχι', 0, 0, result)
        db.save_moria_data(afm, data)

    def test_combined_eligibility_both_eligible(self):
        """eligibility=ΕΠΙΛΕΞΙΜΟΣ + moria=ΕΠΙΛΕΞΙΜΟΣ → combined=ΕΠΙΛΕΞΙΜΟΣ."""
        db.save_producer_basics('111111111', 'A', 'A', 'Αττική')
        self._save_elig('111111111', 'ΕΠΙΛΕΞΙΜΟΣ')
        self._save_moria('111111111', 'ΕΠΙΛΕΞΙΜΟΣ')
        row = db.fetch_single_producer_row('111111111')
        self.assertEqual(row[7], 'ΕΠΙΛΕΞΙΜΟΣ')

    def test_combined_eligibility_one_not_eligible(self):
        """Έστω και 1 'ΜΗ ΕΠΙΛΕΞΙΜΟΣ' → combined=ΜΗ ΕΠΙΛΕΞΙΜΟΣ."""
        db.save_producer_basics('111111111', 'A', 'A', 'Αττική')
        self._save_elig('111111111', 'ΕΠΙΛΕΞΙΜΟΣ')
        self._save_moria('111111111', 'ΜΗ ΕΠΙΛΕΞΙΜΟΣ')
        row = db.fetch_single_producer_row('111111111')
        self.assertEqual(row[7], 'ΜΗ ΕΠΙΛΕΞΙΜΟΣ')

    def test_combined_eligibility_missing_returns_empty(self):
        """Αν λείπει είτε eligibility είτε moria → combined='' (ούτε ΜΗ ούτε ΕΠΙΛΕΞΙΜΟΣ)."""
        db.save_producer_basics('111111111', 'A', 'A', 'Αττική')
        self._save_elig('111111111', 'ΕΠΙΛΕΞΙΜΟΣ')
        # Δεν αποθηκεύουμε moria
        row = db.fetch_single_producer_row('111111111')
        self.assertEqual(row[7], '')

    def test_combined_eligibility_in_fetch_all(self):
        """Το ίδιο combined logic ισχύει και στο fetch_all_producers."""
        db.save_producer_basics('111111111', 'A', 'A', 'Αττική')
        self._save_elig('111111111', 'ΜΗ ΕΠΙΛΕΞΙΜΟΣ')
        self._save_moria('111111111', 'ΕΠΙΛΕΞΙΜΟΣ')
        results = db.fetch_all_producers()
        self.assertEqual(results[0][7], 'ΜΗ ΕΠΙΛΕΞΙΜΟΣ')

    def test_import_new_populates_timestamp(self):
        """New AFM import INSERTs last_modified."""
        data = [{
            'afm': '111111111', 'name': 'A', 'surname': 'A',
            'region': 'Αττική', 'rows': []
        }]
        with patch('database_manager._now_iso', return_value='2026-04-23 09:15:00'):
            db.import_producers_batch_transaction(data)
        row = db.fetch_single_producer_row('111111111')
        self.assertEqual(row[8], '2026-04-23 09:15:00')

    def test_import_replace_updates_only_timestamp(self):
        """_replace updates last_modified but leaves first_name/last_name/region intact."""
        with patch('database_manager._now_iso', return_value='2026-01-01 08:00:00'):
            db.save_producer_basics('111111111', 'OrigName', 'OrigSurname', 'Αττική')

        data = [{
            'afm': '111111111', '_replace': True,
            'name': 'IgnoredName', 'surname': 'IgnoredSurname', 'region': 'Κρήτη',
            'rows': []
        }]
        with patch('database_manager._now_iso', return_value='2026-04-23 14:00:00'):
            db.import_producers_batch_transaction(data)

        producer = db.fetch_producer('111111111')  # (first_name, last_name, region)
        self.assertEqual(producer[0], 'OrigName')
        self.assertEqual(producer[1], 'OrigSurname')
        self.assertEqual(producer[2], 'Αττική')

        row = db.fetch_single_producer_row('111111111')
        self.assertEqual(row[8], '2026-04-23 14:00:00')


if __name__ == '__main__':
    unittest.main()
