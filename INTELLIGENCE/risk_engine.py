# INTELLIGENCE/risk_engine.py

import json
import os
import time

DATA_PATH = "data"

def load_json(filename, default={}):
    try:
        with open(os.path.join(DATA_PATH, filename), "r") as f:
            return json.load(f)
    except:
        return default

def save_json(filename, data):
    with open(os.path.join(DATA_PATH, filename), "w") as f:
        json.dump(data, f, indent=4)

# ---------------------------
# CORE FORMULA
# Risk = Drift x Exposure / Remaining Choice
# ---------------------------

def calculate_risk(drift, exposure, remaining_choice):
    if remaining_choice <= 0:
        return float("inf")  # collapse state
    return (drift * exposure) / remaining_choice

# ---------------------------
# DATA SOURCES
# ---------------------------

def get_drift():
    logs = load_json("decision_log.json", [])
    if not logs:
        return 1
    return min(len(logs) / 10, 10)  # scale drift

def get_exposure():
    node_trust = load_json("node_trust.json", {})
    if not node_trust:
        return 1
    return sum(node_trust.values()) / max(len(node_trust), 1)

def get_remaining_choice():
    world = load_json("world_history.json", {})
    if "choices" not in world:
        return 5
    return max(world["choices"], 1)

# ---------------------------
# DASHBOARD GENERATOR
# ---------------------------

def generate_dashboard():
    drift = get_drift()
    exposure = get_exposure()
    remaining_choice = get_remaining_choice()

    risk = calculate_risk(drift, exposure, remaining_choice)

    status = "SAFE"
    if risk > 20:
        status = "WARNING"
    if risk > 50:
        status = "DANGER"
    if risk == float("inf"):
        status = "COLLAPSE"

    dashboard = {
        "timestamp": time.time(),
        "drift": drift,
        "exposure": exposure,
        "remaining_choice": remaining_choice,
        "risk": risk,
        "status": status
    }

    return dashboard

# ---------------------------
# MAIN EXECUTION
# ---------------------------

def run_audit():
    dashboard = generate_dashboard()

    logs = load_json("decision_log.json", [])
    logs.append(dashboard)

    save_json("decision_log.json", logs)

    return dashboard


if __name__ == "__main__":
    result = run_audit()
    print("=== DRIFTZERO DASHBOARD ===")
    print(result)
