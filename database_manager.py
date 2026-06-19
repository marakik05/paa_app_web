import sqlite3
import os
import datetime


def _now_iso():
    """Τρέχον timestamp σε ISO format για αποθήκευση στη βάση."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_db_path():
    """Βρίσκει την κατάλληλη διαδρομή για τη βάση δεδομένων στα Windows AppData."""
    # os.getenv('LOCALAPPDATA') -> Επιστρέφει το C:\Users\ΌνομαΧρήστη\AppData\Local
    local_path = os.getenv('LOCALAPPDATA')
    # Ορίζουμε το όνομα του κρυφού φακέλου της εφαρμογής μας
    app_folder = os.path.join(local_path, "OsdeCalculatorApp_web")
    # Δημιουργία του φακέλου αν δεν υπάρχει
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)
    # Επιστρέφουμε την πλήρη διαδρομή του αρχείου .db
    return os.path.join(app_folder, 'osde_app_web.db')
 
# Η σταθερά DB_PATH παίρνει πλέον την τιμή από τη συνάρτηση
DB_PATH = get_db_path()

SCHEMA_VERSION = 0  # baseline — αύξησε όταν προσθέσεις νέο migration


def _column_exists(cursor, table, column):
    cursor.execute("PRAGMA table_info({})".format(table))
    return any(row[1] == column for row in cursor.fetchall())


def _add_column_if_missing(cursor, table, column, col_type):
    if not _column_exists(cursor, table, column):
        cursor.execute("ALTER TABLE {} ADD COLUMN {} {}".format(table, column, col_type))


def _run_migrations(cursor):
    """Εκτελεί όλα τα migration steps ώστε η βάση να φτάσει στο SCHEMA_VERSION.

    Σε fresh DB (current=0, SCHEMA_VERSION=0) δεν τρέχουν actual migration steps,
    αλλά το PRAGMA user_version τίθεται ρητά — defensive για μελλοντικά bumps.
    """
    cursor.execute("PRAGMA user_version")
    current = cursor.fetchone()[0]

    # DB από το μέλλον (π.χ. μετά από rollback σε παλιότερο build) — μη γυρίσουμε πίσω.
    if current > SCHEMA_VERSION:
        return

    try:
        cursor.execute("BEGIN")

        # Version 0: baseline — κανένα migration step δεν εκτελείται ακόμη.
        # Όταν χρειαστεί migration μετά το release, ξεσχολίασε τα παρακάτω
        # και bump το SCHEMA_VERSION:
        #
        # if current < 1:
        #     _add_column_if_missing(cursor, "eligibility", "new_col", "TEXT")
        #
        # if current < 2:
        #     cursor.execute("DROP TABLE IF EXISTS obsolete_table")
        #     cursor.execute("CREATE TABLE ...")

        cursor.execute("PRAGMA user_version = {}".format(SCHEMA_VERSION))
        cursor.execute("COMMIT")

    except Exception:
        cursor.execute("ROLLBACK")
        raise


def setup_database():
    """Αρχική δημιουργία της βάσης και των πινάκων με υποστήριξη Cascade Deletes."""
  
    get_db_path()
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #  UTF-8 encoding (για κάλυψη των windows 7)
    cursor.execute("PRAGMA encoding = 'UTF-8';")
    
    # Ενεργοποίηση Foreign Keys (απαραίτητο για το Cascade)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Πίνακας Παραγωγών (Ο "Γονέας")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producers (
            afm TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            region TEXT,
            last_modified TEXT
        )
    ''')

    # 2. Πίνακας Εγγραφών Πινάκων ΟΣΔΕ (Αρχική & Μελλοντική ΤΑ)
    # Με ON DELETE CASCADE: αν σβηστεί ο παραγωγός, σβήνονται αυτόματα οι σειρές του.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS osde_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producer_afm TEXT,
            scenario_type TEXT,
            category_osde TEXT,
            description TEXT,
            typical_output REAL,
            quantity REAL,
            certification TEXT,
            trees_over_4 INTEGER, 
            trees_under_4 INTEGER, 
            vine_over_3 INTEGER,
            output_per_choice REAL, 
            total_output REAL,
            ta_productive REAL, 
            ta_plant REAL, 
            ta_animal REAL, 
            ta_bees REAL,
            FOREIGN KEY (producer_afm) REFERENCES producers (afm) ON DELETE CASCADE
        )
    ''')

    # # 3. Πίνακας Επιλεξιμότητας
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS eligibility (
    #         producer_afm TEXT PRIMARY KEY,
    #         q1 INTEGER, q2 TEXT, q3 TEXT, q4 TEXT, q5 TEXT, q6 TEXT, q7 TEXT, q8 TEXT, q9 TEXT,
    #         typical_output_val REAL,
    #         eligibility_result TEXT,
    #         FOREIGN KEY (producer_afm) REFERENCES producers (afm) ON DELETE CASCADE
    #     )
    # ''')

    # # 3. Πίνακας Μοριοδότησης
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS moria (
    #         producer_afm TEXT PRIMARY KEY,
    #         q1_1 TEXT, q1_2 TEXT, q2_1 REAL, q2_2 REAL, q3_1_1 REAL, q3_1_2 TEXT, q3_1_3 TEXT, q3_1_4 TEXT, q3_2 TEXT, q3_3 TEXT, q3_4 TEXT, q3_5 TEXT, q4_1 REAL, q5_1 REAL, q6_1 TEXT, q7_1 TEXT,
    #         budget_val REAL,
    #         moria_val REAL,
    #         moria_epileximos TEXT,
    #         FOREIGN KEY (producer_afm) REFERENCES producers (afm) ON DELETE CASCADE
    #     )
    # ''')

    # Indexes για γρήγορα JOINs / lookups
    # (idempotent — CREATE INDEX IF NOT EXISTS)
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_osde_entries_afm_scenario
        ON osde_entries (producer_afm, scenario_type)
    ''')

    _run_migrations(cursor)

    conn.commit()
    conn.close()

# --- ΣΥΝΑΡΤΗΣΕΙΣ ΑΠΟΘΗΚΕΥΣΗΣ (SAVE) ---

def save_producer_basics(afm, fname, lname, region):
    """Αποθηκεύει ή ενημερώνει τα βασικά στοιχεία του παραγωγού + timestamp τελευταίας επεξεργασίας."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT OR REPLACE INTO producers (afm, first_name, last_name, region, last_modified) '
        'VALUES (?, ?, ?, ?, ?)',
        (afm, fname, lname, region, _now_iso())
    )
    conn.commit()
    conn.close()

