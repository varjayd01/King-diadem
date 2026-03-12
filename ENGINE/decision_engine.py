# KING DIADEM Decision Engine
# Central Orchestrator

from ENGINE.world_intel import analyze_location
from ENGINE.situation_analyzer import analyze_situation
from ENGINE.human_state_engine import evaluate_human_state
from ENGINE.resource_estimator import estimate_resources
from ENGINE.survival_advisor import survival_advisor
from ENGINE.strategy_planner import plan_strategy
from ENGINE.escape_routes import generate_escape_routes
from ENGINE.choice_optimizer import optimize_choice
from ENGINE.collapse_predictor import predict_collapse
from ENGINE.simulation_engine import simulate_future


def decision_engine(location, lat, lng, food, money, risk):

    # 1 WORLD INTELLIGENCE
    world = analyze_location(lat, lng)

    # 2 SITUATION ANALYSIS
    situation = analyze_situation(location, risk)

    # 3 HUMAN STATE
    human = evaluate_human_state(food, money, risk)

    # 4 RESOURCE ESTIMATION
    resources = estimate_resources(food, money)

    # 5 SURVIVAL ANALYSIS
    survival = survival_advisor(food, money, risk)

    # 6 STRATEGY GENERATION
    strategy = plan_strategy(
        situation,
        resources,
        survival
    )

    # 7 ESCAPE PATHS
    routes = generate_escape_routes(
        lat,
        lng,
        world
    )

    # 8 COLLAPSE RISK
    collapse = predict_collapse(
        situation,
        resources,
        risk
    )

    # 9 FUTURE SIMULATION
    future = simulate_future(
        strategy,
        collapse
    )

    # 10 CHOICE OPTIMIZATION
    ranked_actions = optimize_choice(
        strategy["actions"]
    )

    best_action = ranked_actions[0]["action"]

    return {

        "location": location,

        "zone": world.get("zone", "unknown"),

        "survival_score": survival.get("survival_score", 0),

        "collapse_risk": collapse.get("risk_level", "unknown"),

        "best_action": best_action,

        "alternatives": ranked_actions,

        "escape_routes": routes,

        "future_projection": future

    }
