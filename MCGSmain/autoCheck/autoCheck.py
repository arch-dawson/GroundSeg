#!/usr/bin/Python

from subprocess import Popen, PIPE
import subprocess
import queue
import threading

class Checker:
    def __init__(self, parseQueue, dataFolder, mRFile):
        self.parseQueue = parseQueue
        self.dataFolder = dataFolder
        self.mRFile = mRFile

    def startCheck(self):
        self.check()

    def check(self):
        newFiles, err = Popen(["autoCheck/autoChecker.sh",'../'+self.dataFolder,self.mRFile], stdout=PIPE).communicate()
        for newFile in newFiles.decode('utf-8').split():
            self.parseQueue.put(self.dataFolder+newFile)
        threading.Timer(30.0,self.check).start()
        return 
    

def main(parseQueue, dataFolder, mRFile):
    # dataFolder has the form 'testFiles/'
    # mRfile can just be called 'mostRecent'
    autoCheck = Checker(parseQueue, dataFolder, mRFile)

    autoCheck.startCheck()
