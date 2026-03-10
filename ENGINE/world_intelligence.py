import json
import os

WORLD_FILE = "data/world_history.json"


def load_world():

    if not os.path.exists(WORLD_FILE):
        return []

    with open(WORLD_FILE, "r") as f:
        return json.load(f)


def save_world(world):

    os.makedirs("data", exist_ok=True)

    with open(WORLD_FILE, "w") as f:
        json.dump(world, f, indent=2)


def update_world(location, food_score, risk_score):

    world = load_world()

    world.append({
        "location": location,
        "food_score": food_score,
        "risk_score": risk_score
    })

    save_world(world)


def build_risk_map():

    world = load_world()

    risk_map = {}

    for entry in world:

        loc = entry["location"]
        risk = entry["risk_score"]

        risk_map.setdefault(loc, []).append(risk)

    return {
        loc: sum(v)/len(v)
        for loc,v in risk_map.items()
    }


def build_resource_map():

    world = load_world()

    resource_map = {}

    for entry in world:

        loc = entry["location"]
        food = entry["food_score"]

        resource_map.setdefault(loc, []).append(food)

    return {
        loc: sum(v)/len(v)
        for loc,v in resource_map.items()
    }
