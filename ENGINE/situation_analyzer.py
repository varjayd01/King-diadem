def analyze(food, money, risk):

    result = {}

    # food
    if food.lower() in ["none", "0", "no"]:
        result["food"] = "critical"
    else:
        result["food"] = "available"

    # money
    try:
        m = float(money)
        if m <= 0:
            result["money"] = "critical"
        elif m < 100:
            result["money"] = "low"
        else:
            result["money"] = "stable"
    except:
        result["money"] = "unknown"

    # risk
    if risk:
        result["risk"] = "alert"
    else:
        result["risk"] = "normal"

    return result
