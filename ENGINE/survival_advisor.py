# KING DIADEM Survival Advisor

from ENGINE.survival_map_engine import build_survival_map
from ENGINE.resource_estimator import estimate_resources
from ENGINE.strategy_planner import plan_strategy


def survival_advice(lat, lng, food, money, risk):

    survival_map = build_survival_map(lat, lng)

    resources = estimate_resources(food, money)

    strategy = plan_strategy()

    return {
        "survival_map": survival_map,
        "resources": resources,
        "strategy": strategy
    }
