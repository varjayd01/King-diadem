def compute_time_to_failure(state):
    risk = (
        state["drift"] * 0.4
        + state["entropy"] * 0.3
        + (100 - state["resource"]) * 0.3
    )
    return max(0, 100 - risk)


def compute_decision_window(ttf):
    return max(0, ttf - 10)
