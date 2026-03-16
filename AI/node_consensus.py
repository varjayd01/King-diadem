import random

def node_vote(options,nodes):

    votes={o:0 for o in options}

    node_count=len(nodes)

    if node_count==0:
        node_count=3

    for i in range(node_count):

        pick=random.choice(options)

        votes[pick]+=1

    ranked=sorted(votes.items(),key=lambda x:x[1],reverse=True)

    return {

        "votes":votes,
        "winner":ranked[0][0]

    }
