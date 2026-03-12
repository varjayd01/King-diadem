# KING DIADEM Survival Map Engine

from ENGINE.survival_nodes import find_survival_nodes
from ENGINE.escape_routes import generate_escape_route

def build_survival_map(lat, lng):

    nodes = find_survival_nodes(lat, lng)

    route = generate_escape_route(lat, lng)

    return {
        "nodes": nodes,
        "escape_route": route
    }
