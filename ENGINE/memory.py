from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Dict, List


MAX_HISTORY = 12


@dataclass
class SessionState:
    history: List[dict] = field(default_factory=list)
    seed: str = ""
    mode: str = "chat"


_STORE: Dict[str, SessionState] = {}
_LOCK = Lock()


def get_state(session_id: str) -> SessionState:
    session_id = (session_id or "default").strip() or "default"
    with _LOCK:
        if session_id not in _STORE:
            _STORE[session_id] = SessionState()
        return _STORE[session_id]


def append_turn(session_id: str, role: str, text: str) -> List[dict]:
    state = get_state(session_id)
    item = {
        "role": role,
        "text": text,
        "at": datetime.now(timezone.utc).isoformat(),
    }
    state.history.append(item)
    if len(state.history) > MAX_HISTORY:
        state.history = state.history[-MAX_HISTORY:]
    return state.history


def snapshot(session_id: str) -> List[dict]:
    state = get_state(session_id)
    return list(state.history)


def reset_state(session_id: str) -> None:
    session_id = (session_id or "default").strip() or "default"
    with _LOCK:
        _STORE[session_id] = SessionState()
