from AI.freedom_signal import freedom_index
from AI.global_decision_map import decision_map
from AI.galaxy_visualization import galaxy_nodes
from AI.reality_learning import learning_summary
from NETWORK.node_registry import get_nodes


def planetary_status():

    freedom = freedom_index()
    decisions = decision_map()
    galaxy = galaxy_nodes()
    learning = learning_summary()
    nodes = get_nodes()

    status="stable"

    if freedom < 30:
        status="compression"

    if freedom > 60:
        status="expansion"

    return {

        "planetary_status":status,
        "freedom_index":freedom,
        "decision_nodes":len(decisions),
        "galaxy_nodes":len(galaxy),
        "active_nodes":len(nodes),
        "learning":learning

    }