def save_scenario_data(afm, scenario_type, table_data):
    """Συγχρονίζει τα δεδομένα των πινάκων (Αρχική/Μελλοντική) για ένα ΑΦΜ."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Διαγραφή παλιών εγγραφών για το συγκεκριμένο σενάριο
    cursor.execute('DELETE FROM osde_entries WHERE producer_afm = ? AND scenario_type = ?', (afm, scenario_type))

    # Sanitize: τα κενά strings μετατρέπονται σε NULL για τις REAL/INTEGER στήλες.
    # Αλλιώς το SQLite αποθηκεύει '' ως TEXT σε REAL column, και το MAX(REAL, '')
    # επιστρέφει '' (TEXT > REAL στο type ordering) → κενό στην αρχική.
    cleaned = []
    for r in table_data:
        cleaned.append((
            r[0], r[1], r[2], r[3],
            to_float_or_empty(r[4]),
            to_float_or_empty(r[5]),
            r[6],
            to_int_or_empty(r[7]),
            to_int_or_empty(r[8]),
            r[9],
            to_float_or_empty(r[10]),
            to_float_or_empty(r[11]),
            to_float_or_empty(r[12]),
            to_float_or_empty(r[13]),
            to_float_or_empty(r[14]),
            to_float_or_empty(r[15]),
        ))

    cursor.executemany('''
        INSERT INTO osde_entries (
            producer_afm, scenario_type, category_osde, description, typical_output,
            quantity, certification, trees_over_4, trees_under_4, vine_over_3,
            output_per_choice, total_output, ta_productive, ta_plant, ta_animal, ta_bees
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', cleaned)

    conn.commit()
    conn.close()

# def save_eligibility_data(afm, data_tuple):
#     """Αποθηκεύει τις επιλογές της καρτέλας Επιλεξιμότητα."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("PRAGMA foreign_keys = ON;")
    
#     cursor.execute('''
#         INSERT OR REPLACE INTO eligibility
#         (producer_afm, q1, q2, q3, q4, q5, q6, q7, q8, q9, typical_output_val, eligibility_result)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (afm, *data_tuple))
    
#     conn.commit()
#     conn.close()

# def save_moria_data(afm, data_tuple):
#     """Αποθηκεύει τις επιλογές της καρτέλας Μοριοδότησης."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("PRAGMA foreign_keys = ON;")
    
