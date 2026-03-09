# KING DIADEM Kernel Runtime
# Connects all core philosophy modules into a live system

from core.axioms import AXIOMS
from core.reality_laws import REALITY_LAWS
from core.dependency_cycle import dependent_cycle
from core.silent_canon import silent_canon
from core.vigilance_protocol import vigilance_check
from core.entropy_guard import entropy_check


def run_kernel(system_state):

    report = {}

    # Step 1 — Reality Drift
    next_state = dependent_cycle(system_state)

    report["next_state"] = next_state

    # Step 2 — Entropy Detection
    entropy_status = entropy_check(system_state)

    report["entropy_status"] = entropy_status

    # Step 3 — Vigilance Protocol
    vigilance = vigilance_check(system_state)

    report["vigilance"] = vigilance

    # Step 4 — Choice Preservation
    choice_count = system_state.get("choices", 1)

    canon_state = silent_canon(choice_count)

    report["silent_canon"] = canon_state

    # Step 5 — System Axioms
    report["axioms"] = AXIOMS

    # Step 6 — Reality Laws
    report["reality_laws"] = REALITY_LAWS

    return report


def kernel_demo():

    system_state = {

        "stability": 60,
        "entropy": 45,
        "choices": 3,
        "resources": 70

    }

    result = run_kernel(system_state)

    print("\nKING DIADEM Kernel Runtime\n")

    for k, v in result.items():

        print(k, ":", v)


if __name__ == "__main__":
    kernel_demo()
