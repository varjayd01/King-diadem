# KING DIADEM Self Learning Engine

import json
import os
import statistics

MEMORY_FILE = "data/decision_history.json"


def load_history():

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):

    os.makedirs("data", exist_ok=True)

    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def record_decision(result):

    history = load_history()

    history.append({
        "survival_score": result["survival_score"],
        "strategy": result["strategy"],
        "location": result["location"]
    })

    save_history(history)


def analyze_patterns():

    history = load_history()

    if len(history) < 5:
        return {"status": "learning"}

    scores = [h["survival_score"] for h in history]

    avg = statistics.mean(scores)

    return {
        "average_survival": avg,
        "decisions": len(history)
    }
