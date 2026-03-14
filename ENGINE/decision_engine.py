from core.king_diadem_core import king_diadem_decision


def decision_engine(location, lat, lng, food, money, risk):

    return king_diadem_decision(
        location,
        lat,
        lng,
        food,
        money,
        risk
    )
