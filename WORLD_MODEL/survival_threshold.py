SYSTEM_BELIEF = {

    "choice_minimum": 1,

    "survival_floor":[
        "food",
        "water",
        "shelter"
    ],

    "human_centered":True,

    "logic_agnostic":True,

    "nature_aligned":True

}


def check_choice(options):

    if options <= SYSTEM_BELIEF["choice_minimum"]:

        return "generate_more_options"

    return "stable"


def survival_priority(context):

    needs = SYSTEM_BELIEF["survival_floor"]

    for n in needs:

        if n not in context:

            return n

    return "stable"
