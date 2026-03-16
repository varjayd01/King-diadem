from collections import deque

chat_log=deque(maxlen=200)

def add_chat(user,message):

    chat_log.append({

        "user":user,
        "message":message

    })

def get_chat():

    return list(chat_log)
