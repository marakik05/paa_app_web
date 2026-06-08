from flask import Flask, render_template, jsonify
from utils.excel_loader import PERIFERIES
from database_manager import fetch_producer

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/regions')
def get_regions():
    return jsonify(PERIFERIES)

@app.route('/api/producer/<afm>/exists')
def producer_exists(afm):
    return jsonify({'exists': fetch_producer(afm) is not None})

if __name__ == '__main__':
    app.run(debug=True)