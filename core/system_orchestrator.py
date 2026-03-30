from ENGINE.decision_engine import DecisionEngine
from SIMULATIONS.future_simulator import FutureSimulator
from DATABASE.db import MemoryDB
from PAYMENT.wallet_engine import topup

class SystemOrchestrator:

    def __init__(self):
        self.engine = DecisionEngine()
        self.sim = FutureSimulator()
        self.db = MemoryDB()

    def run(self, user_input):

        # 1 วิเคราะห์
        analysis = self.engine.analyze(user_input)

        # 2 จำ
        self.db.save(user_input, analysis)

        # 3 จำลอง
        future = self.sim.run(user_input, analysis)

        # 4 ตัดสินใจ
        if future["collapse"]:
            return "⚠️ เสี่ยงพัง หยุดก่อน"

        return f"👑 ระบบตอบ: {analysis}"
