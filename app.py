from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from ENGINE.decision_engine import KingDiademEngine

app = Flask(__name__, static_folder='static')
CORS(app)

engine = KingDiademEngine()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/decision', methods=['POST'])
def decision():
    data = request.json
    user_input = data.get("input", "")
    mode = data.get("mode", "normal")

    result = engine.run(user_input, mode)

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
