import json
import os

TRUST_FILE = "data/node_trust.json"

node_trust = {}

def load_trust():

    global node_trust

    if os.path.exists(TRUST_FILE):
        with open(TRUST_FILE,"r") as f:
            node_trust = json.load(f)


def save_trust():

    with open(TRUST_FILE,"w") as f:
        json.dump(node_trust,f)


def get_trust(node_id):

    return node_trust.get(node_id,0.5)


def update_trust(node_id, valid=True):

    score = node_trust.get(node_id,0.5)

    if valid:
        score += 0.05
    else:
        score -= 0.1

    score = max(0.0, min(1.0, score))

    node_trust[node_id] = score

    save_trust()

    return score
