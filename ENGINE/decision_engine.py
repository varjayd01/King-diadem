from typing import Dict, Any
from core.system_orchestrator import SystemOrchestrator

class DecisionEngine:

    def __init__(self):
        self.orchestrator = SystemOrchestrator()

    def run(self, data: Dict[str, Any]) -> Dict[str, Any]:

        user_input = data.get("input", "")
        state = data.get("state", {})

        energy = int(state.get("energy", 50))
        food = state.get("food", True)
        safe = state.get("safe_place", True)

        # 🧠 1. ให้ core เลือกว่าจะใช้ engine ไหน
        route = self.orchestrator.route(user_input)

        # 🧠 2. execute เฉพาะ engine ที่จำเป็น
        core_result = self.orchestrator.execute(route, data)

        # 🧠 3. fallback survival logic
        risk = self._assess_risk_local(energy, food, safe)

        choices = self._generate_choices(risk, energy)

        return {
            "route": route,
            "core_result": core_result,
            "risk": risk,
            "choices": choices,
            "input": user_input
        }

    # ---------------------

    def _assess_risk_local(self, energy, food, safe):

        if energy < 20 or not food or not safe:
            return "HIGH"

        if energy < 50:
            return "MEDIUM"

        return "LOW"

    # ---------------------

    def _generate_choices(self, risk, energy):

        if risk == "HIGH":
            return [
                "หยุดทุกการตัดสินใจที่ไม่จำเป็น",
                "ฟื้นฟูพลังงานทันที",
                "ออกจากสภาพแวดล้อมเสี่ยง"
            ]

        if risk == "MEDIUM":
            return [
                "ลดความเสี่ยงก่อนขยาย",
                "ประเมินทรัพยากรใหม่",
                "เลี่ยงการตัดสินใจใหญ่"
            ]

        return [
            "ดำเนินการต่อได้",
            "สังเกตการเปลี่ยนแปลง",
            "ขยายได้แบบควบคุม"
        ]
