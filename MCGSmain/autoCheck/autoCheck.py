#!/usr/bin/Python

from subprocess import Popen, PIPE
import subprocess
import queue
import threading

def check(parseQueue, mRFile, path):
    newFiles, err = Popen(["autoCheck/autoChecker.sh",path, mRFile], stdout=PIPE).communicate()
    for newFile in newFiles.decode('utf-8').split():
        parseQueue.put(path+newFile)
    threading.Timer(30.0,check,args=(parseQueue, dataFolder, mRFile, path)         
    

def main(parseQueue,  mRFile, path):
    # path is absolute path to beacons folder
    # mRfile should be absolute path as well

    check()
