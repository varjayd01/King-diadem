# KING DIADEM Core Orchestrator
# Connects all system engines

from ENGINE.situation_analyzer import analyze_situation
from ENGINE.human_state_engine import analyze_human_state
from ENGINE.relationship_engine import analyze_relationship
from ENGINE.collapse_predictor import predict_collapse
from ENGINE.path_generator import generate_paths
from ENGINE.intervention_engine import intervention
from ENGINE.decision_engine import decision_engine

from core.silent_canon import SILENT_CANON
from core.axioms import AXIOMS
from core.memory_store import record_decision


def king_diadem(question: str):

    # -----------------------------
    # PERCEPTION
    # -----------------------------

    situation = analyze_situation(question)
    human_state = analyze_human_state(question)

    # -----------------------------
    # RELATIONSHIP ANALYSIS
    # -----------------------------

    relationship_state = analyze_relationship(human_state)

    # -----------------------------
    # COLLAPSE PREDICTION
    # -----------------------------

    collapse_risk = predict_collapse(human_state)

    # -----------------------------
    # PATH GENERATION
    # -----------------------------

    paths = generate_paths(human_state)

    # -----------------------------
    # INTERVENTION
    # -----------------------------

    help_plan = intervention(paths)

    # -----------------------------
    # DECISION ENGINE
    # -----------------------------

    decision = decision_engine(
        situation.get("location", "unknown"),
        situation.get("food", "medium"),
        situation.get("money", 0),
        situation.get("risk", "medium")
    )

    # -----------------------------
    # FINAL RESULT
    # -----------------------------

    result = {
        "question": question,
        "situation": situation,
        "human_state": human_state,
        "relationship_state": relationship_state,
        "collapse_risk": collapse_risk,
        "paths": paths,
        "intervention": help_plan,
        "decision": decision,
        "axioms": AXIOMS,
        "silent_canon": SILENT_CANON
    }

    record_decision(result)

    return result
