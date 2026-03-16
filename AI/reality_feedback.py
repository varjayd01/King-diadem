feedback_store=[]

def record_feedback(problem,option,success):

    feedback_store.append({

        "problem":problem,
        "option":option,
        "success":success

    })


def feedback_stats():

    total=len(feedback_store)

    success=sum(1 for f in feedback_store if f["success"])

    if total==0:
        return {"success_rate":0}

    return {

        "success_rate":round(success/total,2),

        "samples":total

    }
