# KING DIADEM Unified Decision Engine

from core.silent_canon import SILENT_CANON

from GLOBAL_NODE.network_sync import sync_node
from core.memory_store import log_decision, log_world_state

from ENGINE.resource_estimator import estimate
from ENGINE.learning_engine import predict_risk, predict_food
from ENGINE.strategy_planner import plan_strategy
from ENGINE.future_simulator import simulate_future
from ENGINE.world_intelligence import update_world
from ENGINE.world_model import build_world_state
from ENGINE.paticcasamuppada_engine import suffering_infrastructure
from ENGINE.intervention_engine import intervention
from ENGINE.survival_map_engine import build_survival_map
from ENGINE.survival_advisor import survival_advice
from ENGINE.human_state_engine import analyze_human_state


# -------------------------
# RESOURCE EVALUATION
# -------------------------

def evaluate_resources(food, money):

    estimation = estimate(food, money)

    try:
        money_value = float(money)
    except:
        money_value = 0

    food_units = estimation.get("food_units", 0)

    resource_score = min(
        100,
        int(food_units * 10 + money_value * 0.5)
    )

    return resource_score, estimation


# -------------------------
# RISK EVALUATION
# -------------------------

def evaluate_risk(risk):

    risk_map = {
        "low": 20,
        "medium": 50,
        "high": 80,
        "critical": 95
    }

    risk_score = risk_map.get(str(risk).lower(), 40)

    learned_adjustment = predict_risk(risk)

    return min(100, risk_score + learned_adjustment)


# -------------------------
# OPTION GENERATION
# -------------------------

def generate_options(resource_score, risk_score):

    options = []

    if resource_score < 40:
        options.append("search for food or local resources")

    if resource_score >= 40:
        options.append("stabilize resources")

    if risk_score > 70:
        options.append("reduce exposure and move to safer location")

    if risk_score < 50:
        options.append("explore income or cooperation opportunities")

    options.append("preserve human choice")

    return options


# -------------------------
# MAIN DECISION ENGINE
# -------------------------

def decision_engine(location, lat, lng, food, money, risk, text):

    # --------------------------------
    # HUMAN STATE ANALYSIS
    # --------------------------------

    human_state = analyze_human_state(text)

    # --------------------------------
    # RESOURCE ANALYSIS
    # --------------------------------

    resource_score, resource_estimation = evaluate_resources(food, money)

    # --------------------------------
    # RISK ANALYSIS
    # --------------------------------

    risk_score = evaluate_risk(risk)

    # --------------------------------
    # SURVIVAL SCORE
    # --------------------------------

    survival_score = max(
        5,
        min(
            95,
            int(resource_score * 0.7 - risk_score * 0.6 + 40)
        )
    )

    # --------------------------------
    # DECISION OPTIONS
    # --------------------------------

    options = generate_options(resource_score, risk_score)

    # --------------------------------
    # INTERVENTION SYSTEM
    # --------------------------------

    intervention_action = intervention(risk)

    # --------------------------------
    # WORLD STATE
    # --------------------------------

    world = build_world_state()

    sync_node(location, {
        "food": food,
        "risk": risk
    })

    update_world(location, food, risk)

    # --------------------------------
    # FUTURE SIMULATION
    # --------------------------------

    future = simulate_future(world, steps=10)

    # --------------------------------
    # STRATEGY PLANNING
    # --------------------------------

    strategy = plan_strategy()

    # --------------------------------
    # SURVIVAL MAP
    # --------------------------------

    survival_map = build_survival_map(lat, lng)

    # --------------------------------
    # SURVIVAL ADVICE
    # --------------------------------

    advice = survival_advice(
        survival_score,
        resource_score,
        risk_score
    )

    # --------------------------------
    # CAUSAL ANALYSIS
    # --------------------------------

    context = f"location:{location} food:{food} money:{money} risk:{risk}"

    causal_chain = suffering_infrastructure(context)

    # --------------------------------
    # SILENT CANON STATE
    # --------------------------------

    canon_state = SILENT_CANON

    # --------------------------------
    # FINAL RESULT
    # --------------------------------

    result = {

        "location": location,

        "human_state": human_state,

        "resource_estimation": resource_estimation,

        "resource_score": resource_score,

        "risk_score": risk_score,

        "survival_score": survival_score,

        "options": options,

        "intervention": intervention_action,

        "strategy": strategy,

        "world_state": world,

        "future_simulation": future,

        "survival_map": survival_map,

        "survival_advice": advice,

        "causal_chain": causal_chain,

        "canon_state": canon_state
    }

    # --------------------------------
    # LEARNING SYSTEM
    # --------------------------------

    log_decision(result)

    log_world_state(world)

    return result
