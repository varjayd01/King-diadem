# ==========================================
# 👑 KING DIADEM — app.py v3.0
# แก้: history + route + voice_mode ถึง LLM จริง
# ==========================================

from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import os, json, stripe, datetime
from urllib.parse import quote, unquote

try:
    from ENGINE.decision_engine import DecisionEngine, run_decision as full_run_decision
except Exception:
    DecisionEngine = None
    full_run_decision = None

try:
    from ENGINE.human_engine import analyze_human
    from AI.intent_engine import analyze_intent
    from AI.freedom_signal import record_question, freedom_index, record_choice, record_crisis
except Exception as e:
    print(f"⚠ ENGINE IMPORT ERROR: {e}")
    analyze_human = analyze_intent = record_question = freedom_index = None
    record_choice = record_crisis = None

try:
    from core.llm_gemini import GeminiLLM
    from core.lyla_kernel import LylaKernel
    lyla = LylaKernel()
    llm  = GeminiLLM(model="gemini-2.0-flash")
    print("✅ LYLA & Gemini Loaded")
except Exception as e:
    print(f"⚠ LLM/LYLA ERROR: {e}")
    llm = lyla = None

try:
    from core.system_orchestrator import get_orchestrator
    _orchestrator = get_orchestrator()
    print("✅ SystemOrchestrator Loaded")
except Exception as e:
    print(f"⚠ ORCHESTRATOR ERROR: {e}")
    _orchestrator = None

try:
    from DATABASE.db import (
        init_db, log_decision, get_credits, add_credits,
        ensure_user, save_chat_state, load_chat_state,
    )
    init_db()
    print("✅ Database initialized")
except Exception as e:
    print(f"⚠ DB ERROR: {e}")
    init_db = log_decision = get_credits = add_credits = None
    ensure_user = save_chat_state = load_chat_state = None

try:
    from AI.planetary_dashboard import planetary_status
    from AI.civilization_learning import record_learning, get_learning
    from AI.civilization_engine import add_node, get_nodes
    print("✅ Civilization Engine Loaded")
except Exception as e:
    print(f"⚠ CIVILIZATION ERROR: {e}")
    planetary_status = get_learning = get_nodes = None
    record_learning = add_node = None

try:
    from ENGINE.realhuman_survivorengine import RealHumanSurvivorEngine, parse_state_from_context
    _survivor_engine = RealHumanSurvivorEngine()
    print("✅ RealHuman SurvivorEngine Loaded")
except Exception as e:
    print(f"⚠ SURVIVOR ENGINE ERROR: {e}")
    _survivor_engine = None
    parse_state_from_context = None

try:
    from authlib.integrations.starlette_client import OAuth
    oauth = OAuth()
    oauth.register(
        name="google",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
    print("✅ Google OAuth Loaded")
except Exception as e:
    print(f"⚠ OAuth ERROR: {e}")
    oauth = None

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
app = FastAPI(title="KING DIADEM OS")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "king-diadem-secret-2026"))
engine = DecisionEngine() if DecisionEngine else None
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
@app.head("/")
def root():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {
        "status": "alive 👑",
        "llm_loaded":    llm is not None,
        "engine_loaded": engine is not None,
        "lyla_loaded":   lyla is not None,
        "stripe_loaded": bool(os.getenv("STRIPE_SECRET_KEY")),
        "freedom_score": freedom_index() if freedom_index else 0,
        "db_initialized": init_db is not None,
    }




@app.get("/time")
def get_time():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    return {
        "iso": now.isoformat(),
        "display": now.strftime("%d/%m/%Y %H:%M"),
        "date": now.strftime("%A %d %B %Y"),
        "time": now.strftime("%H:%M"),
        "day_th": ["จันทร์","อังคาร","พุธ","พฤหัส","ศุกร์","เสาร์","อาทิตย์"][now.weekday()],
        "tz": "Asia/Bangkok (UTC+7)"
    }

@app.get("/dashboard")
async def dashboard():
    try:    status = planetary_status() if planetary_status else {}
    except: status = {}
    try:    learning = get_learning() if get_learning else []
    except: learning = []
    try:    nodes = get_nodes() if get_nodes else []
    except: nodes = []
    return {
        "observer": "KING DIADEM",
        "planetary": status,
        "recent_learning": learning[-10:] if learning else [],
        "active_nodes": nodes[-10:] if nodes else [],
        "freedom_index": freedom_index() if freedom_index else 50,
        "sunyata_signal": "ทุกระบบว่างเปล่าจากการมีอยู่โดยตัวเอง — ทางเลือกเกิดจากความสัมพันธ์เท่านั้น",
    }


