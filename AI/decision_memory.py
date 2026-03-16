memory=[]

def save_decision(question,result):

    memory.append({

        "question":question,

        "result":result

    })

def get_memory():

    return memory[-20:]
