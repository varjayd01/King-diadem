# KING DIADEM Decision Engine
# Reality Optimization Core

from core.silent_canon import SILENT_CANON
from GLOBAL_NODE.network_sync import sync_node
from core.memory_store import log_decision, log_world_state

from ENGINE.future_simulator import simulate_future
from ENGINE.strategy_planner import plan_strategy


# -----------------------------
# RESOURCE EVALUATION
# -----------------------------

def evaluate_resources(food, money):

    food_map = {
        "low": 20,
        "medium": 50,
        "high": 80
    }

    food_score = food_map.get(str(food).lower(), 40)

    try:
        money_score = max(0, int(money))
    except:
        money_score = 30

    resource_score = food_score + money_score * 0.5

    return resource_score, food_score


# -----------------------------
# RISK EVALUATION
# -----------------------------

def evaluate_risk(risk):

    risk_map = {
        "low": 20,
        "medium": 50,
        "high": 80
    }

    return risk_map.get(str(risk).lower(), 40)


# -----------------------------
# OPTION GENERATION
# -----------------------------

def generate_options(resource_score, risk_score):

    options = []

    if resource_score < 60:
        options.append("Find local food or community resources")

    if resource_score >= 60:
        options.append("Stabilize resources and avoid waste")

    if risk_score >= 60:
        options.append("Reduce movement and secure safe location")

    if risk_score < 60:
        options.append("Explore small income opportunities")

    options.append("Preserve human choice")

    return options


# -----------------------------
# MAIN DECISION ENGINE
# -----------------------------

def decision(location, food, money, risk):

    resource_score, food_score = evaluate_resources(food, money)

    risk_score = evaluate_risk(risk)

    survival_score = max(
        5,
        min(
            95,
            int(resource_score * 0.7 - risk_score * 0.6 + 40)
        )
    )

    options = generate_options(resource_score, risk_score)

    # -----------------------------
    # GLOBAL NODE UPDATE
    # -----------------------------

    world = sync_node(location, {
        "food_score": food_score,
        "risk_score": risk_score
    })

    # -----------------------------
    # SILENT CANON STATE
    # -----------------------------

    canon_state = SILENT_CANON()

    # -----------------------------
    # FUTURE SIMULATION
    # -----------------------------

    future = simulate_future(world, steps=10)

    # -----------------------------
    # STRATEGY PLANNER
    # -----------------------------

    strategy = plan_strategy()

    # -----------------------------
    # RESULT
    # -----------------------------

    result = {
        "location": location,
        "survival_score": survival_score,
        "options": options,
        "strategy": strategy,
        "canon_state": canon_state,
        "world_state": world,
        "future_simulation": future
    }

    # -----------------------------
    # MEMORY LOGGING
    # -----------------------------

    log_decision(result)
    log_world_state(world)

    return result


# -----------------------------
# PUBLIC ENGINE
# -----------------------------

def decision_engine(location, food, money, risk):

    return decision(
        location,
        food,
        money,
        risk
    )
