class GlobalNode:

    def __init__(self):

        self.nodes = []
        self.world_state = {
            "food_index": 50,
            "risk_index": 50,
            "resource_index": 50
        }


    def register_node(self, location, data):

        node = {
            "location": location,
            "data": data
        }

        self.nodes.append(node)


    def update_world_state(self):

        if len(self.nodes) == 0:
            return self.world_state

        food_total = 0
        risk_total = 0

        for n in self.nodes:

            food_total += n["data"].get("food_score",50)
            risk_total += n["data"].get("risk_score",50)

        self.world_state["food_index"] = food_total / len(self.nodes)
        self.world_state["risk_index"] = risk_total / len(self.nodes)

        return self.world_state
