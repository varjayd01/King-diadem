# KING DIADEM Core Axioms
# Stability Layer for Decision Engine

AXIOMS = {

    "A1": "Collapse occurs when choices disappear",

    "A2": "Preserve at least one viable option",

    "A3": "Do not optimize when survival floor is unstable",

    "A4": "Small drift compounds into system collapse",

    "A5": "Intervene only when choice approaches zero"

}


# -----------------------------
# DriftZero Governance Metrics
# -----------------------------

# Daily Harm Delta
# Maximum allowed system drift per day (0.1%)

DHD_MAX_THRESHOLD = 0.001


# Choice Safety Floor
# If choices drop below this, trigger intervention

CHOICE_MIN_THRESHOLD = 1


# Stop-the-Line Trigger
# If harm drift exceeds threshold, system must halt actions

STOP_THE_LINE = True
