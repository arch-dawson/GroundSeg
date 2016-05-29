

from subprocess import Popen, PIPE
import random
def autoGen():
    Popen(["fakeBeaconGen/autoGen.sh"])
    threading.Timer(float(random.randint(10,20)),autoGen).start()
    return

autoGen()
