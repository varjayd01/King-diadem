import json
import os
import time


HISTORY_FILE = "DATABASE/decision_log.json"


def load_history():

    if not os.path.exists(HISTORY_FILE):

        return []

    try:

        with open(HISTORY_FILE,"r") as f:

            return json.load(f)

    except:

        return []


def save_history(data):

    with open(HISTORY_FILE,"w") as f:

        json.dump(data,f,indent=2)


def save_decision(decision):

    history = load_history()

    record = {

        "timestamp": time.time(),

        "decision": decision
    }

    history.append(record)

    if len(history) > 1000:

        history = history[-1000:]

    save_history(history)


def get_recent_decisions(limit=10):

    history = load_history()

    return history[-limit:]
