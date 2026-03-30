from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_risk(drift, exposure, choice):
    if choice <= 0:
        return float('inf')
    return (drift * exposure) / choice

def evaluate(drift, exposure, choice):
    risk = calculate_risk(drift, exposure, choice)

    if choice <= 1:
        return {"status": "CRITICAL", "action": "STOP", "risk": risk}
    elif risk > 10:
        return {"status": "HIGH RISK", "action": "REDUCE EXPOSURE", "risk": risk}
    elif risk > 5:
        return {"status": "WARNING", "action": "MONITOR", "risk": risk}
    else:
        return {"status": "STABLE", "action": "CONTINUE", "risk": risk}

@app.route('/')
def home():
    return "KING DIADEM RUNNING"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    drift = float(data.get("drift", 0))
    exposure = float(data.get("exposure", 0))
    choice = float(data.get("choice", 1))

    result = evaluate(drift, exposure, choice)
    return jsonify(result)
