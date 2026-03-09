from GLOBAL_NODE.node_model import GlobalNode

global_node = GlobalNode()


def sync_node(location, data):

    global_node.register_node(location, data)

    world = global_node.update_world_state()

    return world
