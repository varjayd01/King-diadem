import random
from AI.decision_memory import get_memory


def galaxy_nodes():

    data=get_memory()

    nodes=[]

    for d in data:

        node={

            "x":random.randint(-100,100),
            "y":random.randint(-100,100),
            "size":len(d["options"])+1,
            "label":d["question"]

        }

        nodes.append(node)

    return nodes
