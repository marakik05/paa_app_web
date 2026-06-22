from flask import Flask, render_template, jsonify, request, send_file
import io
import os
import openpyxl
from database_manager import (
    fetch_producer, setup_database, fetch_all_producers, delete_producer,
    fetch_entries, save_producer_basics, save_scenario_data,
    import_producers_batch_transaction_web,
)
from utils.excel_loader import load_excel_data, resource_path, PERIFERIES
from utils.ta_calculations import calc_row, calc_totals, to_float, to_int
from utils.import_utils import build_canon_dicts, build_region_canon, read_excel_file

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB — guard για oversized import uploads
setup_database()

@app.route('/')
def index():
    return render_template('index.html')

#Main-Window

#combo box περιφερειών
@app.route('/api/regions')
def get_regions():
    return jsonify(PERIFERIES)
#έλεγχος αν υπάρχει παραγωγός με το συγκεκριμένο ΑΦΜ
@app.route('/api/producer/<afm>/exists')
def producer_exists(afm):
    return jsonify({'exists': fetch_producer(afm) is not None})

#κουμπί φόρτωσης
@app.route('/api/producer/<afm>/full')
def get_producer_full(afm):
    producer = fetch_producer(afm)
    if not producer:
        return jsonify({'found': False})
    initial = fetch_entries(afm, 'initial')
    return jsonify({
        'found': True,
        'name': producer[0], 'surname': producer[1], 'region': producer[2],
        'initial_rows': [list(r) for r in initial],
    })

#save κουμπί
@app.route('/api/producer/<afm>/save', methods=['POST'])
def save_producer(afm):
    body = request.get_json()
    save_producer_basics(afm, body['name'], body['surname'], body['region'])

    if body.get('initial_rows') is not None:
        rows = [[afm, 'initial'] + list(r) for r in body['initial_rows']]
        save_scenario_data(afm, 'initial', rows)
  
    return jsonify({'ok': True})

#Section arxiki
#λίστα παραγωγών
@app.route('/api/producers')
def get_producers():
    return jsonify([list(r) for r in fetch_all_producers()])

#διαγραφή παραγωγού
@app.route('/api/producer/<afm>', methods=['DELETE'])
def delete_producer_route(afm):
    ok = delete_producer(afm)
    return jsonify({'ok': ok})

#Section arxiki-ta

TA_MAPPING, TA_VALUE_MAPPING = load_excel_data(resource_path('data/ta.xlsx'))

_CANON_PAIR, _CANON_CAT, _VALID_CATS, _VALID_DESCS = build_canon_dicts(TA_VALUE_MAPPING)
_CANON_REGION = build_region_canon(PERIFERIES)

@app.route('/api/ta/reference')
def ta_reference():
    return jsonify({'mapping': TA_MAPPING})

@app.route('/api/ta/recalculate', methods=['POST'])
def ta_recalculate():
    body = request.get_json()
    region = body.get('region', '')
    rows_calc = [
        calc_row(
            TA_VALUE_MAPPING, region,
            r.get('category', ''), r.get('description', ''),
            to_float(r.get('quantity')), to_int(r.get('trees_over_4')),
            to_int(r.get('trees_under_4')), r.get('vine_over_3', '')
        )
        for r in body.get('rows', [])
    ]
    return jsonify({
        'rows': [{k: r[k] for k in ('typical_output', 'output_per_choice', 'lock_ampeli', 'lock_trees')} for r in rows_calc],
        'totals': calc_totals(rows_calc)
    })
@app.route('/api/import/parse', methods=['POST'])
def import_parse():
    f = request.files.get('file')
    if not f:
        return jsonify({'ok': False, 'error': 'Δεν επιλέχθηκε αρχείο.'})
    try:
        producers, skipped = read_excel_file(
            f.read(), _CANON_PAIR, _CANON_CAT, _VALID_CATS, _VALID_DESCS, _CANON_REGION)
    except ValueError as e:
        return jsonify({'ok': False, 'error': str(e)})

    existing_afms = {r[0] for r in fetch_all_producers()}
    new_data, conflicts = [], []
    for p in producers:
        if p['afm'] in existing_afms:
            conflicts.append(p)
        else:
            new_data.append(p)

    return jsonify({'ok': True, 'new_data': new_data, 'conflicts': conflicts,
                    'skipped': len(skipped)})


