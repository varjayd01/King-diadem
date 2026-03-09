# KING DIADEM Decision Engine
# Evaluates survival conditions and produces system decisions

from ENGINE.kernel_runtime import run_kernel
from GLOBAL_NODE.network_sync import sync_node


# -------------------------
# RESOURCE EVALUATION
# -------------------------

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

    resource_score = food_score + (money_score * 0.5)

    return resource_score, food_score


# -------------------------
# RISK EVALUATION
# -------------------------

def evaluate_risk(risk):

    risk_map = {
        "low": 20,
        "medium": 50,
        "high": 80
    }

    risk_score = risk_map.get(str(risk).lower(), 40)

    return risk_score


# -------------------------
# OPTION GENERATION
# -------------------------

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


# -------------------------
# MAIN DECISION ENGINE
# -------------------------

def decision(location, food, money, risk):

    # Resource calculation
    resource_score, food_score = evaluate_resources(food, money)

    # Risk calculation
    risk_score = evaluate_risk(risk)

    # Survival score formula
    survival_score = max(
        5,
        min(
            95,
            int(resource_score * 0.7 - risk_score * 0.6 + 40)
        )
    )

    # Generate action options
    options = generate_options(resource_score, risk_score)

    # -------------------------
    # Kernel Runtime
    # -------------------------

    system_state = {
        "stability": survival_score,
        "entropy": risk_score,
        "choices": len(options),
        "resources": resource_score
    }

    kernel_report = run_kernel(system_state)

    # -------------------------
    # Global Node Sync
    # -------------------------

    world_state = sync_node(location, {
        "food_score": food_score,
        "risk_score": risk_score
    })

    # -------------------------
    # Final Result
    # -------------------------

    result = {
        "location": location,
        "survival_score": survival_score,
        "options": options,
        "kernel": kernel_report,
        "world_state": world_state
    }

    return result


# -------------------------
# WRAPPER FOR API
# -------------------------

def decision_engine(location, food, money, risk):

    return decision(location, food, money, risk)
