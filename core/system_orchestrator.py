from core.decision_engine import DecisionEngine


class Orchestrator:

    def __init__(self):
        self.engine = DecisionEngine()

    def run(self, user_input, context):

        result = self.engine.run(user_input, context)

        return result
