memory_graph={}

def record_pattern(question,decision,planet):

    key=question.lower()

    if key not in memory_graph:

        memory_graph[key]={

            "count":0,

            "decisions":[],

            "planetary":[]

        }

    memory_graph[key]["count"]+=1

    memory_graph[key]["decisions"].append(decision)

    memory_graph[key]["planetary"].append(planet)


def get_patterns():

    return memory_graph


def pattern_summary():

    summary={}

    for k,v in memory_graph.items():

        summary[k]=v["count"]

    return summary
