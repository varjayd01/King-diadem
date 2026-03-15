import random


def simulate_future(score):

    simulations = []

    for i in range(20):

        drift = random.uniform(-0.15, 0.15)

        outcome = score + drift

        simulations.append(outcome)

    avg = sum(simulations) / len(simulations)

    if avg > 0.65:
        outlook = "high growth"

    elif avg > 0.45:
        outlook = "stable expansion"

    elif avg > 0.25:
        outlook = "uncertain market"

    else:
        outlook = "high risk environment"

    return {
        "simulated_score": round(avg,3),
        "future_outlook": outlook
    }
