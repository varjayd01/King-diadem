# KING DIADEM Decision Engine
# Unified Intelligence Core

from core.silent_canon import SILENT_CANON
from GLOBAL_NODE.network_sync import sync_node
from core.memory_store import log_decision, log_world_state

from ENGINE.future_simulator import simulate_future
from ENGINE.strategy_planner import plan_strategy
from ENGINE.self_learning import record_decision

from ENGINE.world_intelligence import update_world
from ENGINE.world_intelligence import build_risk_map
from ENGINE.world_intelligence import build_resource_map

from ENGINE.paticcasamuppada_engine import suffering_infrastructure


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
        "low": 0,
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
# GLOBAL SURVIVAL MAP
# -----------------------------

def build_survival_map():

    risk_map = build_risk_map()
    resource_map = build_resource_map()

    survival_map = {}

    locations = set(risk_map) | set(resource_map)

    for loc in locations:

        risk = risk_map.get(loc, 50)
        resource = resource_map.get(loc, 50)

        survival = max(
            0,
            min(
                100,
                int(resource * 0.7 - risk * 0.6 + 50)
            )
        )

        survival_map[loc] = survival

    return survival_map


# -----------------------------
# MAIN DECISION ENGINE
# -----------------------------

def decision(location, food, money, risk):

    # RESOURCE + RISK
    resource_score, food_score = evaluate_resources(food, money)
    risk_score = evaluate_risk(risk)

    # SURVIVAL SCORE
    survival_score = max(
        5,
        min(
            95,
            int(resource_score * 0.7 - risk_score * 0.6 + 40)
        )
    )

    # OPTIONS
    options = generate_options(resource_score, risk_score)

    # GLOBAL NODE UPDATE
    world = sync_node(location, {
        "food_score": food_score,
        "risk_score": risk_score
    })

    # WORLD INTELLIGENCE UPDATE
    update_world(location, food_score, risk_score)

    # SILENT CANON STATE
    canon_state = SILENT_CANON

    # FUTURE SIMULATION
    future = simulate_future(world, steps=10)

    # STRATEGY PLANNER
    strategy = plan_strategy()

    # GLOBAL SURVIVAL MAP
    survival_map = build_survival_map()

    # -----------------------------
    # CAUSAL ANALYSIS
    # -----------------------------

    context = f"{location} food:{food} money:{money} risk:{risk}"

    causal = suffering_infrastructure(context)

    # RESULT
    result = {
        "location": location,
        "survival_score": survival_score,
        "options": options,
        "strategy": strategy,
        "canon_state": canon_state,
        "world_state": world,
        "future_simulation": future,
        "global_survival_map": survival_map,
        "causal_chain": causal
    }

    # MEMORY + LEARNING
    log_decision(result)
    log_world_state(world)

    record_decision(result)

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
