def run_engine(text: str):
    text = text.strip()

    if not text:
        return "..."

    result = text

    # 🔥 decision (ต้องมี)
    try:
        from ENGINE.decision import think
    except:
        from engine.decision import think

    try:
        result = think(result)
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
