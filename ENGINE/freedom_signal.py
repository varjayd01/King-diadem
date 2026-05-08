# ENGINE/freedom_signal.py

_question_count = 0

def record_question():
    global _question_count
    _question_count += 1

def freedom_index() -> int:
    return _question_count
