#!/usr/bin/Python3

import threading
import queue

from autoCheck import autoCheck
from parsing import parsing
from database import database
from uftp import uftp

# ==== DEFINING STUFF ====
# Change database soon
telemetryDef = "BeaconDefinition.xlsx"
dbName = 'fakeSatellite' # Change before launch.  Duh.
tableName = 'fakeTelemetry' # Be kinda funny if you didn't change this
path = '/home/dev/PolarCube/beacons'
mostRecentFile = '/home/dev/PolarCube/mostRecent' 

# ==== AUTO GEN FAKE BEACONS (TEMPORARY) ====
# Autogen fake stuff
# Only for testing all code
# Should remove soonish
from subprocess import Popen, PIPE
import random
def autoGen():
    Popen(["fakeBeaconGen/autoGen.sh"])
    threading.Timer(float(random.randint(10,20)),autoGen).start()
    return

# ==== MAKING THE QUEUES ====
# Queues are for the threads
# Global synchronization
# Called from anywhere
parseQueue = queue.Queue()
databaseQueue = queue.Queue()

# ==== DEFINING ARGUMENTS TO EACH THREAD ====
autoCheck_args = (parseQueue,mostRecentFile,path)
parsing_args = (telemetryDef, parseQueue, databaseQueue)
database_args = (databaseQueue, dbName, tableName, telemetryDef)
uftp_args = (parseQueue,beaconFolder)

# ==== CREATING THE THREADS ====
threads = [
    threading.Thread(name='autoCheck', target=autoCheck.main, args=autoCheck_args),
    threading.Thread(name='parsing', target=parsing.main, args=parsing_args),
#    threading.Thread(name='database',target=database.main, args=database_args),
#    threading.Thread(name='uftp',target=uftp.main, args=uftp_args),
]

# queue.get() will remove and return. Will wait if nothing available

for t in threads:
    t.daemon = True
    t.start()
while True:
    for t in threads:
        t.join(5)
