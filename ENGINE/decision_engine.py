def run_decision(input_data: dict):

    try:
        food = str(input_data.get("food", "")).lower()
        money = str(input_data.get("money", "")).lower()
        risk = str(input_data.get("risk", "")).lower()
        location = input_data.get("location", "")

        if "high" in risk:
            return {
                "priority": "SURVIVAL",
                "action": "reduce_risk",
                "tool": "none"
            }

        if "low" in food:
            return {
                "priority": "FOOD",
                "action": "search_food",
                "tool": "open_url",
                "url": "https://maps.google.com"
            }

        if "low" in money:
            return {
                "priority": "ECONOMY",
                "action": "write_log",
                "tool": "write_note",
                "content": "User needs income strategy"
            }

        return {
            "priority": "STABLE",
            "action": f"operate in {location}",
            "tool": "none"
        }

    except Exception as e:
        return {"error": str(e)}
