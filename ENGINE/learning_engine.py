import json
import os

LOG_FILE = "data/decision_log.json"


def load_logs():

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE,"r") as f:
        return json.load(f)


def learn_patterns():

    logs = load_logs()

    risk_pattern = {}
    food_pattern = {}

    for entry in logs:

        risk = entry["input"].get("risk","unknown")
        food = entry["input"].get("food","unknown")

        risk_pattern[risk] = risk_pattern.get(risk,0) + 1
        food_pattern[food] = food_pattern.get(food,0) + 1

    return {
        "risk_pattern": risk_pattern,
        "food_pattern": food_pattern
    }
