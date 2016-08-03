import threading
import subprocess
from subprocess import Popen, PIPE
import shlex

cmdString = './autoGen.sh /home/dawson/SpaceGrant/GroundSeg/MCGSmain/fakeBeaconGen'

def generate():
    Popen(shlex.split(cmdString))
    threading.Timer(15.0, generate).start()


threading.Timer(15.0, generate).start()
