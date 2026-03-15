from SIMULATIONS.scenario_tree import simulate_paths

def run_decision(problem, persona):

    paths = simulate_paths(problem)

    return {

        "problem":problem,

        "persona":persona,

        "paths":paths

    }
