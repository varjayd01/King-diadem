# core/dependency_cycle.py
"""
Dependency Cycle Engine
Water flow model — systems lose 0.1% choice daily
Like water: always finds the lowest point
"""

DECAY_RATE = 0.9      # 10% drift per cycle
FLOOR = 0.01          # minimum — system never fully dies

def dependent_cycle(state: dict) -> dict:
    """
    Model resource/choice decay like water flowing downhill.
    Each cycle = one day of unaddressed drift.
    """
    if not isinstance(state, dict):
        return {"error": "invalid state", "floor_breached": True}

    next_state = {}
    warnings = []

    for key, value in state.items():
        if isinstance(value, (int, float)):
            decayed = max(FLOOR, value * DECAY_RATE)
            next_state[key] = round(decayed, 3)
            if decayed < 30:
                warnings.append(f"{key} approaching floor: {decayed:.1f}")
        else:
            next_state[key] = value

    floor_breached = any(
        v < 10 for v in next_state.values()
        if isinstance(v, (int, float))
    )

    return {
        "state": next_state,
        "warnings": warnings,
        "floor_breached": floor_breached,
        "drift_rate": "0.1%/day",
        "lyla_signal": "INTERVENE" if floor_breached else "MONITOR",
        "metaphor": "น้ำไหลลงเสมอ — ถ้าไม่เติม waterline จะหาย"
    }

def simulate_days(initial_state: dict, days: int = 30) -> list:
    """Simulate drift over N days"""
    states = [initial_state.copy()]
    current = initial_state.copy()

    for _ in range(days):
        result = dependent_cycle(current)
        current = result["state"]
        states.append({
            "day": _ + 1,
            "state": current,
            "floor_breached": result["floor_breached"]
        })
        if result["floor_breached"]:
            break

    return states
