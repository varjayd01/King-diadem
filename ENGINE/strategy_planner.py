import random

from ENGINE.future_simulator import simulate_future
from ENGINE.world_model import build_world_state


# ---------------------------------
# ACTION SPACE
# ---------------------------------

ACTIONS = [
    "seek_food",
    "secure_location",
    "explore_income",
    "stabilize_resources",
    "stay_low"
]


# ---------------------------------
# ACTION EFFECT MODEL
# ---------------------------------

def apply_action(state, action):

    food = state.get("food_index", 50)
    risk = state.get("risk_index", 50)

    if action == "seek_food":
        food += random.uniform(2, 6)
        risk += random.uniform(0, 2)

    elif action == "secure_location":
        risk -= random.uniform(3, 6)

    elif action == "explore_income":
        food += random.uniform(1, 4)
        risk += random.uniform(1, 3)

    elif action == "stabilize_resources":
        food += random.uniform(0, 2)
        risk -= random.uniform(1, 2)

    elif action == "stay_low":
        risk -= random.uniform(1, 3)

    food = max(0, min(100, food))
    risk = max(0, min(100, risk))

    return {
        "food_index": food,
        "risk_index": risk
    }


# ---------------------------------
# SCORE FUNCTION
# ---------------------------------

def score_state(state):

    food = state.get("food_index", 50)
    risk = state.get("risk_index", 50)

    survival = food * 0.6 + (100 - risk) * 0.4

    return survival


# ---------------------------------
# PLAN STRATEGY
# ---------------------------------

def plan_strategy(simulations=20):

    world = build_world_state()

    base_state = {
        "food_index": 50,
        "risk_index": 50
    }

    best_action = None
    best_score = -999

    for action in ACTIONS:

        total_score = 0

        for _ in range(simulations):

            state = apply_action(base_state, action)

            future = simulate_future(10)

            last = future[-1]

            state["food_index"] = (state["food_index"] + last["food_index"]) / 2
            state["risk_index"] = (state["risk_index"] + last["risk_index"]) / 2

            total_score += score_state(state)

        avg_score = total_score / simulations

        if avg_score > best_score:
            best_score = avg_score
            best_action = action

    return {
        "best_action": best_action,
        "expected_score": best_score
    }
