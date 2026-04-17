def clamp(v):
    return max(0, min(100, v))


def analyze_pattern(input_data):
    return {
        "entropy": clamp(float(input_data.get("entropy", 40))),
        "resource": clamp(float(input_data.get("resource", 50))),
        "stability": clamp(float(input_data.get("stability", 60))),
        "drift": 0,
    }
