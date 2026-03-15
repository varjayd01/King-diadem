import threading
import time

feed = []

lock = threading.Lock()


def add_feed_entry(api_key, decision):

    entry = {
        "time": time.time(),
        "decision": decision
    }

    with lock:
        feed.append(entry)

        # จำกัด feed ไม่ให้ใหญ่เกิน
        if len(feed) > 1000:
            feed.pop(0)


def get_feed():

    with lock:
        return list(feed[-50:])
