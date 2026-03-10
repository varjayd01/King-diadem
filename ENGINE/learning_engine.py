import json
import os
import time

LOG_FILE = "data/decision_log.json"
MODEL_FILE = "data/learning_model.json"


def load_logs():

    if not os.path.exists(LOG_FILE):
        return []

    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def load_model():

    if not os.path.exists(MODEL_FILE):
        return {
            "risk_patterns": {},
            "food_patterns": {},
            "decision_success": {},
            "last_trained": 0
        }

    try:
        with open(MODEL_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "risk_patterns": {},
            "food_patterns": {},
            "decision_success": {},
            "last_trained": 0
        }


def save_model(model):

    with open(MODEL_FILE, "w") as f:
        json.dump(model, f, indent=2)


def train_model():

    logs = load_logs()
    model = load_model()

    risk_patterns = {}
    food_patterns = {}
    decision_success = {}

    for entry in logs:

        data = entry.get("input", {})
        result = entry.get("result", {})

        risk = data.get("risk", "unknown")
        food = data.get("food", "unknown")
        decision = result.get("decision", "none")

        risk_patterns[risk] = risk_patterns.get(risk, 0) + 1
        food_patterns[food] = food_patterns.get(food, 0) + 1

        if decision not in decision_success:
            decision_success[decision] = {
                "count": 0
            }

        decision_success[decision]["count"] += 1

    model["risk_patterns"] = risk_patterns
    model["food_patterns"] = food_patterns
    model["decision_success"] = decision_success
    model["last_trained"] = time.time()

    save_model(model)

    return model


def predict_risk(risk_value):

    model = load_model()
    patterns = model["risk_patterns"]

    if risk_value in patterns:
        return patterns[risk_value]

    return 0


def predict_food(food_value):

    model = load_model()
    patterns = model["food_patterns"]

    if food_value in patterns:
        return patterns[food_value]

    return 0
