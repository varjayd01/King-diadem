import time

REQUEST_LOG = {}

LIMIT = 30
WINDOW = 60

def allow_request(api_key):

    now=time.time()

    logs=REQUEST_LOG.get(api_key,[])

    logs=[t for t in logs if now-t<WINDOW]

    if len(logs)>=LIMIT:
        return False

    logs.append(now)

    REQUEST_LOG[api_key]=logs

    return True
