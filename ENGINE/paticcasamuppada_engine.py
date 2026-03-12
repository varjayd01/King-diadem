# KING DIADEM
# Paticcasamuppada Engine
# Infrastructure of Suffering

CHAIN = [
    "ignorance",
    "formations",
    "consciousness",
    "name_form",
    "sense_bases",
    "contact",
    "feeling",
    "craving",
    "clinging",
    "becoming",
    "birth",
    "collapse"
]


class DependentChain:

    def __init__(self):
        self.chain = CHAIN

    def simulate(self, root_event):

        results = []

        for step in self.chain:
            results.append({
                "stage": step,
                "triggered_by": root_event
            })

        return results


def detect_root_cause(context):

    keywords = [
        "misinformation",
        "ignorance",
        "bias",
        "fear",
        "panic"
    ]

    for k in keywords:
        if k in context.lower():
            return "ignorance"

    return "unknown"


def suffering_infrastructure(context):

    root = detect_root_cause(context)

    engine = DependentChain()

    chain = engine.simulate(root)

    return {
        "root_cause": root,
        "collapse_chain": chain
    }
