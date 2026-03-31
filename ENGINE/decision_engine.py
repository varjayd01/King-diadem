def run(self, user_input, mode="normal", persona_mode=None):

    reality = self.reality_filter(user_input)
    clean = reality["filtered_input"]

    patterns = analyze_patterns(clean)
    risk = evaluate_risk(clean)

    world = build_world_state()
    risk_map = build_risk_map()
    resource_map = build_resource_map()

    future = forecast()
    collapse = predict_collapse(risk["risk_level"])

    # 🔥 STOP THE LINE
    if collapse or risk["risk_level"] >= 0.95:
        return {
            "text": "⛔ SYSTEM STOP — high collapse risk",
            "risk": risk["risk_level"],
            "choices": ["STOP", "WAIT", "EXIT"]
        }

    # 🔥 AI (controlled)
    ai = self.call_gemini(clean)
    if "ERROR" in ai:
        ai = "AI unavailable"

    if risk["risk_level"] > 0.8:
        ai = "High risk — AI ignored"

    base = f"Structured analysis: {clean}"
    intelligence = intelligence_layer(base, patterns, risk, ai)

    persona = get_persona(persona_mode)

    actions = [
        "reduce risk",
        "increase resource",
        "wait",
        "move location"
    ]

    ranked = optimize_choice(
        actions,
        risk=risk,
        collapse=collapse,
        world=world
    )

    return {
        "text": intelligence,
        "risk": risk["risk_level"],
        "collapse": collapse,
        "future": future,
        "persona": persona,
        "choices": ranked,
        "best_action": ranked[0] if ranked else None
    }
