#!/usr/bin/Python

from subprocess import Popen, PIPE
import subprocess
import queue

def main(parseQueue, dataFolder, mRFile):
    # dataFolder has the form 'testFiles/'
    # mRfile can just be called 'mostRecent'
    
    newFiles, err = Popen(["autoCheck/autoChecker.sh",'../'+dataFolder,mRFile], stdout=PIPE).communicate()
    for newFile in newFiles.decode('utf-8').split():
        parseQueue.put(dataFolder+newFile)

    # ADD TIMER STUFF HERE