#     cursor.execute('''
#         INSERT OR REPLACE INTO moria
#         (producer_afm, q1_1, q1_2, q2_1, q2_2, q3_1_1, q3_1_2, q3_1_3, q3_1_4, q3_2, q3_3, q3_4, q3_5, q4_1, q5_1, q6_1, q7_1, budget_val, moria_val, moria_epileximos)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (afm, *data_tuple))
    
#     conn.commit()
#     conn.close()

# --- ΣΥΝΑΡΤΗΣΕΙΣ ΑΝΑΚΤΗΣΗΣ (FETCH) ---

def fetch_producer(afm):
    """Επιστρέφει τα βασικά στοιχεία παραγωγού."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, region FROM producers WHERE afm = ?", (afm,))
    result = cursor.fetchone()
    conn.close()
    return result

def fetch_all_producers():
    """Επιστρέφει όλους τους παραγωγούς από τη βάση με ηλικία, περιφέρεια, αρχική και μελλοντική ΤΑ.

    Χρήση pre-aggregated LEFT JOIN αντί για correlated subqueries: γρήγορο για χιλιάδες εγγραφές
    (απαιτεί το index idx_osde_entries_afm_scenario που δημιουργείται στο setup_database)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            p.afm,
            p.first_name,
            p.last_name,
            NULLIF(p.region, '--Επιλέξτε'),
            oe.initial_ta,
            p.last_modified
        FROM producers p
        LEFT JOIN (
            SELECT
                producer_afm,
                MAX(CASE WHEN scenario_type = 'initial' THEN total_output END) AS initial_ta
            FROM osde_entries
            GROUP BY producer_afm
        ) oe ON oe.producer_afm = p.afm
        ORDER BY p.afm ASC
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def fetch_single_producer_row(afm):
    """Επιστρέφει μία γραμμή με το ίδιο shape της fetch_all_producers για συγκεκριμένο ΑΦΜ."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            p.afm,
            p.first_name,
            p.last_name,
            NULLIF(p.region, '--Επιλέξτε'),
            (SELECT MAX(oe.total_output) FROM osde_entries oe
             WHERE oe.producer_afm = p.afm AND oe.scenario_type = 'initial'),
            p.last_modified
        FROM producers p
        WHERE p.afm = ?
    """, (afm,))
    result = cursor.fetchone()
    conn.close()
    return result


def fetch_entries(afm, scenario_type):
    """Επιστρέφει τις γραμμές του πίνακα ΟΣΔΕ για το UI."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM osde_entries WHERE producer_afm = ? AND scenario_type = ?", (afm, scenario_type))
    results = cursor.fetchall()
    conn.close()
    return results

# def fetch_eligibility(afm):
#     """Επιστρέφει τα δεδομένα επιλεξιμότητας για το UI."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT q1, q2, q3, q4, q5, q6, q7, q8, q9, typical_output_val, eligibility_result FROM eligibility WHERE producer_afm = ?", (afm,))
#     result = cursor.fetchone()
#     conn.close()
#     return result

# def fetch_moria(afm):
#     """Επιστρέφει τα δεδομένα μοριοδότησης για το UI."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT q1_1, q1_2, q2_1, q2_2, q3_1_1, q3_1_2, q3_1_3, q3_1_4, q3_2, q3_3, q3_4, q3_5, q4_1, q5_1, q6_1, q7_1, budget_val, moria_val, moria_epileximos FROM moria WHERE producer_afm = ?", (afm,))
#     result = cursor.fetchone()
#     conn.close()
#     return result

# --- ΣΥΝΑΡΤΗΣΗ ΔΙΑΓΡΑΦΗΣ (DELETE) ---

def delete_producer(afm):
    """Διαγραφή παραγωγού. Το CASCADE αναλαμβάνει τα υπόλοιπα αυτόματα."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("DELETE FROM producers WHERE afm = ?", (afm,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Database Error: {e}")
        return False
    finally:
        conn.close()


# def import_producers_batch_transaction(producers_data, progress_callback=None):
#     """
#     Import με mini-transactions PER AFM.
#     Επιστρέφει detailed results.
    
#     Returns:
#         dict: {
#             'success': [afm1, afm2, ...],
#             'failed': [(afm, error), ...],
#             'replace': int,
#             'total_success': int,
#             'total_failed': int
#         }
#     """
#     conn = sqlite3.connect(DB_PATH)
#     try:
#         cursor = conn.cursor()

#         success_afms = []
#         failed_afms = []
#         replace_afms=[]

#         cursor.execute("PRAGMA foreign_keys = ON;")

#         total = len(producers_data)

