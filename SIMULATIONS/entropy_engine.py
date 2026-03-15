import random


def analyze_entropy(system_state):

    entropy = system_state.get("entropy", 50)
    stability = system_state.get("stability", 50)

    simulations = []

    for i in range(20):

        entropy_change = random.randint(-5,5)
        stability_change = random.randint(-5,5)

        new_entropy = max(0, min(100, entropy + entropy_change))
        new_stability = max(0, min(100, stability + stability_change))

        survival_score = new_stability - new_entropy

        simulations.append(survival_score)

    avg = sum(simulations) / len(simulations)

    if avg > 30:
        state = "high stability"

    elif avg > 10:
        state = "balanced"

    elif avg > -10:
        state = "unstable"

    else:
        state = "collapse risk"

    return {
        "entropy_score": round(avg,2),
        "system_state": state
    }
