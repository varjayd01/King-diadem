import time

class GlobalNode:

    def __init__(self):

        # ใช้ dict ป้องกัน node ซ้ำ
        self.nodes = {}

        self.world_state = {
            "food_index": 50,
            "risk_index": 50,
            "resource_index": 50,
            "trend": "stable",
            "collapse_probability": 0.0
        }


    def register_node(self, location, data):

        node = {
            "data": data,
            "time": time.time()
        }

        # overwrite node เดิม
        self.nodes[location] = node


    def update_world_state(self):

        if len(self.nodes) == 0:
            return self.world_state

        food_total = 0
        risk_total = 0

        for location, node in self.nodes.items():

            food_total += node["data"].get("food_score", 50)
            risk_total += node["data"].get("risk_score", 50)

        food_index = food_total / len(self.nodes)
        risk_index = risk_total / len(self.nodes)

        self.world_state["food_index"] = food_index
        self.world_state["risk_index"] = risk_index

        # trend logic
        if risk_index > 70:
            self.world_state["trend"] = "danger"

        elif risk_index < 40:
            self.world_state["trend"] = "stable"

        else:
            self.world_state["trend"] = "warning"

        # collapse probability
        self.world_state["collapse_probability"] = min(1.0, risk_index / 100)

        return self.world_state
