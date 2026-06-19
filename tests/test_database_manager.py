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
        for t in ('producers', 'osde_entries'):
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
        """Αν user_version > SCHEMA_VERSION (DB από το μέλλον), δεν γυρίζει πίσω."""
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

    def test_fetch_all_producers_returns_6_tuple(self):
        """fetch_all_producers: [afm, first_name, last_name, region, initial_ta, last_modified]."""
        db.save_producer_basics('111111111', 'A', 'B', 'Αττική')
        results = db.fetch_all_producers()
        self.assertEqual(len(results), 1)
        row = results[0]
        self.assertEqual(len(row), 6)
        self.assertEqual(row[0], '111111111')   # afm
        self.assertEqual(row[1], 'A')            # first_name
        self.assertEqual(row[2], 'B')            # last_name
        self.assertEqual(row[3], 'Αττική')       # region
        self.assertIsNone(row[4])                # initial_ta (no entries yet)

    def test_fetch_all_producers_region_default_becomes_null(self):
        """region == '--Επιλέξτε' γίνεται NULL μέσω NULLIF στο SELECT."""
        db.save_producer_basics('111111111', 'A', 'B', '--Επιλέξτε')
        row = db.fetch_all_producers()[0]
        self.assertIsNone(row[3])

    def test_fetch_all_producers_initial_ta_from_entries(self):
        db.save_producer_basics('111111111', 'A', 'B', 'Αττική')
        db.save_scenario_data('111111111', 'initial', [
            ('111111111', 'initial', 'CAT', 'DESC', 100.0, 5.0,
             'Συμβατικά', 0, 0, '', 500.0, 500.0, 500.0, 0, 0, 0)
        ])
        row = db.fetch_all_producers()[0]
        self.assertEqual(row[4], 500.0)


# ─── Single Producer Row ─────────────────────────────────────────────

class TestFetchSingleProducerRow(_TempDBMixin, unittest.TestCase):

    def setUp(self):
        super().setUp()
        db.setup_database()

    def test_returns_6_tuple_same_shape_as_fetch_all(self):
        db.save_producer_basics('123456789', 'A', 'B', 'Αττική')
        row = db.fetch_single_producer_row('123456789')
        self.assertIsNotNone(row)
        self.assertEqual(len(row), 6)
        self.assertEqual(row[0], '123456789')

    def test_nonexistent_returns_none(self):
        self.assertIsNone(db.fetch_single_producer_row('000000000'))

    def test_matches_fetch_all_producers_row(self):
        db.save_producer_basics('123456789', 'A', 'B', 'Αττική')
        db.save_scenario_data('123456789', 'initial', [
            ('123456789', 'initial', 'CAT', 'DESC', 100.0, 5.0,
             'Συμβατικά', 0, 0, '', 500.0, 500.0, 500.0, 0, 0, 0)
        ])
        single = db.fetch_single_producer_row('123456789')
        all_row = db.fetch_all_producers()[0]
        self.assertEqual(single, all_row)


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


# ─── Batch Import (web) ──────────────────────────────────────────────

