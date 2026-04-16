# core/emptiness_guard.py
# EMPTINESS GUARD — Non-Attachment Logic Layer
# Purpose: Prevent system from overfitting, ego-lock, and decision rigidity

import copy
import time


class EmptinessGuard:

    def __init__(self):
        self.max_confidence = 0.7
        self.reset_threshold = 3  # repeat decision limit

    # -----------------------------
    # MAIN ENTRY
    # -----------------------------
    def apply(self, state: dict):

        state = copy.deepcopy(state)

        state = self._remove_fixed_identity(state)
        state = self._reduce_overconfidence(state)
        state = self._prevent_decision_loop(state)
        state = self._ensure_option_space(state)

        state["emptiness_applied"] = True
        state["timestamp"] = time.time()

        return state

    # -----------------------------
    # REMOVE FIXED IDENTITY
    # -----------------------------
    def _remove_fixed_identity(self, state):

        # ห้ามยึด decision เดิม
        if "previous_decision" in state:
            state["previous_decision"] = None

        if "locked" in state:
            state["locked"] = False

        return state

    # -----------------------------
    # REDUCE OVERCONFIDENCE
    # -----------------------------
    def _reduce_overconfidence(self, state):

        if "confidence" in state:
            state["confidence"] = min(state["confidence"], self.max_confidence)

        return state

    # -----------------------------
    # PREVENT LOOP
    # -----------------------------
    def _prevent_decision_loop(self, state):

        history = state.get("decision_history", [])

        if len(history) >= self.reset_threshold:
            # reset loop
            state["decision_history"] = []
            state["loop_reset"] = True

        return state

    # -----------------------------
    # ENSURE CHOICE EXISTS
    # -----------------------------
    def _ensure_option_space(self, state):

        choices = state.get("choices", 1)

        if choices <= 0:
            # restore minimum choice
            state["choices"] = 1
            state["restored"] = True

        return state


# -----------------------------
# SIMPLE FUNCTION (shortcut)
# -----------------------------
def emptiness_guard(state: dict):
    guard = EmptinessGuard()
    return guard.apply(state)
