// static/app.js — client tone detection for KING DIADEM (used by index.html + /run payload)

const EMOTION_W = [
  "ท้อ", "เสียใจ", "กลัว", "เครียด", "ร้องไห้", "หมดหวัง", "ไม่ไหว", "อยากตาย", "เหนื่อยมาก",
  "sad", "hopeless", "scared", "cry", "panic", "depressed", "lonely", "ท้อแท้", "หมดแรง",
];

const CRISIS_W = ["อยากตาย", "ไม่อยากอยู่", "จบแล้ว", "พังหมด", "ฆ่า", "หมดแล้ว", "ไม่อยากมีชีวิต"];

function detectConversationMode(t) {
  const tl = String(t || "").toLowerCase();
  if (CRISIS_W.some(function (w) { return tl.includes(w); })) return "crisis";
  if (EMOTION_W.some(function (w) { return tl.includes(w); })) return "vega";
  return "lyla";
}

/** คำอธิบายสั้นๆ ให้ backend/LLM ปรับโทน — ไม่แทนที่ intent ฝั่งเซิร์ฟเวอร์ */
function buildVoiceHint(text, mode) {
  if (mode === "crisis")
    return "ผู้ใช้อาจอยู่ในวิกฤตความปลอดภัย — ตอบด้วยความเมตตาสูงสุด ไม่สั่งการ ไม่ตัดสิน เปิดทางรับความช่วยเหลือ (เช่น 1323)";
  if (mode === "vega")
    return "ผู้ใช้สื่ออารมณ์หนัก — ใช้โทนอ่อน สั้น ช้า รับรู้ความรู้สึกก่อน แล้วค่อยเสนอทางเลือกไม่เกิน 3 ข้อ";
  return "โทนปกติ/สังเกตการณ์ — กระชับ เป็นหลักฐาน คืนทางเลือก หลีกเลี่ยงภาษาคำสั่งหรือฟันธงแทนผู้ใช้";
}

window.detectConversationMode = detectConversationMode;
window.buildVoiceHint = buildVoiceHint;
