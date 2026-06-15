from flask import Flask, render_template, jsonify, request
from utils.excel_loader import PERIFERIES
from database_manager import fetch_producer, setup_database, fetch_all_producers, delete_producer

app = Flask(__name__, template_folder='templates', static_folder='static')
setup_database()

@app.route('/')
def index():
    return render_template('index.html')

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

#λίστα παραγωγών
@app.route('/api/producers')
def get_producers():
    return jsonify([list(r) for r in fetch_all_producers()])

#διαγραφή παραγωγού
@app.route('/api/producer/<afm>', methods=['DELETE'])
def delete_producer_route(afm):
    ok = delete_producer(afm)
    return jsonify({'ok': ok})

if __name__ == '__main__':
    app.run(debug=True)