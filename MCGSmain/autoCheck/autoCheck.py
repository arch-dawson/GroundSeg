#!/usr/bin/Python

from subprocess import Popen, PIPE
import subprocess
import queue
import threading

def check(parseQueue, mRFile, path):
    newFiles, err = Popen(["/home/dev/GroundSeg/MCGSmain/autoCheck/autoChecker.sh",path, mRFile], stdout=PIPE).communicate()
    for newFile in newFiles.decode('utf-8').split():
        parseQueue.put(path+newFile)
        print("Adding file to parse Queue: {}".format(path+newFile))
    threading.Timer(30.0,check,args=(parseQueue, mRFile, path)) 
    return

def main(parseQueue,  mRFile, path):
    # path is absolute path to beacons folder
    # mRfile should be absolute path as well

    check(parseQueue, mRFile, path)