# ── Auth ──────────────────────────────────────────────────────────
def _cookie_ascii(value: str) -> str:
    return quote(str(value), safe="") if value else ""


@app.get("/login/google")
async def google_login(request: Request):
    if not oauth:
        return JSONResponse({"error": "OAuth not configured"}, status_code=500)
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "https://king-diadem.onrender.com/auth/google/callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/google/callback")
async def google_callback(request: Request):
    if not oauth:
        return RedirectResponse("/static/login.html?error=oauth_disabled")
    try:
        token = await oauth.google.authorize_access_token(request)
        user  = token.get("userinfo")
        email = user.get("email", "unknown")
        name  = user.get("name", email)
        if ensure_user: ensure_user(email)
        if get_credits and add_credits and get_credits(email) == 0:
            add_credits(email, 10)
        try:
            sess = getattr(request, "session", None)
            if sess:
                for k in list(sess.keys()):
                    if isinstance(k, str) and (k.startswith("_state") or "oauth" in k.lower() or k.endswith("_token")):
                        sess.pop(k, None)
        except: pass
        response = RedirectResponse("/")
        response.set_cookie("kd_email", _cookie_ascii(email), max_age=86400*30)
        response.set_cookie("kd_name",  _cookie_ascii(name),  max_age=86400*30)
        return response
    except Exception as e:
        print("google_callback:", repr(e))
        return RedirectResponse("/static/login.html?error=oauth_error")


@app.get("/me")
async def me(request: Request):
    email = unquote(request.cookies.get("kd_email") or "")
    name  = unquote(request.cookies.get("kd_name")  or "")
    if not email: return {"logged_in": False}
    credits = get_credits(email) if get_credits else 0
    return {"logged_in": True, "email": email, "name": name, "credits": credits}


@app.get("/api/chat-state")
async def get_chat_state(request: Request):
    email = unquote(request.cookies.get("kd_email") or "").strip()
    if not email or not load_chat_state: return {"state": None}
    raw = load_chat_state(email)
    if not raw: return {"state": None}
    try:    return {"state": json.loads(raw)}
    except: return {"state": None}


@app.put("/api/chat-state")
async def put_chat_state(request: Request, data: dict):
    email = unquote(request.cookies.get("kd_email") or "").strip()
    if not email or not save_chat_state:
        return JSONResponse({"ok": False, "error": "unauthorized"}, status_code=401)
    state = data.get("state") if isinstance(data.get("state"), dict) else data
    if not isinstance(state, dict):
        return JSONResponse({"ok": False, "error": "invalid"}, status_code=400)
    save_chat_state(email, json.dumps(state, ensure_ascii=False))
    return {"ok": True}


@app.post("/api/chat-state")
async def post_chat_state(request: Request, data: dict):
    return await put_chat_state(request, data)


@app.post("/logout")
async def logout():
    r = JSONResponse({"status": "ok"})
    r.delete_cookie("kd_email")
    r.delete_cookie("kd_name")
    return r


@app.post("/register")
async def register(data: dict):
    email = (data.get("email") or "").strip()
    if not email: return {"status": "error", "message": "กรุณากรอก email"}
    if ensure_user: ensure_user(email)
    if add_credits and get_credits and get_credits(email) == 0:
        add_credits(email, 10)
    credits = get_credits(email) if get_credits else 0
    r = JSONResponse({"status": "ok", "email": email, "credits": credits})
    r.set_cookie("kd_email", _cookie_ascii(email), max_age=86400*30)
    r.set_cookie("kd_name",  _cookie_ascii(email), max_age=86400*30)
    return r


@app.post("/login")
async def login_email(data: dict):
    email = (data.get("email") or "").strip()
    if not email: return {"status": "error"}
    if ensure_user: ensure_user(email)
    credits = get_credits(email) if get_credits else 0
    r = JSONResponse({"status": "ok", "email": email, "credit": credits})
    r.set_cookie("kd_email", _cookie_ascii(email), max_age=86400*30)
    r.set_cookie("kd_name",  _cookie_ascii((data.get("name") or email).strip()), max_age=86400*30)
    return r


