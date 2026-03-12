# KING DIADEM Resource Estimator

def estimate(food, money):

    estimation = {}

    try:
        money_value = float(money)
        estimation["days_survival"] = money_value / 50
    except:
        estimation["days_survival"] = "unknown"

    food_units = len(food.split())

    estimation["food_units"] = food_units

    return estimation
