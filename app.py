# =====================
# INTELLIGENCE LAYER
# =====================
def decision_engine(intent, question):
    if intent == "SURVIVAL":
        return "เริ่มจากลดความเสี่ยงก่อน แล้วค่อยหาทางเพิ่มทางเลือก"

    if intent == "DECISION":
        return "แยกทางเลือก → ประเมิน downside → เลือกสิ่งที่พังยากที่สุด"

    return None


def fallback_engine(intent, question):
    if intent == "SURVIVAL":
        return "ถ้าทุกอย่างตัน ให้รักษาสิ่งที่ยังไม่พังก่อน"

    if intent == "DECISION":
        return "เลือกทางที่เสียหายน้อยที่สุดก่อน"

    return "ระบบยังทำงาน แต่ AI ไม่พร้อมใช้งาน"


# =====================
# TITLE AUTO
# =====================
def safe_title(text):
    return text[:30]


# =====================
# ASK (อัปเกรด)
# =====================
@app.post("/ask")
async def ask(req: Request):
    data = await req.json()
    cid = data["chat_id"]
    q = data["question"]

    chat = load_chat(cid)

    # USER MSG
    user_msg = {
        "role": "user",
        "content": q,
        "timestamp": now_iso()
    }
    chat["messages"].append(user_msg)

    context = build_context(chat["messages"])
    intent = detect_intent(q)

    # TRY AI
    try:
        answer = gemini_answer(q, context, intent)
    except Exception as e:
        print("AI FAIL:", e)

        # ใช้ decision ก่อน
        answer = decision_engine(intent, q)

        # ถ้ายังไม่ได้ → fallback
        if not answer:
            answer = fallback_engine(intent, q)

    # AUTO TITLE
    if chat["title"] == "New Chat" and len(chat["messages"]) <= 2:
        chat["title"] = safe_title(q)

    # AI MSG
    ai_msg = {
        "role": "assistant",
        "content": answer,
        "timestamp": now_iso(),
        "intent": intent
    }

    chat["messages"].append(ai_msg)
    save_chat(chat)

    return {
        "answer": answer,
        "intent": intent,
        "timestamp": ai_msg["timestamp"],
        "title": chat["title"]
    }
