#!/usr/bin/Python3

import threading
import queue

from autoCheck import autoCheck

parseQueue = queue.Queue()

autoCheck_args = (parseQueue,'../testFiles','mostRecent')

threads = [
    threading.Thread(name='autoCheck', target=autoCheck.main, args=autoCheck_args),
]

# queue.get() will remove and return. Will wait if nothing available

for t in threads:
    t.daemon = True
    t.start()
while True:
    for t in threads:
        t.join(5)