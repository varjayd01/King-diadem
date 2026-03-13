# KING DIADEM Survival Advisor

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
