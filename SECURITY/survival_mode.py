import time

traffic=[]

WINDOW=10

LIMIT=200

def survival_check():

    now=time.time()

    traffic.append(now)

    while traffic and now-traffic[0]>WINDOW:

        traffic.pop(0)

    if len(traffic)>LIMIT:

        return "throttle"

    return "ok"
