"""
Browser/E2E tests μέσω raw Playwright (sync API) μέσα σε unittest — όχι pytest-playwright,
ώστε να παραμείνει ένα μόνο test runner (`python -m unittest discover`) για όλο το project.

Παραλείπονται αυτόματα (skip, όχι error) αν δεν είναι εγκατεστημένο το πακέτο `playwright`
στο venv ή δεν έχει τρέξει `playwright install chromium` — έτσι το CI (tests.yml), που
εγκαθιστά μόνο requirements.txt, συνεχίζει να τρέχει πράσινο χωρίς αυτό το βαρύ dev-only
dependency.
"""
import os
import io
import sys
import shutil
import random
import tempfile
import threading
import unittest

import openpyxl

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import database_manager as db

try:
    from playwright.sync_api import sync_playwright
    from werkzeug.serving import make_server
    _PLAYWRIGHT_AVAILABLE = True
except ImportError:
    _PLAYWRIGHT_AVAILABLE = False

_tmp_dir = None
_orig_db_path = None
_http_server = None
_http_thread = None
_BASE_URL = None


def setUpModule():
    global _tmp_dir, _orig_db_path, _http_server, _http_thread, _BASE_URL
    if not _PLAYWRIGHT_AVAILABLE:
        return

    _tmp_dir = tempfile.mkdtemp()
    _orig_db_path = db.DB_PATH
    db.DB_PATH = os.path.join(_tmp_dir, 'test.db')
    db.setup_database()  # ρητή δημιουργία πινάκων — δεν αρκεί το module-level setup_database()
                          # του server.py αν το 'server' module είναι ήδη cached από άλλο test file

    import server as server_module
    app = server_module.app
    app.testing = True

    _http_server = make_server('127.0.0.1', 0, app)
    _BASE_URL = f'http://127.0.0.1:{_http_server.server_port}'
    _http_thread = threading.Thread(target=_http_server.serve_forever, daemon=True)
    _http_thread.start()


def tearDownModule():
    if not _PLAYWRIGHT_AVAILABLE:
        return
    _http_server.shutdown()
    db.DB_PATH = _orig_db_path
    shutil.rmtree(_tmp_dir, ignore_errors=True)


