from flask import Flask, request, jsonify, session
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
    """Test page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Calculator API Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 600px; }
            .result { background: #f0f0f0; padding: 20px; margin: 20px 0; border-radius: 5px; font-size: 24px; font-weight: bold; }
            .display { background: #e0e0e0; padding: 15px; margin: 10px 0; border-radius: 5px; font-size: 18px; }
            button { margin: 5px; padding: 15px 25px; cursor: pointer; font-size: 16px; }
            input { margin: 5px; padding: 10px; width: 120px; font-size: 16px; }
            .operation-btn { background-color: #007bff; color: white; }
            .equals-btn { background-color: #28a745; color: white; }
            .clear-btn { background-color: #dc3545; color: white; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Calculator API Test</h1>
            <div class="result" id="result">Result: 0</div>
            <div class="display" id="currentInput">Input: </div>
            
            <input type="number" id="numberInput" placeholder="Enter number" step="any">
            <br>
            <button class="operation-btn" onclick="calculate('add')">+</button>
            <button class="operation-btn" onclick="calculate('subtract')">-</button>
            <button class="operation-btn" onclick="calculate('multiply')">×</button>
            <button class="operation-btn" onclick="calculate('divide')">/</button>
            <button class="equals-btn" onclick="updateResult()">=</button>
            <button class="clear-btn" onclick="reset()">C</button>
            <button onclick="showHistory()">History</button>
            
            <div id="history"></div>
        </div>
        
       <script>
            // Global variables to track state
            let currentInput = '';
            let pendingOperation = null;
            let waitingForNewNumber = false;
            
            // Load current result on page load
            window.onload = async function() {
                await updateResult();
            };
            
            // Update current input display
            function updateInputDisplay() {
                document.getElementById('currentInput').textContent = 
                    currentInput ? `Input: ${currentInput}` : 'Input: ';
            }
            
            // Update result display
            async function updateResult() {
                try {
                    const response = await fetch('/api/result');
                    const data = await response.json();
                    document.getElementById('result').textContent = `Result: ${data.result}`;
                } catch (error) {
                    console.error('Error updating result:', error);
                }
            }
            
            // Handle number input
            document.getElementById('numberInput').addEventListener('input', function(e) {
                currentInput = e.target.value;
                updateInputDisplay();
            });
            
            // Handle Enter key
            document.getElementById('numberInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    updateResult();
                }
            });
            
            // Perform calculation
            async function calculate(operation) {
                const number = document.getElementById('numberInput').value;
                if (!number) {
                    alert('Please enter a number');
                    return;
                }
                
                try {
                    const response = await fetch(`/api/${operation}`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({number: parseFloat(number)})
                    });
                    
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        document.getElementById('result').textContent = `Result: ${data.result}`;
                        
                        // Clear input and prepare for next number
                        document.getElementById('numberInput').value = '';
                        currentInput = '';
                        updateInputDisplay();
                        
                        // Focus back to input
                        document.getElementById('numberInput').focus();
                        
                        console.log(`${operation}: ${number} → ${data.result}`);
                    } else {
                        document.getElementById('result').textContent = `Error: ${data.error}`;
                    }
                } catch (error) {
                    document.getElementById('result').textContent = `Error: ${error.message}`;
                }
            }
            
            // Reset calculator
            async function reset() {
                try {
                    const response = await fetch('/api/reset', {method: 'POST'});
                    const data = await response.json();
                    document.getElementById('result').textContent = `Result: ${data.result}`;
                    document.getElementById('numberInput').value = '';
                    currentInput = '';
                    updateInputDisplay();
                    document.getElementById('numberInput').focus();
                } catch (error) {
                    document.getElementById('result').textContent = `Error: ${error.message}`;
                }
            }
            
            // Show calculation history
            async function showHistory() {
                try {
                    const response = await fetch('/api/history');
                    const data = await response.json();
                    const historyDiv = document.getElementById('history');
                    
                    if (data.history && data.history.length > 0) {
                        historyDiv.innerHTML = '<h3>Calculation History:</h3>' + 
                            data.history.map(h => {
                                const date = new Date(h.date).toLocaleString();
                                return `<p><strong>${date}:</strong> ${h.operation} - ${h.first_number} ${getOperationSymbol(h.operation)} ${h.second_number} = ${h.result}</p>`;
                            }).join('');
                    } else {
                        historyDiv.innerHTML = '<h3>History:</h3><p>No calculations yet</p>';
                    }
                } catch (error) {
                    document.getElementById('history').innerHTML = `<h3>History:</h3><p>Error: ${error.message}</p>`;
                }
            }
            
            // Get operation symbol for display
            function getOperationSymbol(operation) {
                switch(operation) {
                    case 'addition': return '+';
                    case 'subtraction': return '-';
                    case 'multiplication': return '×';
                    case 'division': return '÷';
                    default: return operation;
                }
            }
            
            // Focus on input field on page load
            document.getElementById('numberInput').focus();
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)