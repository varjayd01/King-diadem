stats={

"questions":0,
"choices":0,
"crisis":0

}

def record_question():

    stats["questions"]+=1

def record_choice():

    stats["choices"]+=1

def record_crisis():

    stats["crisis"]+=1

def freedom_index():

    q=stats["questions"]

    if q==0:
        return 50

    value=(stats["choices"]-stats["crisis"])/q

    score=max(0,min(100,int(50+value*50)))

    return score
