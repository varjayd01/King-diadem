import time
import threading

NODES={}
LOCK=threading.Lock()

NODE_TIMEOUT=120


def register_node(node_id,data):

    with LOCK:

        data["last_seen"]=time.time()

        NODES[node_id]=data


def heartbeat(node_id):

    with LOCK:

        if node_id in NODES:

            NODES[node_id]["last_seen"]=time.time()


def remove_dead_nodes():

    now=time.time()

    with LOCK:

        dead=[]

        for nid,node in NODES.items():

            if now-node["last_seen"]>NODE_TIMEOUT:

                dead.append(nid)

        for nid in dead:

            del NODES[nid]


def get_nodes():

    remove_dead_nodes()

    return NODES
