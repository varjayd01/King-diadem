// static/app.js — KING DIADEM core logic

const EMOTION_W = ["ท้อ","เสียใจ","กลัว","เครียด","ร้องไห้","หมดหวัง","ไม่ไหว","อยากตาย","เหนื่อยมาก","sad","hopeless","scared"];
const CRISIS_W  = ["อยากตาย","ไม่อยากอยู่","จบแล้ว","พังหมด"];

function detectMode(t) {
    const tl = t.toLowerCase();
    if (CRISIS_W.some(w => tl.includes(w))) return "crisis";
    if (EMOTION_W.some(w => tl.includes(w))) return "vega";
    return "lyla";
}

async function run() {
    const inputEl  = document.getElementById("input") || document.getElementById("main-input");
    const outputEl = document.getElementById("output");
    if (!inputEl) return;

    const text = inputEl.value.trim();
    if (!text) {
        if (outputEl) outputEl.innerText = "⚠ กรุณาพิมพ์สถานการณ์ก่อน";
        return;
    }

    if (outputEl) outputEl.innerText = "⟳ กำลังวิเคราะห์...";

    const mode = detectMode(text);

    try {
        const res = await fetch("/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input: text })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        if (data.error) {
            if (outputEl) outputEl.innerText = "❌ " + data.error;
            return;
        }

        if (outputEl) {
            const prefix = mode === "vega" ? "[VEGA]" : mode === "crisis" ? "[VEGA · CRISIS]" : "[LYLA]";
            if (data.ai_response) {
                outputEl.innerText = `${prefix}\n\n${data.ai_response}`;
            } else {
                outputEl.innerText = JSON.stringify(data, null, 2);
            }
        }

        const routeTag = document.getElementById("route-tag");
        if (routeTag) routeTag.textContent = `→ route: ${data.route || "general"} | risk: ${Math.round(data.risk_score || 0)} | mode: ${mode}`;

    } catch (err) {
        console.error(err);
        if (outputEl) outputEl.innerText = "🚫 SYSTEM ERROR\n" + err;
    }
}
