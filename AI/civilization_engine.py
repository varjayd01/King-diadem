# AI/civilization_engine.py
"""
Civilization Engine — บันทึก decision nodes ของ KING DIADEM
"""
import time

civilization_nodes = []

def add_node(problem: str, options: list, route: str = "general"):
    node = {
        "problem":   problem,
        "options":   options,
        "route":     route,
        "timestamp": time.time(),
    }
    civilization_nodes.append(node)
    # keep last 200
    if len(civilization_nodes) > 200:
        civilization_nodes.pop(0)

def get_nodes():
    return civilization_nodes[-50:]

def get_node_summary() -> str:
    if not civilization_nodes:
        return "ยังไม่มี decision nodes"
    last = civilization_nodes[-5:]
    lines = []
    for n in last:
        lines.append(f"• {n['problem'][:60]} [{n['route'].upper()}]")
    return "\n".join(lines)
