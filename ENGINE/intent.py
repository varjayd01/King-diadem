from __future__ import annotations


def detect_intent(text: str) -> str:
    t = (text or "").casefold().strip()

    if not t:
        return "empty"

    if any(k in t for k in ("render", "deploy", "start command", "build command", "root directory", "web service")):
        return "deploy"

    if any(k in t for k in ("ui", "ux", "template", "index.html", "button", "input", "chat shell", "หน้าต่าง", "หน้าเว็บ")):
        return "ui"

    if any(k in t for k in ("cors", "fastapi", "uvicorn", "jinja2", "flask", "module not found", "traceback", "500", "error")):
        return "debug"

    if any(k in t for k in ("login", "sign up", "signup", "register", "password", "email", "auth")):
        return "auth"

    if any(k in t for k in ("api", "endpoint", "fetch", "json", "request", "response")):
        return "api"

    if any(k in t for k in ("help", "how", "ทำไง", "ควร", "แก้", "บอก", "สรุป")):
        return "help"

    return "general"
