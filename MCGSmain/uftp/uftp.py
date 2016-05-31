from subprocess import Popen, PIPE
import shlex

class uftpConnection:
    def __init__(self,parseQueue,beaconFolder):
        self.parseQueue = parseQueue
        self.beaconFolder = beaconFolder

        self.initClnt()
        

    def initServ(self):
        # Add -f and -F options
        # Could just do a search to see if file exists?
        # Could send really big file then close connection halfway through
        # -i file_list.  Seperate files to be sent, one per line.
        # USE FULL FILEPATH FOR ABOVE
        # -C tfmcc to dynamically determine transmission rate
        # AES-256-CBC, SHA-1 hashing, autogen 512-bit RSA key:
        # uftp -Y aes256-cbc -h sha1 [-k keyfile]
        # -L logfile
        # -S status_file for human-readable
        # -g max_log_size (1-1024) MB
        #  -n max_log_size (1-1000)
        # Max combo of the two above will allow for more than 1TB of log files
        # -m max_nak_count (1-10) probably change this if having lotsa naks
        # -x Should we want to change detail in logs. (1-5), 5 has the most.
        # Default for -x is 2
        # -s robustness (10-50), default 20. number of times sending waiting for client
        # -t time-to-live
        # -r init_grtt[:min_grtt:max_grtt] CHANGE IF SENDING FAILS 
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
