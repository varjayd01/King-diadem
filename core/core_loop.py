from core.time_engine import compute_time_to_failure, compute_decision_window


def clamp(v):
    return max(0, min(100, v))


def compute_drift(state):
    return clamp((state["entropy"] * 0.5) + ((100 - state["resource"]) * 0.5))


def update_entropy(state):
    state["entropy"] = clamp(state["entropy"] + state["drift"] * 0.1 - 1.5)
    return state


def update_stability(state):
    state["stability"] = clamp(state["stability"] - state["drift"] * 0.3 + 0.5)
    return state


def stop_the_line(state):
    return state["stability"] < 20 or state["resource"] < 10


def run_core(state):
    state["drift"] = compute_drift(state)
    state = update_entropy(state)
    state = update_stability(state)

    if stop_the_line(state):
        return {"status": "HALT", "state": state}

    ttf = compute_time_to_failure(state)
    window = compute_decision_window(ttf)

    return {
        "status": "RUNNING",
        "state": state,
        "time_to_failure": ttf,
        "decision_window": window
    }