@unittest.skipUnless(
    _PLAYWRIGHT_AVAILABLE,
    "playwright δεν είναι εγκατεστημένο — pip install playwright && playwright install chromium"
)
class FrontendE2ETests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._pw = sync_playwright().start()
        cls._browser = cls._pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls._browser.close()
        cls._pw.stop()

    def setUp(self):
        self.page = self._browser.new_page()

    def tearDown(self):
        self.page.close()

    def _load_producer_into_ta(self, name='Τεστ', surname='Παραγωγός', region='Αττική'):
        """Σπείρει παραγωγό απευθείας στη βάση + edit-flow μέσω UI ώστε να ξεκλειδώσει το section ΤΑ."""
        afm = str(random.randint(100000000, 999999999))
        db.save_producer_basics(afm, name, surname, region)
        self.page.goto(_BASE_URL, wait_until='networkidle')
        self.page.click(f'tr[data-afm="{afm}"] .edit-btn')
        self.page.wait_for_selector('[data-page-container="ta"]:not([hidden])')
        return afm

    # ─── Unit-style ─────────────────────────────────────────────────

    def test_pure_js_functions_format_correctly(self):
        """formatTimestamp/formatNumber (section_arxiki.js) μέσω page.evaluate — unit-style test χωρίς Node/Jest."""
        self.page.goto(_BASE_URL, wait_until='networkidle')
        self.assertEqual(
            self.page.evaluate("formatTimestamp('2026-06-19 14:30:45')"),
            '19/06/2026 14:30'
        )
        self.assertEqual(self.page.evaluate("formatNumber(12.3)"), '12.30')
        self.assertEqual(self.page.evaluate("formatNumber(null)"), '')

    def test_num_or_null_and_int_or_null_edge_cases(self):
        """numOrNull/intOrNull (section_ta.js) — το 0 παραμένει 0, μόνο NaN γίνεται null, κόμμα→τελεία."""
        self.page.goto(_BASE_URL, wait_until='networkidle')
        self.assertEqual(self.page.evaluate("numOrNull('3,5')"), 3.5)
        self.assertIsNone(self.page.evaluate("numOrNull('')"))
        self.assertEqual(self.page.evaluate("numOrNull('0')"), 0)
        self.assertEqual(self.page.evaluate("intOrNull('7')"), 7)
        self.assertIsNone(self.page.evaluate("intOrNull('abc')"))

    # ─── E2E: Αρχική (πίνακας παραγωγών) ────────────────────────────

    def test_new_record_flow_saves_and_appears_in_table(self):
        """E2E: κουμπί 'Νέα Εγγραφή' → συμπλήρωση modal → save → εμφάνιση στον πίνακα παραγωγών."""
        afm = str(random.randint(100000000, 999999999))
        self.page.goto(_BASE_URL, wait_until='networkidle')

        self.page.click('#new-record')
        self.page.fill('#modal-afm', afm)
        self.page.fill('#modal-name', 'Δοκιμαστικό')
        self.page.fill('#modal-surname', 'Όνομα')
        self.page.click('#modal-save')

        self.page.wait_for_selector(f'text={afm}')

    def test_edit_flow_loads_producer_into_ta_section(self):
        """E2E: κουμπί 'Επεξεργασία' → ξεκλείδωμα + αυτόματη πλοήγηση στο section ΤΑ + γέμισμα φόρμας."""
        afm = str(random.randint(100000000, 999999999))
        db.save_producer_basics(afm, 'Επεξεργασία', 'Στοιχείων', 'Κρήτη')
        self.page.goto(_BASE_URL, wait_until='networkidle')

        self.page.click(f'tr[data-afm="{afm}"] .edit-btn')
        self.page.wait_for_selector('[data-page-container="ta"]:not([hidden])')

        self.assertEqual(self.page.input_value('#AFM'), afm)
        self.assertEqual(self.page.input_value('#name'), 'Επεξεργασία')
        self.assertEqual(self.page.input_value('#surname'), 'Στοιχείων')
        self.assertEqual(self.page.input_value('#district'), 'Κρήτη')
        nav_class = self.page.get_attribute('.navbar a[data-page="ta"]', 'class') or ''
        self.assertNotIn('nav-disabled', nav_class)

    def test_delete_flow_removes_producer_after_confirm(self):
        """E2E: κουμπί 'Διαγραφή' → styled confirm modal → DELETE → εξαφάνιση από τον πίνακα."""
        afm = str(random.randint(100000000, 999999999))
        db.save_producer_basics(afm, 'Διαγραφή', 'Τεστ', 'Αττική')
        self.page.goto(_BASE_URL, wait_until='networkidle')

        self.page.click(f'tr[data-afm="{afm}"] .delete-btn')
        # σημ.: το #modal-confirm wrapper έχει .modal-overlay (position:fixed) ως μοναδικό
        # παιδί, οπότε ο ίδιος ο wrapper «μαζεύεται» σε ύψος 0 — Playwright θεωρεί visible
        # μόνο στοιχεία με μη-μηδενικό bounding box, γι' αυτό περιμένουμε στο .modal-overlay
        self.page.wait_for_selector('#modal-confirm .modal-overlay', state='visible')
        self.page.click('#modal-confirm-ok')

        self.page.wait_for_selector(f'tr[data-afm="{afm}"]', state='detached')

    def test_live_filter_by_afm_and_surname_uses_cache_not_new_request(self):
        """Client-side φιλτράρισμα (_allProducers cache) — καμία νέα κλήση /api/producers ανά πληκτρολόγηση."""
        afm1 = str(random.randint(100000000, 199999999))
        afm2 = str(random.randint(200000000, 299999999))
        db.save_producer_basics(afm1, 'Πρώτος', 'Αλφα', 'Αττική')
        db.save_producer_basics(afm2, 'Δεύτερος', 'Βήτα', 'Αττική')

        producers_requests = []
        self.page.on('request', lambda req: producers_requests.append(req.url)
                     if '/api/producers' in req.url else None)

        self.page.goto(_BASE_URL, wait_until='networkidle')
        self.assertEqual(len(producers_requests), 1)  # μόνο το αρχικό φόρτωμα

        self.page.fill('#search-afm', afm1)
        self.assertEqual(self.page.locator('#records-table tbody tr').count(), 1)
        self.assertEqual(self.page.get_attribute('#records-table tbody tr', 'data-afm'), afm1)

        self.page.fill('#search-afm', '')
        self.page.fill('#search-surname', 'Βήτα')
        self.assertEqual(self.page.locator('#records-table tbody tr').count(), 1)
        self.assertEqual(self.page.get_attribute('#records-table tbody tr', 'data-afm'), afm2)

        self.assertEqual(len(producers_requests), 1)  # ακόμα καμία επιπλέον κλήση

    # ─── E2E: section ΤΑ ─────────────────────────────────────────────

    def test_lock_ta_section_initial_state(self):
        """Το section ΤΑ ξεκινά κλειδωμένο (disabled fieldset + nav-disabled + άδειος πίνακας)."""
        self.page.goto(_BASE_URL, wait_until='networkidle')
        # σημ.: Playwright's is_disabled() δεν διαβάζει αξιόπιστα disabled σε <fieldset> —
        # ελέγχουμε ένα παιδί input/button μέσα του, που είναι ο πραγματικός μηχανισμός κλειδώματος
        self.assertTrue(self.page.is_disabled('#add-row'))
        nav_class = self.page.get_attribute('.navbar a[data-page="ta"]', 'class') or ''
        self.assertIn('nav-disabled', nav_class)
        self.assertEqual(self.page.locator('#ta-table tbody tr').count(), 0)

    def test_ta_table_add_row_triggers_recalc_request(self):
        """Κουμπί 'Προσθήκη' → νέα γραμμή + αυτόματο POST /api/ta/recalculate."""
        self._load_producer_into_ta()
        with self.page.expect_response(lambda r: '/api/ta/recalculate' in r.url) as resp_info:
            self.page.click('#add-row')
        response = resp_info.value
        self.assertTrue(response.ok)
        data = response.json()
        self.assertEqual(len(data['rows']), 1)
        self.assertIn('totals', data)
        self.assertEqual(self.page.locator('#ta-table tbody tr').count(), 1)

    def test_ta_table_category_change_resets_description_combo(self):
        """Αλλαγή κατηγορίας (col 0) → καταστροφή + ξανά-χτίσιμο της περιγραφής (col 1) σε '--Επιλέξτε'."""
        self._load_producer_into_ta()
        self.page.wait_for_function("() => Object.keys(taMapping).length > 0")
        if self.page.evaluate("Object.keys(taMapping).length") < 2:
            self.skipTest("Απαιτούνται τουλάχιστον 2 κατηγορίες ΟΣΔΕ στο ta.xlsx για αυτό το test")

        self.page.click('#add-row')
        row = self.page.locator('#ta-table tbody tr').first
        cat_cell = row.locator('td[data-col="0"]')
        current_value = cat_cell.locator('.combo-input').input_value()

        cat_cell.locator('.combo-arrow').click()
        dropdown = self.page.locator('.combo-dropdown-portal:visible')
        option_texts = dropdown.locator('.combo-option').all_text_contents()
        target = next(t for t in option_texts if t != current_value)

        with self.page.expect_response(lambda r: '/api/ta/recalculate' in r.url):
            dropdown.get_by_text(target, exact=True).click()

        self.assertEqual(cat_cell.locator('.combo-input').input_value(), target)
        desc_cell = row.locator('td[data-col="1"]')
        self.assertEqual(desc_cell.locator('.combo-input').input_value(), '--Επιλέξτε')

    def test_ta_table_quantity_input_debounced_recalc(self):
        """Πληκτρολόγηση στο 'Έκταση/Αριθμός ζώων' → debounce 350ms → POST /api/ta/recalculate."""
        self._load_producer_into_ta()
        self.page.click('#add-row')
        row = self.page.locator('#ta-table tbody tr').first
        qty_input = row.locator('td[data-col="3"] input')

        with self.page.expect_response(lambda r: '/api/ta/recalculate' in r.url):
            qty_input.fill('12,5')

        self.assertEqual(qty_input.input_value(), '12,5')  # sanitization επιτρέπει ψηφία/κόμμα/τελεία

    def test_ta_table_delete_row_cleans_up_portal_dropdowns(self):
        """destroyCombo() αφαιρεί τα portal dropdowns από το body πριν το tr.remove() — αποτρέπει memory leak."""
        self._load_producer_into_ta()
        self.page.click('#add-row')
        self.page.wait_for_selector('#ta-table tbody tr')
        self.assertEqual(self.page.locator('.combo-dropdown-portal').count(), 2)  # col0 + col1

        self.page.click('.delete-row-btn')
        self.page.wait_for_selector('#ta-table tbody tr', state='detached')

        self.assertEqual(self.page.locator('#ta-table tbody tr').count(), 0)
        self.assertEqual(self.page.locator('.combo-dropdown-portal').count(), 0)

    def test_searchable_combo_filters_and_selects_option(self):
        """Portal combo: άνοιγμα dropdown, live φιλτράρισμα με πληκτρολόγηση, επιλογή με κλικ."""
        self._load_producer_into_ta()
        self.page.click('#add-row')
        row = self.page.locator('#ta-table tbody tr').first
        cat_cell = row.locator('td[data-col="0"]')

        cat_cell.locator('.combo-arrow').click()
        dropdown = self.page.locator('.combo-dropdown-portal:visible')
        self.assertGreater(dropdown.locator('.combo-option').count(), 0)

        # Portal pattern: το dropdown ζει στο <body>, όχι μέσα στο table cell
        self.assertEqual(dropdown.evaluate('el => el.parentElement.tagName'), 'BODY')
        self.assertEqual(dropdown.evaluate('el => getComputedStyle(el).position'), 'absolute')

        first_option_text = dropdown.locator('.combo-option').first.text_content()
        cat_cell.locator('.combo-input').fill(first_option_text)
        filtered_texts = self.page.locator('.combo-dropdown-portal:visible .combo-option').all_text_contents()
        self.assertIn(first_option_text, filtered_texts)

        self.page.locator('.combo-dropdown-portal:visible .combo-option', has_text=first_option_text).first.click()
        self.assertEqual(cat_cell.locator('.combo-input').input_value(), first_option_text)

    def test_readonly_columns_have_green_background(self):
        """Read-only στήλες (Τυπική Απόδοση / ΤΑ ανά επιλογή) έχουν background var(--green-50)."""
        self._load_producer_into_ta()
        self.page.click('#add-row')
        bg = self.page.eval_on_selector('#ta-table td[data-col="2"]', 'el => getComputedStyle(el).backgroundColor')
        self.assertEqual(bg, 'rgb(232, 245, 233)')

    # ─── E2E: Import / unsaved-changes ──────────────────────────────

    def test_import_flow_conflict_replace_renders_text_safely(self):
        """Conflict modal: ΑΦΜ που υπάρχει ήδη → 'Αντικατάσταση Όλων' → εκτέλεση· επιβεβαιώνει το XSS fix
        (το όνομα/επώνυμο αποδίδονται ως textContent, όχι innerHTML — δεν εκτελείται ως markup)."""
        afm = str(random.randint(300000000, 399999999))
        db.save_producer_basics(afm, 'Old', 'Name', 'Αττική')
        payload_name = '<img src=x onerror="window.__xss_fired = true">'

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Τυπική Απόδοση'
        ws.append(["ΑΦΜ", "Όνομα", "Επώνυμο", "Περιφέρεια", "Κατηγορία ΟΣΔΕ", "Περιγραφή",
                   "Έκταση/Αριθμός ζώων", "Βιολογικά", "Δένδρα >=4 ετών", "Δένδρα <4 ετών", "Αμπέλι >3 ετών"])
        ws.append([afm, payload_name, "Surname", "Αττική", "Cat", "Desc", 1, "Συμβατικά", "", "", ""])
        buf = io.BytesIO()
        wb.save(buf)
        wb.close()
        xlsx_bytes = buf.getvalue()

        self.page.goto(_BASE_URL, wait_until='networkidle')
        self.page.set_input_files('#import-file-input', files=[{
            'name': 'import.xlsx',
            'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'buffer': xlsx_bytes,
        }])

        self.page.wait_for_selector('#modal-import-conflict .modal-overlay', state='visible')
        conflict_text = self.page.text_content('#conflict-list')
        self.assertIn(payload_name, conflict_text)
        self.assertIsNone(self.page.evaluate('window.__xss_fired'))  # δεν εκτελέστηκε ως HTML

        with self.page.expect_response(lambda r: '/api/import/execute' in r.url) as resp_info:
            self.page.click('#conflict-replace-all')
            self.page.click('#conflict-confirm')
        self.assertTrue(resp_info.value.ok)

        self.page.wait_for_selector(f'tr[data-afm="{afm}"]')
        updated_name = self.page.text_content(f'tr[data-afm="{afm}"] td:nth-child(2)')
        self.assertEqual(updated_name, payload_name)
        self.assertIsNone(self.page.evaluate('window.__xss_fired'))

    def test_import_button_warns_on_unsaved_changes(self):
        """Κουμπί 'Εισαγωγή' με μη-αποθηκευμένες αλλαγές → styled confirm πριν προχωρήσει· Άκυρο = καμία κλήση."""
        self._load_producer_into_ta()
        self.page.fill('#name', 'Αλλαγή Ονόματος')  # markDirty μέσω input event
        # το κουμπί 'Εισαγωγή' είναι disabled όσο βρισκόμαστε στο section ΤΑ
        # (updatePageButtons) — επιστροφή στην Αρχική για να ξανα-ενεργοποιηθεί
        self.page.click('.navbar a[data-page="arxiki"]')

        parse_requests = []
        self.page.on('request', lambda req: parse_requests.append(req.url)
                     if '/api/import/parse' in req.url else None)

        self.page.click('#import')
        self.page.wait_for_selector('#modal-confirm .modal-overlay', state='visible')
        message = self.page.text_content('#modal-confirm-message')
        self.assertIn('μη αποθηκευμένες αλλαγές', message)

        self.page.click('#modal-confirm-cancel')
        self.page.wait_for_selector('#modal-confirm .modal-overlay', state='hidden')
        self.assertEqual(parse_requests, [])

    # ─── Visual/CSS ──────────────────────────────────────────────────

    def test_mobile_breakpoint_applies_navbar_height(self):
        """Visual/CSS: @media (max-width: 600px) στο responsive.css μειώνει το ύψος του navbar σε 44px."""
        self.page.set_viewport_size({'width': 500, 'height': 800})
        self.page.goto(_BASE_URL, wait_until='networkidle')
        height = self.page.eval_on_selector('.navbar', 'el => getComputedStyle(el).height')
        self.assertEqual(height, '44px')

    def test_tablet_breakpoint_applies_navbar_padding(self):
        """Visual/CSS: @media (max-width: 1024px) στο responsive.css αλλάζει το padding του navbar."""
        self.page.set_viewport_size({'width': 900, 'height': 800})
        self.page.goto(_BASE_URL, wait_until='networkidle')
        padding_left = self.page.eval_on_selector('.navbar', 'el => getComputedStyle(el).paddingLeft')
        padding_top = self.page.eval_on_selector('.navbar', 'el => getComputedStyle(el).paddingTop')
        self.assertEqual(padding_left, '14px')
        self.assertEqual(padding_top, '0px')

    def test_large_screen_breakpoint_widens_main_max_width(self):
        """Visual/CSS: @media (min-width: 1920px) στο responsive.css αυξάνει το max-width του main από 1700px σε 2200px."""
        self.page.set_viewport_size({'width': 1920, 'height': 1080})
        self.page.goto(_BASE_URL, wait_until='networkidle')
        max_width = self.page.eval_on_selector('main', 'el => getComputedStyle(el).maxWidth')
        self.assertEqual(max_width, '2200px')


if __name__ == '__main__':
    unittest.main()
