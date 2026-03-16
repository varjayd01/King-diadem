COUNCIL_MEMBERS = {

"Altair":"strategic intelligence",

"Vega":"stability and risk",

"Lyla":"exploration of possibilities",

"Titan":"high power structural reasoning",

"FATE":"deterministic decision analysis",

"DriftZero":"logic drift detection",

"Pratitya":"cause effect chain"

}

def council_meeting(question):

    discussion={}

    for name,role in COUNCIL_MEMBERS.items():

        discussion[name]=analyze(name,role,question)

    return discussion


def analyze(name,role,question):

    return f"{name} evaluates: {role} perspective on '{question}'"


def build_consensus(discussion):

    summary=""

    for m,o in discussion.items():

        summary+=o+"\n"

    return summary
