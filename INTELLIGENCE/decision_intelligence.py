def intelligence_layer(base_decision, patterns, risk, external_ai):
    signal = "normal"

    if patterns.get("pattern_detected"):
        if patterns.get("pivot_ratio", 0) > 0.5:
            signal = "market instability"
        elif patterns.get("defensive_ratio", 0) > 0.4:
            signal = "risk environment"

    return {
        "system_signal": signal,
        "pattern_analysis": patterns,
        "risk": risk,
        "internal_decision": base_decision,
        "external_ai": external_ai
    }
