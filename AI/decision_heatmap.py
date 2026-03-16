import random
from AI.decision_memory import get_memory


def heatmap():

    memory = get_memory()

    map_data=[]

    for m in memory:

        node={

            "lat":random.uniform(-90,90),
            "lon":random.uniform(-180,180),
            "pressure":len(m["options"])

        }

        map_data.append(node)

    return map_data