class TestBatchImportWeb(_TempDBMixin, unittest.TestCase):

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
                     'quantity': '5', 'certification': 'Συμβατικά',
                     'trees_over_4': '', 'trees_under_4': '', 'vine_over_3': ''}
                ]
            }
        ]
        result = db.import_producers_batch_transaction_web(data)
        self.assertEqual(result['total_success'], 1)
        self.assertEqual(result['total_failed'], 0)

        producer = db.fetch_producer('111111111')
        self.assertIsNotNone(producer)
        self.assertEqual(producer[2], 'Αττική')
        entries = db.fetch_entries('111111111', 'initial')
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0][3], 'CAT')

    def test_import_replace_mode_deletes_old_entries(self):
        """_replace=True διαγράφει τις παλιές initial entries πριν εισάγει τις νέες."""
        db.save_producer_basics('111111111', 'A', 'A', 'Αττική')
        db.save_scenario_data('111111111', 'initial', [
            ('111111111', 'initial', 'OLD', 'OLD', 100, 1, '', 0, 0, '', 100, 100, 100, 0, 0, 0)
        ])

        data = [
            {
                'afm': '111111111',
                '_replace': True,
                'name': 'A', 'surname': 'A', 'region': 'Κρήτη',
                'rows': [
                    {'category_osde': 'NEW', 'description': 'NEW',
                     'quantity': '3', 'certification': '',
                     'trees_over_4': '', 'trees_under_4': '', 'vine_over_3': ''}
                ]
            }
        ]
        result = db.import_producers_batch_transaction_web(data)
        self.assertEqual(result['total_success'], 1)

        entries = db.fetch_entries('111111111', 'initial')
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0][3], 'NEW')
        producer = db.fetch_producer('111111111')
        self.assertEqual(producer[2], 'Κρήτη')

    def test_import_duplicate_afm_without_replace_fails(self):
        """INSERT χωρίς _replace σε ήδη υπάρχον ΑΦΜ → UNIQUE constraint, καταγράφεται ως failed."""
        db.save_producer_basics('111111111', 'A', 'A', 'Αττική')
        data = [{'afm': '111111111', 'name': 'B', 'surname': 'B', 'rows': []}]
        result = db.import_producers_batch_transaction_web(data)
        self.assertEqual(result['total_failed'], 1)
        self.assertEqual(result['total_success'], 0)

    def test_import_empty_list(self):
        result = db.import_producers_batch_transaction_web([])
        self.assertEqual(result['total_success'], 0)
        self.assertEqual(result['total_failed'], 0)

    def test_import_calculated_fields_are_not_trusted(self):
        """Το typical_output/output_per_choice/κλπ δεν περνάνε από το import — αποθηκεύονται NULL."""
        data = [{
            'afm': '111111111', 'name': 'A', 'surname': 'A', 'region': 'Αττική',
            'rows': [{'category_osde': 'CAT', 'description': 'DESC', 'quantity': '5',
                      'certification': '', 'trees_over_4': '', 'trees_under_4': '', 'vine_over_3': ''}]
        }]
        db.import_producers_batch_transaction_web(data)
        entries = db.fetch_entries('111111111', 'initial')
        # entry layout: [..., typical_output(5), quantity(6), ..., output_per_choice(11), total_output(12), ...]
        self.assertIsNone(entries[0][5])    # typical_output
        self.assertIsNone(entries[0][11])   # output_per_choice
        self.assertIsNone(entries[0][12])   # total_output


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
        entry_other = ('123456789', 'other', 'C2', 'D2', 200, 3, '', 0, 0, '', 600, 600, 600, 0, 0, 0)
        db.save_scenario_data('123456789', 'initial', [entry_initial])
        db.save_scenario_data('123456789', 'other', [entry_other])

        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        db.delete_producer_entries(cur, '123456789', scenario_type='initial')
        conn.commit()
        conn.close()

        initial = db.fetch_entries('123456789', 'initial')
        other = db.fetch_entries('123456789', 'other')
        self.assertEqual(len(initial), 0)
        self.assertEqual(len(other), 1)

    def test_delete_entries_default_scenario_type(self):
        """Default scenario_type='initial' όταν δεν περάσει ρητά."""
        entry_initial = ('123456789', 'initial', 'C1', 'D1', 100, 5, '', 0, 0, '', 500, 500, 500, 0, 0, 0)
        db.save_scenario_data('123456789', 'initial', [entry_initial])

        conn = sqlite3.connect(self._tmp_db)
        cur = conn.cursor()
        db.delete_producer_entries(cur, '123456789')
        conn.commit()
        conn.close()

        self.assertEqual(len(db.fetch_entries('123456789', 'initial')), 0)


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

    def test_fetch_all_producers_last_modified_at_index_5(self):
        with patch('database_manager._now_iso', return_value='2026-04-23 12:00:00'):
            db.save_producer_basics('111111111', 'A', 'B', 'Αττική')
        results = db.fetch_all_producers()
        self.assertEqual(len(results), 1)
        row = results[0]
        self.assertEqual(row[0], '111111111')                 # afm
        self.assertEqual(row[5], '2026-04-23 12:00:00')       # last_modified

    def test_fetch_single_producer_row_last_modified_at_index_5(self):
        with patch('database_manager._now_iso', return_value='2026-04-23 12:00:00'):
            db.save_producer_basics('111111111', 'A', 'B', 'Αττική')
        row = db.fetch_single_producer_row('111111111')
        self.assertIsNotNone(row)
        self.assertEqual(row[0], '111111111')
        self.assertEqual(row[5], '2026-04-23 12:00:00')

    def test_import_new_populates_timestamp(self):
        """New AFM import INSERTs last_modified."""
        data = [{
            'afm': '111111111', 'name': 'A', 'surname': 'A',
            'region': 'Αττική', 'rows': []
        }]
        with patch('database_manager._now_iso', return_value='2026-04-23 09:15:00'):
            db.import_producers_batch_transaction_web(data)
        row = db.fetch_single_producer_row('111111111')
        self.assertEqual(row[5], '2026-04-23 09:15:00')

    def test_import_replace_updates_only_timestamp_and_basics(self):
        """_replace ενημερώνει name/surname/region/last_modified (web version, σε αντίθεση
        με το desktop replace που άφηνε τα βασικά στοιχεία αμετάβλητα)."""
        with patch('database_manager._now_iso', return_value='2026-01-01 08:00:00'):
            db.save_producer_basics('111111111', 'OrigName', 'OrigSurname', 'Αττική')

        data = [{
            'afm': '111111111', '_replace': True,
            'name': 'NewName', 'surname': 'NewSurname', 'region': 'Κρήτη',
            'rows': []
        }]
        with patch('database_manager._now_iso', return_value='2026-04-23 14:00:00'):
            db.import_producers_batch_transaction_web(data)

        producer = db.fetch_producer('111111111')  # (first_name, last_name, region)
        self.assertEqual(producer[0], 'NewName')
        self.assertEqual(producer[1], 'NewSurname')
        self.assertEqual(producer[2], 'Κρήτη')

        row = db.fetch_single_producer_row('111111111')
        self.assertEqual(row[5], '2026-04-23 14:00:00')


if __name__ == '__main__':
    unittest.main()
