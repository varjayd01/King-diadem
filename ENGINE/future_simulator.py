import random
import numpy as np

from ENGINE.world_model import build_world_state
from ENGINE.learning_engine import load_model


def simulate_step(state, model):

    risk_patterns = model.get("risk_patterns", {})
    food_patterns = model.get("food_patterns", {})

    food_index = state.get("food_index", 50)
    risk_index = state.get("risk_index", 50)

    food_noise = random.uniform(-3, 3)
    risk_noise = random.uniform(-3, 3)

    if str(food_index) in food_patterns:
        food_noise += food_patterns[str(food_index)] * 0.01

    if str(risk_index) in risk_patterns:
        risk_noise += risk_patterns[str(risk_index)] * 0.01

    food_index = max(0, min(100, food_index + food_noise))
    risk_index = max(0, min(100, risk_index + risk_noise))

    next_state = {
        "food_index": food_index,
        "risk_index": risk_index
    }

    return next_state


def simulate_future(steps=30):

    world = build_world_state()
    model = load_model()

    state = {
        "food_index": 50,
        "risk_index": 50
    }

    history = []

    for _ in range(steps):

        state = simulate_step(state, model)

        history.append({
            "food_index": state["food_index"],
            "risk_index": state["risk_index"]
        })

    return history


def collapse_probability(simulations=200):

    collapse_count = 0

    for _ in range(simulations):

        future = simulate_future(30)

        last = future[-1]

        if last["risk_index"] > 80:
            collapse_count += 1

    return collapse_count / simulations


def forecast():

    future = simulate_future(30)

    food_values = [s["food_index"] for s in future]
    risk_values = [s["risk_index"] for s in future]

    return {
        "food_projection": float(np.mean(food_values)),
        "risk_projection": float(np.mean(risk_values)),
        "collapse_probability": collapse_probability()
    }
