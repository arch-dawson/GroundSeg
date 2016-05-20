#!/usr/bin/Python3

import threading
import queue

from autoCheck import autoCheck
from parsing import parsing

telemetryDef = "BeaconDefinition.xlsx"

parseQueue = queue.Queue()

autoCheck_args = (parseQueue,'../testFiles','mostRecent')
parsing_args = (telemetryDef, parseQueue)
# Looks like we're going to be using pymysql instead of mysqldb since the latter only works on python2

threads = [
    threading.Thread(name='autoCheck', target=autoCheck.main, args=autoCheck_args),
    threading.Thread(name='parsing', target=parsing.main, args=parsing_args),
]

# queue.get() will remove and return. Will wait if nothing available

for t in threads:
    t.daemon = True
    t.start()
while True:
    for t in threads:
        t.join(5)
