# CORE DECISION ENGINE (ไม่ผูกกับไฟล์อื่น)

def run_decision(input_data: dict):

    try:
        food = str(input_data.get("food", "")).lower()
        money = str(input_data.get("money", "")).lower()
        risk = str(input_data.get("risk", "")).lower()
        location = input_data.get("location", "")

        # ===== PRIORITY ENGINE =====
        if "high" in risk:
            return {
                "priority": "SURVIVAL",
                "action": "minimize risk, reduce exposure"
            }

        if "low" in food:
            return {
                "priority": "FOOD",
                "action": "secure food immediately"
            }

        if "low" in money:
            return {
                "priority": "ECONOMY",
                "action": "increase income / reduce burn"
            }

        return {
            "priority": "STABLE",
            "action": f"operate normally in {location}"
        }

    except Exception as e:
        return {"error": str(e)}
