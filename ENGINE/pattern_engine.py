# =========================
# 🧠 PATTERN ENGINE (SAFE + UNIVERSAL)
# =========================

def _clamp(value, low=0.0, high=100.0):
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = low
    return max(low, min(high, value))


def analyze_pattern(input_data):
    if not isinstance(input_data, dict):
        input_data = {}

    # 🔹 input text
    text = str(input_data.get("input", input_data.get("question", ""))).strip()

    # 🔹 basic signals
    entropy = _clamp(input_data.get("entropy", 40))
    resource = _clamp(input_data.get("resource", 50))
    stability = _clamp(input_data.get("stability", 60))

    # 🔹 choices
    try:
        choices = int(input_data.get("choices", 1))
    except:
        choices = 1
    choices = max(1, choices)

    # 🔹 confidence (0-1)
    confidence = input_data.get("confidence", 0.5)
    confidence = _clamp(confidence, 0.0, 1.0)

    # 🔹 lists safe
    def safe_list(x):
        return x if isinstance(x, list) else [str(x)]

    warnings = safe_list(input_data.get("warnings", []))
    history = safe_list(input_data.get("decision_history", []))
    alternatives = safe_list(input_data.get("alternatives", []))

    # =========================
    # 🔥 simple pattern logic
    # =========================

    route = "general"

    if resource < 20 or entropy > 80:
        route = "survival"
    elif stability < 30:
        route = "risk"
    elif confidence < 0.3:
        route = "uncertain"

    return {
        "input": text,
        "route": route,
        "entropy": entropy,
        "resource": resource,
        "stability": stability,
        "choices": choices,
        "confidence": confidence,
        "warnings": warnings,
        "decision_history": history,
        "alternatives": alternatives,
        "locked": bool(input_data.get("locked", False)),
    }


# =========================
# 🔥 BACKWARD COMPAT (กันพัง)
# =========================

def detect_pattern(input_data):
    return analyze_pattern(input_data)
