from ENGINE.decision_engine import DecisionEngine
from SIMULATIONS.future_simulator import FutureSimulator
from DATABASE.db import db

class Orchestrator:

    def __init__(self):
        self.engine = DecisionEngine()
        self.sim = FutureSimulator()

    def process(self, message):

        # วิเคราะห์
        result = self.engine.analyze(message)

        # จำ
        db.save(message, result)

        # จำลอง
        future = self.sim.simulate(message)

        # ตัดสินใจ
        if future.get("risk") == "high":
            return "⚠️ Risk detected"

        return result
