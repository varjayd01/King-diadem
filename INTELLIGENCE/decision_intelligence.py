from INTELLIGENCE.pattern_engine import analyze_patterns


def intelligence_layer(result):

    patterns = analyze_patterns()

    signal = "normal"

    if patterns.get("pattern_detected"):

        if patterns["pivot_ratio"] > 0.5:

            signal = "market instability"

        elif patterns["defensive_ratio"] > 0.4:

            signal = "risk environment"

    return {

        "system_signal": signal,

        "pattern_analysis": patterns,

        "decision": result
    }
