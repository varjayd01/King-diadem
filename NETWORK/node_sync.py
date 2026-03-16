import random
from NETWORK.node_registry import get_nodes


def network_status():

    nodes=get_nodes()

    n=len(nodes)

    health="stable"

    if n>10:

        health="expanding"

    if n>100:

        health="planetary"

    return {

        "active_nodes":n,

        "network_health":health

    }
