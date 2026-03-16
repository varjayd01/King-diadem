global_stats={
    "questions":0,
    "choices_created":0,
    "crisis":0,
    "business":0,
    "survival":0
}

def record_event(intent):

    global_stats["questions"]+=1

    if intent=="crisis":
        global_stats["crisis"]+=1

    if intent=="business":
        global_stats["business"]+=1

    if intent=="survival":
        global_stats["survival"]+=1


def record_choice():

    global_stats["choices_created"]+=1


def calculate_freedom():

    q=global_stats["questions"]
    c=global_stats["choices_created"]
    crisis=global_stats["crisis"]

    if q==0:
        return 50

    freedom=(c*2 - crisis)/q

    score=max(0,min(100,int(50+freedom*50)))

    return score
