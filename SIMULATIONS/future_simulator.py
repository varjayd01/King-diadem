# KING DIADEM Future Simulation Engine
# Simulates possible future states and evaluates stability

import random


def simulate_future(system_state, scenarios=5):

    print("\nRunning future simulations...\n")

    results = []

    for i in range(scenarios):

        entropy = system_state.get("entropy", 50)
        stability = system_state.get("stability", 50)

        # simulate random drift
        entropy_change = random.randint(-5, 5)
        stability_change = random.randint(-5, 5)

        new_entropy = max(0, min(100, entropy + entropy_change))
        new_stability = max(0, min(100, stability + stability_change))

        survival_score = new_stability - new_entropy

        scenario = {
            "scenario": i + 1,
            "entropy": new_entropy,
            "stability": new_stability,
            "survival_score": survival_score
        }

        results.append(scenario)

        print("Scenario", i + 1, "→", scenario)

    # choose safest scenario
    best = max(results, key=lambda x: x["survival_score"])

    print("\nBest future path:", best)

    return best
