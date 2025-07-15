from flask import Flask, request, jsonify, session, render_template
from backend.calculator import Calculator
from backend.database import Database
from backend.config import SECRET_KEY
import uuid

app = Flask(__name__)
app.secret_key = SECRET_KEY

calculators = {}

def get_calculator():
    """Get calculator for the current session"""
    if 'calc_id' not in session:
        session['calc_id'] = str(uuid.uuid4())
    
    calc_id = session['calc_id']
    
    if calc_id not in calculators:
        db = Database()
        calculators[calc_id] = Calculator(database=db)
    
    return calculators[calc_id]

@app.route('/api/add', methods=['POST'])
def add():
    """Addition"""
    try:
        data = request.get_json()
        number = float(data['number'])
        calc = get_calculator()
        result = calc.add(number)
        return jsonify({'result': result, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/api/subtract', methods=['POST'])
def subtract():
    """Subtraction"""
    try:
        data = request.get_json()
        number = float(data['number'])
        calc = get_calculator()
        result = calc.subtract(number)
        return jsonify({'result': result, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/api/multiply', methods=['POST'])
def multiply():
    """Multiplication"""
    try:
        data = request.get_json()
        number = float(data['number'])
        calc = get_calculator()
        result = calc.multiply(number)
        return jsonify({'result': result, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/api/divide', methods=['POST'])
def divide():
    """Division"""
    try:
        data = request.get_json()
        number = float(data['number'])
        calc = get_calculator()
        result = calc.divide(number)
        return jsonify({'result': result, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset"""
    try:
        calc = get_calculator()
        result = calc.reset()
        return jsonify({'result': result, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/api/result', methods=['GET'])
def result():
    """Current result"""
    try:
        calc = get_calculator()
        result = calc.result()
        return jsonify({'result': result, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/api/history', methods=['GET'])
def history():
    """History"""
    try:
        limit = request.args.get('limit', 10, type=int)
        calc = get_calculator()
        history_data = calc.history(limit)
        return jsonify({'history': history_data, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/api/session', methods=['GET'])
def session_info():
    """Session info"""
    return jsonify({
        'session_id': session.get('calc_id'),
        'calculator_id': get_calculator().session_id if 'calc_id' in session else None
    })

@app.route('/')
def index():
    """Serve the main calculator interface"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)