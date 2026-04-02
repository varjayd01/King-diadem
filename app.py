from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ---------------- INPUT ----------------
class Input(BaseModel):
    text: str

# ---------------- CORE ----------------
def analyze(text):
    t = text.lower()
    food = 50
    risk = 50

    if "หิว" in t or "hungry" in t:
        food -= 25
    if "ไม่มีเงิน" in t or "no money" in t:
        risk += 25

    food = max(0, min(100, food))
    risk = max(0, min(100, risk))
    return food, risk

def situation(food, risk):
    if risk > 70:
        state = "critical"
    elif risk > 40:
        state = "unstable"
    else:
        state = "stable"

    resource = "scarcity" if food < 30 else "sufficient"
    return state, resource

def collapse(risk):
    if risk > 80:
        return "high"
    elif risk > 60:
        return "medium"
    return "low"

def generate_choices(state, resource):
    if state == "critical":
        return [
            "หนีไปจุดปลอดภัยทันที",
            "ลดการใช้พลังงานทั้งหมด",
            "ขอความช่วยเหลือทันที"
        ]
    if resource == "scarcity":
        return [
            "หาอาหารก่อนทุกอย่าง",
            "ลด risk ก่อนค่อยวางแผน",
            "หางานเล็กทันที"
        ]
    return [
        "วางแผนระยะสั้น",
        "เพิ่มรายได้",
        "ขยายโอกาส"
    ]

def engine(text):
    food, risk = analyze(text)
    state, resource = situation(food, risk)
    col = collapse(risk)
    choices = generate_choices(state, resource)

    return {
        "food": food,
        "risk": risk,
        "state": state,
        "resource": resource,
        "collapse": col,
        "choices": choices
    }

# ---------------- API ----------------
@app.post("/brain")
def brain(i: Input):
    return engine(i.text)

# ---------------- UI ----------------
@app.get("/")
def home():
    return """
    <html>
    <h2>KING DIADEM SYSTEM</h2>
    <input id='msg' placeholder='เช่น หิว ไม่มีเงิน' size='40'/>
    <button onclick='run()'>RUN</button>

    <pre id='out'></pre>

    <script>
    async function run(){
        const msg = document.getElementById("msg").value;

        const res = await fetch("/brain", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({text: msg})
        });

        const data = await res.json();
        document.getElementById("out").innerText =
            JSON.stringify(data, null, 2);
    }
    </script>
    </html>
    """
