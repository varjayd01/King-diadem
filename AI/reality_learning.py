learning_log=[]


def record_outcome(question,decision,outcome):

    node={

        "question":question,
        "decision":decision,
        "outcome":outcome

    }

    learning_log.append(node)



def learning_summary():

    success=0
    fail=0

    for n in learning_log:

        if n["outcome"]=="positive":

            success+=1

        if n["outcome"]=="negative":

            fail+=1

    return{

        "positive":success,
        "negative":fail,
        "total":len(learning_log)

    }


def get_learning():

    return learning_log[-50:]
