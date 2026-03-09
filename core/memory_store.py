import json
import os
from datetime import datetime

DATA_DIR = "data"

WORLD_HISTORY = os.path.join(DATA_DIR, "world_history.json")
NODE_REGISTRY = os.path.join(DATA_DIR, "node_registry.json")
DECISION_LOG = os.path.join(DATA_DIR, "decision_log.json")


def load_json(path):

    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_json(path, data):

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def log_decision(decision):

    data = load_json(DECISION_LOG)

    entry = {
        "time": datetime.utcnow().isoformat(),
        "decision": decision
    }

    data.append(entry)

    save_json(DECISION_LOG, data)


def register_node(location, node_data):

    data = load_json(NODE_REGISTRY)

    entry = {
        "time": datetime.utcnow().isoformat(),
        "location": location,
        "data": node_data
    }

    data.append(entry)

    save_json(NODE_REGISTRY, data)


def log_world_state(state):

    data = load_json(WORLD_HISTORY)

    entry = {
        "time": datetime.utcnow().isoformat(),
        "state": state
    }

    data.append(entry)

    save_json(WORLD_HISTORY, data)
