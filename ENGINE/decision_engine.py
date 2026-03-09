# KING DIADEM Decision Engine
# Evaluates survival conditions and produces system decisions

import random
from core.silent_canon import SILENT_CANON


def evaluate_resources(food, money):

    food_map = {
        "low": 20,
        "medium": 50,
        "high": 80
    }

    food_score = food_map.get(food.lower(), 40)

    try:
        money_score = max(0, int(money))
    except:
        money_score = 30

    return food_score + money_score * 0.5


def evaluate_risk(risk):

    risk_map = {
        "low": 20,
        "medium": 50,
        "high": 80
    }

    return risk_map.get(risk.lower(), 40)


def generate_options(resource_score, risk_score):

    options = []

    if resource_score < 60:
        options.append("Find local food or community resources")

    if risk_score >= 60:
        options.append("Reduce movement and secure safe location")

    if resource_score >= 60:
        options.append("Stabilize resources and avoid waste")

    options.append("Preserve human choice")

    return options


def decision(location, food, money, risk):

    resource_score = evaluate_resources(food, money)
    risk_score = evaluate_risk(risk)

    survival_score = max(
        5,
        min(
            95,
            int(resource_score * 0.7 - risk_score * 0.6 + 40)
        )
    )

    options = generate_options(resource_score, risk_score)

    canon_action = SILENT_CANON

    result = {
        "location": location,
        "survival_score": survival_score,
        "options": options,
        "canon_state": canon_action
    }

    print("\nDecision Engine Output:", result)

    return result


# wrapper สำหรับระบบ runtime
def decision_engine(location, food, money, risk):

    return decision(location, food, money, risk)

# compatibility function for older modules
def generate_choices(resource_score, risk_score):

    return generate_options(resource_score, risk_score)
