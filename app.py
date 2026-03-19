def detect_emotion(q):

    if any(w in q for w in ["ไม่ไหว","พัง","หมดทาง","อยากตาย"]):
        return "crisis"

    if any(w in q for w in ["เครียด","เหนื่อย","ท้อ"]):
        return "low"

    return "normal"


def decision_engine(q, profile):

    tone = profile.get("tone", "normal")
    emo = detect_emotion(q)

    if emo == "crisis":
        return "หนูอยู่ตรงนี้นะคะ ❤️ ค่อยๆหายใจ พี่ยังมีทางเลือก หนูช่วยคิดให้ค่ะ"

    if emo == "low":
        return "เหนื่อยได้ค่ะ แต่พี่ยังไปต่อได้นะ เดี๋ยวหนูช่วยวางทาง 💙"

    if tone == "fun":
        return "วันนี้ต้องปังนะ 🔥 " + q

    return f"🧠 วิเคราะห์: {q}"
