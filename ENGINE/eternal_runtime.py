# KING DIADEM Eternal Runtime
# Autonomous strategic runtime loop

import time

from core.drift_monitor import detect_drift
from core.dependency_cycle import dependent_cycle
from core.entropy_guard import entropy_guard
from core.vigilance_protocol import vigilance_check

from ENGINE.self_evolution import evolve_system
from SIMULATIONS.future_simulator import simulate_future
from GLOBAL_NODE.network_sync import sync_state


def eternal_runtime(system_state):

    print("\nKING DIADEM Eternal Runtime Activated\n")

    cycle = 0

    while True:

        cycle += 1

        print(f"\n===== Runtime Cycle {cycle} =====")

        # 1 dependent cycle evolution
        system_state = dependent_cycle(system_state)

        # 2 self evolution
        system_state = evolve_system(system_state)

        # 3 simulate possible futures
        future = simulate_future(system_state, 3)

        print("\nChosen future:", future)

        # 4 network synchronization
        sync_state(system_state)

        # 5 drift detection
        drift = detect_drift(system_state)
        print("\nDrift status:", drift)

        # 6 entropy protection
        guard = entropy_guard(system_state)
        print("Entropy guard:", guard)

        # 7 vigilance protocol
        vigilance = vigilance_check()
        print("Vigilance:", vigilance)

        # 8 sleep cycle
        print("\nCycle complete — waiting...\n")

        time.sleep(10)


def eternal_snapshot(system_state):
    """
    รอบเดียวของ eternal loop — สำหรับเชื่อมกับ decision / API โดยไม่ while True
    คืนสรุปสถานะเชิงกลยุทธ์แบบอ่านได้ (ไม่บล็อก worker)
    """
    if not isinstance(system_state, dict):
        system_state = {}

    state = dict(system_state)

    try:
        state = dependent_cycle(state)
    except Exception as e:
        state["_dependent_cycle_error"] = str(e)

    try:
        state = evolve_system(state)
    except Exception as e:
        state["_evolve_error"] = str(e)

    future = None
    try:
        future = simulate_future(state, 3)
    except Exception as e:
        future = {"error": str(e)}

    drift = None
    try:
        drift = detect_drift(state)
    except Exception as e:
        drift = {"error": str(e)}

    guard = None
    try:
        guard = entropy_guard(state)
    except Exception as e:
        guard = {"error": str(e)}

    vigilance = None
    try:
        vigilance = vigilance_check()
    except Exception as e:
        vigilance = {"error": str(e)}

    try:
        sync_state(state)
    except Exception as e:
        state["_sync_state_error"] = str(e)

    return {
        "state_after_cycle": state,
        "future_hint": future,
        "drift": drift,
        "entropy_guard": guard,
        "vigilance": vigilance,
    }