# ── Helpers ───────────────────────────────────────────────────────
def _route_bias(route: str, text: str) -> str:
    tags = {
        "risk":     "[โหมด: ประเมินความเสี่ยง/ผลกระทบ]",
        "survival": "[โหมด: ความอยู่รอดพื้นฐาน — อาหาร ที่พัก ความปลอดภัย]",
        "collapse": "[โหมด: ลูกโซ่ความเสียหาย/แรงกดดันสะสม]",
        "civil":    "[โหมด: งาน/พลเมือง/ความรับผิดชอบต่อส่วนรวม]",
        "vega":     "[โหมด: อนาคต/โลกกว้าง/ทางเลือกระยาว]",
    }
    tag = tags.get(route, "")
    return f"{tag} {text}".strip() if tag else text


def _build_history_text(history: list) -> str:
    if not history:
        return ""
    lines = []
    for turn in history[-10:]:
        role    = turn.get("role", "user")
        content = str(turn.get("content", "")).strip()
        if content:
            lines.append(f"{'ผู้ใช้' if role == 'user' else 'LYLA'}: {content}")
    if not lines:
        return ""
    return "=== บทสนทนาก่อนหน้า ===\n" + "\n".join(lines) + "\n========================\n\n"


# ── /run ─────────────────────────────────────────────────────────
@app.post("/run")
@app.post("/decision")
async def run_kernel(request: Request, data: dict):
    user_input = data.get("input") or data.get("text") or ""
    if not user_input:
        return {"error": "Input is required"}

    email      = unquote(request.cookies.get("kd_email", "anonymous"))
    route      = data.get("route") or "general"
    voice_mode = (data.get("voice_mode") or "lyla").lower().strip()
    history    = data.get("history") or []

    if record_question: record_question()

    human_state = (
        analyze_human(data.get("context", {})) if analyze_human
        else {"entropy": 40, "resource": 50, "stability": 60, "risk_score": 10}
    )

    # ★ RealHuman SurvivorEngine — วิเคราะห์สถานะมนุษย์จริง ★
    survivor_ctx = ""
    if _survivor_engine and parse_state_from_context:
        try:
            h_state  = parse_state_from_context(data.get("context", {}))
            survival = _survivor_engine.run(h_state)
            survivor_ctx = survival.context_for_lyla
            # ถ้าตัดสินใจไม่ได้ — บอก LYLA ห้ามผลักดัน
            if not survival.can_decide:
                survivor_ctx += " | USER_CANNOT_DECIDE_NOW"
        except Exception as _e:
            survivor_ctx = 
    intent = (
        analyze_intent(user_input) if analyze_intent
        else {"intent": "general", "confidence": 0.5}
    )

    # ★ ถ้ามี full_run_decision / engine ใช้ก่อน ★
    # ★ SystemOrchestrator — เชื่อมทุก engine ★
    if _orchestrator:
        try:
            result = _orchestrator.run({
                **data,
                "input":      user_input,
                "route":      route,
                "voice_mode": voice_mode,
                "history":    history,
                "context":    data.get("context", {}),
            })
            result["route"] = result.get("route") or route
            # เพิ่ม pattern/risk ถ้า engine อื่นไม่ได้ใส่
            if "pattern" not in result:
                result["pattern"] = human_state
            if "risk_score" not in result:
                result["risk_score"] = human_state.get("risk_score", 10)
            # log + learning
            if log_decision and result.get("ai_response"):
                try: log_decision(email, user_input, result.get("route","general"), str(result.get("ai_response","")))
                except: pass
            if record_choice: record_choice()
            return result
        except Exception as _oe:
            print(f"⚠ orchestrator.run error: {_oe}")
            # fall through to LLM direct

    if full_run_decision or engine:
        routed  = _route_bias(route, user_input)
        payload = {**data, "input": routed}
        result  = full_run_decision(payload) if full_run_decision else engine.run(payload)
        result["route"] = result.get("route") or route

    else:
        # ★ ใช้ LLM โดยตรง — ส่ง history + route + voice_mode ★
        if llm:
            try:
                _ctx_parts = [
                    f"entropy={human_state.get('entropy')} stability={human_state.get('stability')} route={route}",
                ]
                if survivor_ctx:
                    _ctx_parts.append(survivor_ctx)
                reply = llm.generate_with_governance(
                    prompt=user_input,
                    additional_context=" | ".join(_ctx_parts),
                    history=history,
                    route=route,
                    voice_mode=voice_mode,
                )
            except Exception as e:
                reply = f"[Gemini Error: {e}]"
        else:
            reply = "[KING DIADEM — Offline]\n— Fail Less. Harm Less. Restore Choice. —"

        result = {
            "observer":   "KING DIADEM",
            "status":     "SUCCESS",
            "route":      intent.get("intent", "general") if isinstance(intent, dict) else "general",
            "ai_response": reply,
            "governance": {"intent": intent, "human_state": human_state},
            "pattern":    human_state,
            "risk_score": human_state.get("risk_score", 10),
        }
        result["route"] = result.get("route") or route

    # log
    if log_decision and result.get("ai_response"):
        try: log_decision(email, user_input, result.get("route","general"), str(result.get("ai_response","")))
        except: pass

    if record_learning and result.get("ai_response"):
        try:
            record_learning(
                question=user_input,
                decision=result.get("route","general"),
                planet_context={"entropy": human_state.get("entropy"), "stability": human_state.get("stability")},
                success=None,
            )
        except: pass

    if add_node:
        try: add_node(user_input[:80], [route], route)
        except: pass

    if record_choice: record_choice()
    return result


