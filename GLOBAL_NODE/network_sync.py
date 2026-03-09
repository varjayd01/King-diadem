# KING DIADEM Global Node Sync
# Allows multiple instances to exchange system states

import json
import time


def sync_state(system_state, node_id="local_node"):

    packet = {
        "node": node_id,
        "state": system_state,
        "timestamp": time.time()
    }

    print("\nBroadcasting system state")

    print(json.dumps(packet, indent=2))

    return packet


def receive_state(packet):

    print("\nReceived state from node:", packet["node"])

    return packet["state"]
