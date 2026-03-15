import random


def run_montecarlo(score, runs=100):

    results = []

    for i in range(runs):

        drift = random.uniform(-0.2,0.2)

        outcome = score + drift

        results.append(outcome)

    avg = sum(results) / len(results)

    return {
        "runs": runs,
        "average_score": round(avg,3),
        "min": round(min(results),3),
        "max": round(max(results),3)
    }
