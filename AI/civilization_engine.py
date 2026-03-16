civilizations=[]

def create_node(user,problem,options):

    node={

        "user":user,

        "problem":problem,

        "options":options

    }

    civilizations.append(node)

    return node


def get_civilization():

    return civilizations[-50:]
