from subprocess import Popen, PIPE
import shlex

class uftpConnection:
    def __init__(self,parseQueue,beaconFolder):
        self.parseQueue = parseQueue
        self.beaconFolder = beaconFolder

        self.initClnt()
        

    def initServ(self):
        pass

    def initClnt(self):
        path, err = Popen("pwd", stdout=PIPE).communicate()
        clnt_cmd = "uftpd -D " + path.decode('utf-8').rstrip() + '/' + self.beaconFolder
        Popen(shlex.split("sudo killall -9 uftpd"))
        Popen(shlex.split(clnt_cmd))
        # The above system is awful.
        # Can only have one instance of uftpd running
        # Future Dawson will hopefully fix this
        return


def main(parseQueue,beaconFolder):
    uftpConn = uftpConnection(parseQueue,beaconFolder)