# ── /simulate ────────────────────────────────────────────────────
@app.post("/simulate")
async def simulate_future(data: dict):
    user_input = data.get("input", "")
    paths      = data.get("paths") or []
    extra      = ""
    if paths:
        extra = "\nทางเลือกที่ผู้ใช้ระบุ:\n" + "\n".join(f"- {p}" for p in paths if str(p).strip())
    if not llm:
        return {"status": "OFFLINE", "message": "LLM not found"}
    try:
        raw = llm.generate_with_governance(
            prompt=f"จำลองอนาคต 30/90/365 วัน: {user_input}{extra}",
            additional_context="mode=simulation analyze paths and risks",
            route="vega",
        )
    except Exception as e:
        raw = f"Simulation error: {e}"
    observation = lyla.observe(user_input) if lyla else {"stability": "NOMINAL"}
    return {"status": "SUCCESS", "simulation": raw, "lyla_observation": observation}


# ── /analyze-image ───────────────────────────────────────────────
@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    if not llm:
        return {"status": "OFFLINE", "message": "LLM not found"}
    try:
        from google import genai as _genai
        from google.genai import types as _types
        content = await file.read()
        client  = _genai.Client(api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY2"))
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[_types.Content(role="user", parts=[
                _types.Part.from_bytes(data=content, mime_type=file.content_type or "image/jpeg"),
                _types.Part.from_text(text="วิเคราะห์ภาพนี้ผ่าน LYLA Governance Framework:\n1. สิ่งที่เห็น\n2. drift หรือความเสี่ยง\n3. ทางเลือก ≤3 ทาง\nตอบตรง ไม่ตัดสิน"),
            ])],
        )
        return {"status": "SUCCESS", "analysis": response.text, "filename": file.filename}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/upload-image")
async def upload_image_alias(file: UploadFile = File(...)):
    return await analyze_image(file)


# ── /payment ─────────────────────────────────────────────────────
@app.post("/payment/create-checkout")
async def create_checkout(request: Request):
    payload = await request.json()
    plan    = payload.get("plan", "basic")
    email   = payload.get("email") or payload.get("api_key") or request.cookies.get("kd_email", "guest")
    plans   = {
        "basic":        {"amount": 29900, "currency": "thb", "name": "KING DIADEM Basic — ฿299/เดือน"},
        "civilization": {"amount": 99900, "currency": "thb", "name": "KING DIADEM Civilization — ฿999/เดือน"},
        "topup":        {"amount": 5000,  "currency": "thb", "name": "KING DIADEM Credits — ฿50"},
    }
    p = plans.get(plan, plans["basic"])
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price_data": {"currency": p["currency"], "product_data": {"name": p["name"]}, "unit_amount": p["amount"]}, "quantity": 1}],
            mode="payment",
            success_url="https://king-diadem.onrender.com/success?plan=" + plan,
            cancel_url="https://king-diadem.onrender.com/",
            customer_email=email if "@" in str(email) else None,
            metadata={"email": str(email), "plan": plan},
        )
        return {"url": session.url}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/success")
async def success():
    return FileResponse("static/index.html")


@app.get("/cancel")
async def cancel():
    return FileResponse("static/index.html")


@app.get("/credits")
async def credits(request: Request):
    email = request.cookies.get("kd_email", "anonymous")
    c = get_credits(email) if get_credits else 0
    return {"email": email, "credits": c}
