# ENGINE/pattern_engine.py

def _clamp(value, low=0.0, high=100.0):
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = low
    return max(low, min(high, value))


def analyze_pattern(input_data):
    if not isinstance(input_data, dict):
        input_data = {}

    choices = input_data.get("choices", 1)
    try:
        choices = int(choices)
    except (TypeError, ValueError):
        choices = 1

    confidence = input_data.get("confidence", 0.5)

    warnings = input_data.get("warnings", [])
    if not isinstance(warnings, list):
        warnings = [str(warnings)]

    decision_history = input_data.get("decision_history", [])
    if not isinstance(decision_history, list):
        decision_history = []

    alternatives = input_data.get("alternatives", [])
    if not isinstance(alternatives, list):
        alternatives = []

    return {
        "input": str(input_data.get("input", input_data.get("question", ""))).strip(),
        "entropy": _clamp(input_data.get("entropy", 40)),
        "resource": _clamp(input_data.get("resource", 50)),
        "stability": _clamp(input_data.get("stability", 60)),
        "choices": max(1, choices),
        "confidence": _clamp(confidence, 0.0, 1.0),
        "decision": input_data.get("decision"),
        "previous_decision": input_data.get("previous_decision"),
        "decision_history": decision_history,
        "warnings": warnings,
        "alternatives": alternatives,
        "locked": bool(input_data.get("locked", False)),
    }
