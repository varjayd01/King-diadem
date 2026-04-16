def run_decision(input_data: dict):

    food = str(input_data.get("food", "")).lower()
    money = str(input_data.get("money", "")).lower()
    risk = str(input_data.get("risk", "")).lower()
    location = input_data.get("location", "")

    if "high" in risk:
        return {
            "priority": "SURVIVAL",
            "action": "reduce_risk",
            "orbit_speed": 3
        }

    if "low" in food:
        return {
            "priority": "FOOD",
            "action": "find_food",
            "orbit_speed": 2
        }

    if "low" in money:
        return {
            "priority": "MONEY",
            "action": "make_money",
            "orbit_speed": 1
        }

    return {
        "priority": "STABLE",
        "action": f"stay in {location}",
        "orbit_speed": 0.5
    }