#         for idx, data in enumerate(producers_data):
#             # Progress callback
#             if progress_callback:
#                 progress_callback(idx, total)

#             afm = data['afm']

#             try:
#                 #  Mini-transaction PER AFM
#                 cursor.execute("BEGIN TRANSACTION")

#                 name = data.get('name', '')
#                 surname = data.get('surname', '')
#                 region = data.get('region', '--Επιλέξτε')
#                 ts = _now_iso()

#                 # Delete if replace
#                 if data.get('_replace'):



#                     delete_producer_entries(cursor,afm,scenario_type='initial')
#                     cursor.execute(
#                         "UPDATE moria SET moria_val = NULL, moria_epileximos = NULL WHERE producer_afm = ?",
#                         (afm,)
#                     )
#                     cursor.execute(
#                         "UPDATE eligibility SET eligibility_result = NULL WHERE producer_afm = ?",
#                         (afm,)
#                     )
#                     cursor.execute(
#                         "UPDATE osde_entries SET total_output = NULL "
#                         "WHERE producer_afm = ? AND scenario_type = 'future'",
#                         (afm,)
#                     )
#                     cursor.execute(
#                         "UPDATE producers SET last_modified = ? WHERE afm = ?",
#                         (ts, afm)
#                     )
#                     replace_afms.append(afm)

#                 else:
#                     # ← Προσθήκη: Εισαγωγή νέου παραγωγού
#                     cursor.execute('''
#                         INSERT INTO producers (afm, first_name, last_name, region, last_modified)
#                         VALUES (?, ?, ?, ?, ?)
#                     ''', (afm, name, surname, region, ts))

#                 # Insert entries
#                 for entry in data.get('rows', []):
#                     cursor.execute('''
#                         INSERT INTO osde_entries (
#                             producer_afm, scenario_type, category_osde, description,
#                             typical_output, quantity, certification, trees_over_4,
#                             trees_under_4, vine_over_3, output_per_choice, total_output,
#                             ta_productive, ta_plant, ta_animal, ta_bees
#                         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                     ''', (
#                         afm, 'initial',
#                         entry.get('category_osde', ''),
#                         entry.get('description', ''),
#                         to_float_or_empty(entry.get('typical_output', '')),
#                         to_float_or_empty(entry.get('quantity', '')),
#                         entry.get('certification', ''),
#                         to_int_or_empty(entry.get('trees_over_4', '')),
#                         to_int_or_empty(entry.get('trees_under_4', '')),
#                         entry.get('vine_over_3', ''),
#                         to_float_or_empty(entry.get('output_per_choice', '')),
#                         to_float_or_empty(entry.get('total_output', '')),
#                         to_float_or_empty(entry.get('ta_productive', '')),
#                         to_float_or_empty(entry.get('ta_plant', '')),
#                         to_float_or_empty(entry.get('ta_animal', '')),
#                         to_float_or_empty(entry.get('ta_bees', ''))
#                     ))

#                 #  Commit ΜΟΝΟ αυτό το AFM
#                 cursor.execute("COMMIT")
#                 success_afms.append(afm)

#             except Exception as e:
#                 #  Rollback ΜΟΝΟ αυτό το AFM
#                 cursor.execute("ROLLBACK")

#                 # Simplify error message
#                 error_msg = str(e)
#                 if "UNIQUE constraint failed" in error_msg:
#                     error_msg = "Διπλή εγγραφή"
#                 elif "NOT NULL constraint failed" in error_msg:
#                     error_msg = "Κενό απαιτούμενο πεδίο"
#                 elif "FOREIGN KEY constraint failed" in error_msg:
#                     error_msg = "Πρόβλημα αναφοράς"

#                 failed_afms.append((afm, error_msg))

#         # Final progress
#         if progress_callback:
#             progress_callback(total, total)

#         #  Return detailed results
#         return {
#             'success': success_afms,
#             'failed': failed_afms,
#             'replace':len(replace_afms),
#             'total_success': len(success_afms),
#             'total_failed': len(failed_afms)
#         }
#     finally:
#         conn.close()


def to_float_or_empty(value):
    """Μετατροπή σε float ή None (NULL στη βάση) για empty/invalid."""
    if value == '' or value is None or value == 'NULL':
        return None
    try:
        if isinstance(value, str):
            value = value.replace(',', '.')
        return float(value)
    except (ValueError, TypeError):
        return None


