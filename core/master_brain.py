def run_system(input_data, user):

    # 1. 🌍 เข้าโลกจริง
    world = load_world_state()

    # 2. 🧠 วิเคราะห์มนุษย์
    human = analyze_human(input_data)

    # 3. ⚠️ คำนวณความเสี่ยง
    risk = analyze_risk(input_data, world, human)

    # 4. 🔮 จำลองอนาคต
    future = simulate_outcome(input_data)

    # 5. 🎯 ตัดสินใจ
    decision = make_decision(input_data, risk, future)

    # 6. 🧬 อัปเดตโลก
    update_world(decision)

    # 7. 📊 บันทึก
    log_decision(user, decision)

    return decision
