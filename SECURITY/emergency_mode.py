import time

ip_table={}

LIMIT=5

WINDOW=3600

def check_emergency(ip):

    now=time.time()

    if ip not in ip_table:

        ip_table[ip]=[now,1]

        return True

    start,count=ip_table[ip]

    if now-start>WINDOW:

        ip_table[ip]=[now,1]

        return True

    if count>=LIMIT:

        return False

    ip_table[ip][1]+=1

    return True
