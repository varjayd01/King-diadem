memory_store=[]

def save_decision(problem,options):

    entry={
        "problem":problem,
        "options":options
    }

    memory_store.append(entry)

def get_recent():

    return memory_store[-20:]
