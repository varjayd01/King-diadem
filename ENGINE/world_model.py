import json
import os

NODE_FILE = "data/node_registry.json"


def load_nodes():

    if not os.path.exists(NODE_FILE):
        return {}

    with open(NODE_FILE,"r") as f:
        return json.load(f)


def build_world_state():

    nodes = load_nodes()

    world = {
        "locations": {},
        "total_nodes": len(nodes)
    }

    for location,data in nodes.items():

        world["locations"][location] = {
            "food": data.get("food"),
            "risk": data.get("risk")
        }

    return world
