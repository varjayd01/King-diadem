from DATABASE.decision_history import get_recent_decisions


def analyze_patterns():

    history = get_recent_decisions(50)

    if not history:
        return {

            "pattern_detected": False
        }

    success = 0
    pivot = 0
    defensive = 0
    scale = 0

    for item in history:

        decision = item.get("decision", {})

        strategy = decision.get("recommended_strategy")

        if strategy == "scale":
            scale += 1

        elif strategy == "pivot":
            pivot += 1

        elif strategy == "defensive":
            defensive += 1

        else:
            success += 1

    total = len(history)

    return {

        "pattern_detected": True,

        "history_analyzed": total,

        "scale_ratio": scale / total,

        "pivot_ratio": pivot / total,

        "defensive_ratio": defensive / total

    }
