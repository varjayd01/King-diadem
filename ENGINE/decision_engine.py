import os, requests

from INTELLIGENCE.pattern_engine import analyze_patterns
from INTELLIGENCE.risk_engine import evaluate_risk
from INTELLIGENCE.decision_intelligence import intelligence_layer

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class KingDiademEngine:

    # ====== Layer 0: Reality Filter (ปฏิจสมุปบาท / FATE) ======
    def reality_filter(self, text):
        illusion_keywords = ["อยากได้ทันที", "รวยเร็ว", "ทางลัด", "ชนะ 100%"]

        filtered = text
        flags = []

        for k in illusion_keywords:
            if k in text:
                flags.append(k)

        return {
            "filtered_input": filtered,
            "illusion_flags": flags
        }

    # ====== Layer External AI ======
    def call_gemini(self, prompt):
        if not GEMINI_API_KEY:
            return "Gemini not configured"

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }

            res = requests.post(url, json=payload, timeout=10)
            data = res.json()

            return data['candidates'][0]['content']['parts'][0]['text']

        except Exception as e:
            return f"AI ERROR: {str(e)}"

    # ====== Council Mode ======
    def council_mode(self, user_input, internal, ai):
        return f"""
[COUNCIL MODE]

👑 KING (Core Logic):
{internal}

🌌 GEMINI (External Intelligence):
{ai}

⚖️ SYNTHESIS:
Combine internal structure + external insight.
Reject illusion. Preserve real choice.
"""

    # ====== MAIN ======
    def run(self, user_input, mode="normal"):

        # 1. Reality Filter
        reality = self.reality_filter(user_input)
        clean_input = reality["filtered_input"]

        # 2. Pattern + Risk
        patterns = analyze_patterns(clean_input)
        risk = evaluate_risk(clean_input)

        # 3. Internal decision
        base_decision = f"Structured analysis of: {clean_input}"

        # 4. External AI
        ai = self.call_gemini(clean_input)

        # 5. Intelligence layer
        intelligence = intelligence_layer(base_decision, patterns, risk, ai)

        # 6. Mode switch
        if mode == "council":
            final = self.council_mode(clean_input, base_decision, ai)
        else:
            final = f"""
[KING DIADEM OUTPUT]

Input: {clean_input}

Signal: {intelligence['system_signal']}
Risk: {risk['risk_level']}

Internal:
{base_decision}

External:
{ai}
"""

        return {
            "reality": reality,
            "intelligence": intelligence,
            "final": final
        }
