def estimate(food, money):

    estimation = {}

    try:
        m = float(money)
        estimation["days_survival"] = m / 50
    except:
        estimation["days_survival"] = "unknown"

    estimation["food_units"] = len(food.split())

    return estimation
