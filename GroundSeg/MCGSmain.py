#!/usr/bin/Python3

import threading
import queue

from autoCheck import autoCheck
from parsing import parsing
from database import database

# ==== DEFINING STUFF ====
telemetryDef = "BeaconDefinition.xlsx"
dbName = 'fakeSatellite' # Change before launch.  Duh.
tableName = 'fakeTelemetry' # Be kinda funny if you didn't change this
beaconFolder = 'testFiles/'
mostRecentFile = 'mostRecent' # Possibly the most useless declaration

# ==== MAKING THE QUEUES ==== 
parseQueue = queue.Queue()
databaseQueue = queue.Queue()

# ==== DEFINING ARGUMENTS TO EACH THREAD ====
autoCheck_args = (parseQueue,beaconFolder,mostRecentFile)
parsing_args = (telemetryDef, parseQueue, databaseQueue)
database_args = (databaseQueue, dbName, tableName, telemetryDef)

# ==== CREATING THE THREADS ==== 
threads = [
    threading.Thread(name='autoCheck', target=autoCheck.main, args=autoCheck_args),
    threading.Thread(name='parsing', target=parsing.main, args=parsing_args),
    threading.Thread(name='database',target=database.main, args=database_args),
]

# queue.get() will remove and return. Will wait if nothing available

for t in threads:
    t.daemon = True
    t.start()
while True:
    for t in threads:
        t.join(5)
