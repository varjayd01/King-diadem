# =========================
# 🛡️ KING DIADEM Survival Advisor (Adapter Ready)
# =========================

def survival_advisor(food, money, risk):

    survival_score = 50
    recommended_actions = []

    if food < 2:
        survival_score -= 20
        recommended_actions.append("find_food")

    if money < 100:
        survival_score -= 10
        recommended_actions.append("secure_income")

    if risk > 5:
        survival_score -= 20
        recommended_actions.append("reduce_risk")

    if survival_score >= 60:
        recommended_actions.append("expand_options")
    else:
        recommended_actions.append("stabilize")

    return {
        "survival_score": survival_score,
        "recommended_actions": recommended_actions
    }


# =========================
# 🔥 ADAPTER (สำคัญ)
# =========================
# รับ pattern จาก DecisionEngine

def advise(pattern: dict):
    try:
        resource = float(pattern.get("resource", 50))
        stability = float(pattern.get("stability", 50))
        entropy = float(pattern.get("entropy", 40))

        # 🔁 map เป็น survival input
        food = max(0, int(resource / 25))     # 0-4
        money = int(resource * 10)            # scale
        risk = int(entropy / 10)              # 0-10

        return survival_advisor(food, money, risk)

    except Exception as e:
        return {"error": f"survival_advisor fail: {str(e)}"}
