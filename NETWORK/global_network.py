from collections import deque

global_chat=deque(maxlen=200)

def add_message(user,text):

    global_chat.append({

        "user":user,

        "message":text

    })

def get_messages():

    return list(global_chat)
