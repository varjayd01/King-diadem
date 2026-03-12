# KING DIADEM Resource Estimator

def estimate_resources(food, money):

    food_score = {
        "low":20,
        "medium":50,
        "high":80
    }

    food_value = food_score.get(str(food).lower(),40)

    try:
        money_value = max(0,int(money))
    except:
        money_value = 0

    total_resource = food_value + money_value * 0.5

    return {
        "food_score": food_value,
        "money_score": money_value,
        "total_resource": total_resource
    }
