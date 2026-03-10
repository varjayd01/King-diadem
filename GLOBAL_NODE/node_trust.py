node_trust = {}


def get_trust(node_id):

    return node_trust.get(node_id,0.5)


def update_trust(node_id, valid=True):

    score = node_trust.get(node_id,0.5)

    if valid:
        score += 0.05
    else:
        score -= 0.1

    score = max(0.0, min(1.0, score))

    node_trust[node_id] = score

    return score
