from flask import Flask, render_template, jsonify, request

from database_manager import fetch_producer, setup_database, fetch_all_producers, delete_producer
from utils.excel_loader import load_excel_data, resource_path, PERIFERIES
from utils.ta_calculations import calc_row, calc_totals, to_float, to_int

app = Flask(__name__, template_folder='templates', static_folder='static')
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
    from database_manager import fetch_producer, fetch_entries, fetch_eligibility, fetch_moria
    producer = fetch_producer(afm)
    if not producer:
        return jsonify({'found': False})
    initial = fetch_entries(afm, 'initial')
    future  = fetch_entries(afm, 'future')
    elig    = fetch_eligibility(afm)
    moria   = fetch_moria(afm)
    return jsonify({
        'found': True,
        'name': producer[0], 'surname': producer[1], 'region': producer[2],
        'initial_rows': [list(r) for r in initial],
        'future_rows':  [list(r) for r in future],
        'eligibility':  list(elig) if elig else None,
        'moria':        list(moria) if moria else None
    })

#save κουμπί
@app.route('/api/producer/<afm>/save', methods=['POST'])
def save_producer(afm):
    from database_manager import (save_producer_basics, save_eligibility_data,
                                   save_moria_data, save_scenario_data)
    body = request.get_json()
    save_producer_basics(afm, body['name'], body['surname'], body['region'])
    if body.get('eligibility'):
        save_eligibility_data(afm, tuple(body['eligibility']))
    if body.get('moria'):
        save_moria_data(afm, tuple(body['moria']))
    if body.get('initial_rows') is not None:
        save_scenario_data(afm, 'initial', body['initial_rows'])
    if body.get('future_rows') is not None:
        save_scenario_data(afm, 'future', body['future_rows'])
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
if __name__ == '__main__':
    app.run(debug=True)