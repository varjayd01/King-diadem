from GLOBAL_NODE.node_model import GlobalNode

global_node = GlobalNode()


def sync_node(location, data):

    global_node.register_node(location, data)

    world = global_node.update_world_state()

    return world


def sync_state(system_state):
    """รองรับ eternal_runtime — sync แบบครั้งเดียวโดยไม่บังคับโครงสร้างพิเศษ"""
    if not isinstance(system_state, dict):
        return system_state
    try:
        return sync_node("eternal", dict(system_state))
    except Exception:
        return system_state