@app.route('/api/import/execute', methods=['POST'])
def import_execute():
    body = request.get_json()
    producers = body.get('producers', [])
    decisions = body.get('decisions', {})

    all_data = []
    for p in producers:
        if p.get('_conflict'):
            if decisions.get(p['afm']) == 'skip':
                continue
            p = dict(p, _replace=True)
        all_data.append(p)

    # Calculated fields  — υπολογίζονται εδώ server-side με τις ίδιες pure functions που χρησιμοποιεί το /api/ta/recalculate.
    for p in all_data:
        region = p.get('region', '')
        rows = p.get('rows', [])
        rows_calc = [
            calc_row(
                TA_VALUE_MAPPING, region,
                r.get('category_osde', ''), r.get('description', ''),
                to_float(r.get('quantity')), to_int(r.get('trees_over_4')),
                to_int(r.get('trees_under_4')), r.get('vine_over_3', '')
            )
            for r in rows
        ]
        totals = calc_totals(rows_calc)
        for r, c in zip(rows, rows_calc):
            r['typical_output'] = c['typical_output']
            r['output_per_choice'] = c['output_per_choice']
            r['total_output'] = totals['total_output']
            r['ta_productive'] = totals['ta_productive']
            r['ta_plant'] = totals['ta_plant']
            r['ta_animal'] = totals['ta_animal']
            r['ta_bees'] = totals['ta_bees']

    result = import_producers_batch_transaction_web(all_data)
    return jsonify({'ok': True, **result})


@app.route('/api/producer/<afm>/export', methods=['POST'])
def export_producer(afm):
    body    = request.get_json()
    name    = body.get('name', '')
    surname = body.get('surname', '')
    region  = body.get('region', '')
    rows    = body.get('rows', [])    # 14-element arrays από getTaRows()
    totals  = body.get('totals', {})

    def _f(v):
        try: return float(v) if v not in (None, '') else None
        except: return None

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Τυπική Απόδοση"
    ws.append([
        'ΑΦΜ', 'Όνομα', 'Επώνυμο', 'Περιφέρεια',
        'Κατηγορία ΟΣΔΕ', 'Περιγραφή Είδους/Ποικιλίας/Ζώων',
        'Τυπική Απόδοση', 'Έκταση/Αριθμός ζώων',
        'Βιολογικά\\Ολοκλ/μένη\\ΠΟΠ/ΠΓΕ',
        'Δένδρα >=4 ετών', 'Δένδρα <4 ετών', 'Αμπέλι >3 ετών',
        'ΤΑ ανά επιλογή',
        'Σύνολο ΤΑ', 'ΤΑ Παραγωγικών', 'ΤΑ Φυτικής', 'ΤΑ Ζωικής',
        'ΤΑ Μελίσσια/Μεταξοσκώληκες',
    ])
    # getTaRows() layout: [cat(0),desc(1),typ_out(2),qty(3),cert(4),trees4+(5),trees4-(6),vine(7),out_pc(8),tot(9),prod(10),plant(11),animal(12),bees(13)]
    for idx, r in enumerate(rows):
        row_totals = [
            _f(totals.get('total_ta')),
            _f(totals.get('ta_prod')),
            _f(totals.get('ta_plant')),
            _f(totals.get('ta_animal')),
            _f(totals.get('ta_bees')),
        ] if idx == 0 else [None, None, None, None, None]
        ws.append([
            afm, name, surname, region,
            r[0] or '', r[1] or '',
            _f(r[2]),   # typical_output
            _f(r[3]),   # quantity
            r[4] or '', # certification
            r[5],       # trees_over_4
            r[6],       # trees_under_4
            r[7] or '', # vine_over_3
            _f(r[8]),   # output_per_choice
            *row_totals,
        ])

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return send_file(
        buf,
        as_attachment=True,
        download_name=f'{afm}_ΤΑ.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )


if __name__ == '__main__':
    # debug = os.environ.get('FLASK_DEBUG') == '1'
    # app.run(debug=debug)
    
    app.run(debug=True) #nosec B201