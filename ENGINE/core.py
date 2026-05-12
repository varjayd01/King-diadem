def run_engine(text: str):
    text = text.strip()

    if not text:
        return "..."

    result = text

    # 🔥 decision (ต้องมี) — ไฟล์จริงชื่อ dicision.py
    think_fn = None
    try:
        from ENGINE.dicision import think as think_fn
    except Exception:
        try:
            from engine.dicision import think as think_fn
        except Exception:
            pass
    if think_fn is None:
        return "decision error: cannot import ENGINE.dicision.think"

    try:
        result = think_fn(result)
    except Exception as e:
        return f"decision error: {str(e)}"

    # 🔥 โมดูลเสริม (มีหรือไม่มีก็ไม่พัง)
    try:
        from ENGINE.brain import process
        result = process(result)
    except:
        pass

    try:
        from ENGINE.memory import recall
        result = recall(result)
    except:
        pass

    return result