def to_int_or_empty(value):
    """Μετατροπή σε int ή None (NULL στη βάση) για empty/invalid."""
    if value == '' or value is None or value == 'NULL':
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def delete_producer_entries(cursor, afm, scenario_type='initial'):
    """Διαγραφή entries για συγκεκριμένο AFM και scenario (χωρίς διαγραφή producer)"""
    try:
        cursor.execute(
            "DELETE FROM osde_entries WHERE producer_afm = ? AND scenario_type = ?",
            (afm, scenario_type)
        )
        return True
    except Exception as e:
        print(f"Database Error: {e}")
        return False


def import_producers_batch_transaction_web(producers_data):
    """Batch import παραγωγών — mini-transaction per ΑΦΜ (χωρίς moria/eligibility)."""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        success, failed = [], []
        for data in producers_data:
            afm = data['afm']
            try:
                cursor.execute("BEGIN TRANSACTION")
                ts = _now_iso()
                if data.get('_replace'):
                    delete_producer_entries(cursor, afm, 'initial')
                    cursor.execute(
                        "UPDATE producers SET first_name=?, last_name=?, region=?, last_modified=? WHERE afm=?",
                        (data.get('name', ''), data.get('surname', ''),
                         data.get('region', '--Επιλέξτε'), ts, afm))
                else:
                    cursor.execute(
                        "INSERT INTO producers (afm,first_name,last_name,region,last_modified)"
                        " VALUES (?,?,?,?,?)",
                        (afm, data.get('name', ''), data.get('surname', ''),
                         data.get('region', '--Επιλέξτε'), ts))
                for entry in data.get('rows', []):
                    cursor.execute('''
                        INSERT INTO osde_entries (
                            producer_afm, scenario_type, category_osde, description,
                            typical_output, quantity, certification, trees_over_4,
                            trees_under_4, vine_over_3, output_per_choice,
                            total_output, ta_productive, ta_plant, ta_animal, ta_bees
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', (
                        afm, 'initial',
                        entry.get('category_osde', ''), entry.get('description', ''),
                        None,
                        to_float_or_empty(entry.get('quantity', '')),
                        entry.get('certification', ''),
                        to_int_or_empty(entry.get('trees_over_4', '')),
                        to_int_or_empty(entry.get('trees_under_4', '')),
                        entry.get('vine_over_3', ''),
                        None, None, None, None, None, None
                    ))
                cursor.execute("COMMIT")
                success.append(afm)
            except Exception as e:
                cursor.execute("ROLLBACK")
                failed.append((afm, str(e)))
        return {'total_success': len(success), 'total_failed': len(failed), 'failed': failed}
    finally:
        conn.close()

        

# def save_osde_entry(afm, scenario_type, category_osde, description, typical_output,
#                     quantity, certification, trees_over_4, trees_under_4, vine_over_3,
#                     output_per_choice, total_output, ta_productive, ta_plant, 
#                     ta_animal, ta_bees):
#     """Αποθήκευση ΜΙΑΣ γραμμής στον πίνακα osde_entries"""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute("PRAGMA foreign_keys = ON;")
        
#         def to_float_or_none(value):
#             """Μετατροπή σε float ή empty string"""
#             if value == '' or value is None or value == 'NULL':
#                 return ''
#             try:
#                 return float(value)
#             except ValueError:
#                 return None
            
#         def to_int_or_none(value):
#             """Μετατροπή σε int ή empty string"""
#             if value == '' or value is None or value=='NULL':
#                 return ''
#             try:
#                 return int(value)
#             except ValueError:
#                 return ''
        
#         cursor.execute('''
#             INSERT INTO osde_entries (
#                 producer_afm, scenario_type, category_osde, description, 
#                 typical_output, quantity, certification, trees_over_4, 
#                 trees_under_4, vine_over_3, output_per_choice, total_output,
#                 ta_productive, ta_plant, ta_animal, ta_bees
#             ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         ''', (
#             afm,
#             scenario_type,
#             category_osde,
#             description,
#             to_float_or_none(typical_output),
#             to_float_or_none(quantity),
#             certification,
#             to_int_or_none(trees_over_4),
#             to_int_or_none(trees_under_4),
#             vine_over_3,  # Text: "Ναι", "Όχι", or ""
#             to_float_or_none(output_per_choice),
#             to_float_or_none(total_output),
#             to_float_or_none(ta_productive),
#             to_float_or_none(ta_plant),
#             to_float_or_none(ta_animal),
#             to_float_or_none(ta_bees)
#         ))
        
#         conn.commit()
#         return True
#     except Exception as e:
#         print(f"Database Error: {e}")
#         return False
#     finally:
#       conn.close()