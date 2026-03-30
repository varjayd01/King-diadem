import os
from google import genai

from INTELLIGENCE.pattern_engine import analyze_patterns
from INTELLIGENCE.risk_engine import evaluate_risk
from INTELLIGENCE.decision_intelligence import intelligence_layer

from ENGINE.future_simulator import forecast
from ENGINE.collapse_predictor import predict_collapse
from ENGINE.choice_optimizer import optimize_choice
from ENGINE.persona_engine import get_persona
from ENGINE.world_model import build_world_state
from ENGINE.world_intelligence import build_risk_map, build_resource_map


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


class KingDiademEngine:

    def reality_filter(self, text):
        illusion_keywords = ["อยากได้ทันที", "รวยเร็ว", "ทางลัด", "ชนะ 100%"]

        flags = [k for k in illusion_keywords if k in text]

        return {
            "filtered_input": text,
            "illusion_flags": flags
        }

    def call_gemini(self, prompt):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"AI ERROR: {str(e)}"

    def run(self, user_input, mode="normal", persona_mode=None):

        # ===== 1. Reality =====
        reality = self.reality_filter(user_input)
        clean = reality["filtered_input"]

        # ===== 2. Pattern / Risk =====
        patterns = analyze_patterns(clean)
        risk = evaluate_risk(clean)

        # ===== 3. World =====
        world = build_world_state()
        risk_map = build_risk_map()
        resource_map = build_resource_map()

        # ===== 4. Simulation =====
        future = forecast()
        collapse = predict_collapse(risk["risk_level"])

        # ===== 5. External AI =====
        ai = self.call_gemini(clean)

        # ===== 6. Core Intelligence =====
        base = f"Structured analysis of: {clean}"
        intelligence = intelligence_layer(base, patterns, risk, ai)

        # ===== 7. Persona =====
        persona = get_persona(persona_mode)

        # ===== 8. Choices =====
        actions = [
            "reduce risk",
            "increase resource",
            "wait",
            "move location"
        ]

        ranked = optimize_choice(actions)

        # ===== FINAL OUTPUT =====
        final = f"""
[KING DIADEM FULL SYSTEM]

🧠 Input:
{clean}

⚠️ Illusion Flags:
{reality['illusion_flags']}

📊 Risk Level:
{risk.get('risk_level')}

🌍 World Nodes:
{world.get('total_nodes')}

📉 Collapse:
{collapse}

🔮 Future:
{future}

🎯 Best Action:
{ranked[0] if ranked else "NONE"}

🧬 Persona:
{persona}

🤖 Gemini Insight:
{ai}
"""

        return {
            "reality": reality,
            "risk": risk,
            "future": future,
            "collapse": collapse,
            "choices": ranked,
            "persona": persona,
            "final": final
        }
