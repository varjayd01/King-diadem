import random

# -----------------------------
# World evaluation
# -----------------------------

def evaluate_state(location, food, money, risk):

    score = 0

    if food == "high":
        score += 3
    elif food == "medium":
        score += 2
    else:
        score += 1

    if money > 500:
        score += 3
    elif money > 100:
        score += 2
    else:
        score += 1

    if risk == "low":
        score += 3
    elif risk == "medium":
        score += 2
    else:
        score += 1

    return score


# -----------------------------
# Possible actions
# -----------------------------

def generate_actions():

    return [
        "stay_and_stabilize",
        "resource_sharing",
        "distributed_food_supply",
        "micro_food_production"
    ]


# -----------------------------
# Future simulation
# -----------------------------

def simulate_action(location, food, money, risk, action):

    food_level = food
    money_level = money
    risk_level = risk

    if action == "stay_and_stabilize":
        money_level -= 20

    if action == "resource_sharing":
        food_level = "medium"

    if action == "distributed_food_supply":
        food_level = "high"
        money_level -= 50

    if action == "micro_food_production":
        food_level = "medium"
        money_level -= 10

    score = evaluate_state(location, food_level, money_level, risk_level)

    # random environmental uncertainty
    score += random.uniform(-0.5, 0.5)

    return {
        "action": action,
        "food": food_level,
        "money": money_level,
        "risk": risk_level,
        "score": score
    }


# -----------------------------
# Monte Carlo future tree
# -----------------------------

def run_simulation(location, food, money, risk):

    actions = generate_actions()

    results = []

    for action in actions:

        simulations = []

        for i in range(20):

            outcome = simulate_action(
                location,
                food,
                money,
                risk,
                action
            )

            simulations.append(outcome["score"])

        avg_score = sum(simulations) / len(simulations)

        results.append({
            "action": action,
            "expected_score": avg_score
        })

    best = max(results, key=lambda x: x["expected_score"])

    return {
        "best_action": best["action"],
        "score": best["expected_score"],
        "alternatives": results
  }
