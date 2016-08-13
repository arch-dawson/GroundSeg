

import serial
import serial.tools.list_ports
import signal
import sys
import binascii
import time
import re
import tkinter as tk
import argparse
import queue
import threading
import random

# Can probably just get away with scanning lines for the 'allstarcosgc' header, low chance 1/(2**(12 * 8)) of same by chance

# IMPORTANT
# When running from MATLAB:
# command = 'start py -3 "C:\Users\Ground Comm\Documents\MATLAB\test.py"' // Change path to correct thing
# This will open the script in a new cmd.exe window and close it when done
# Really should specify the port for this unless you want pseudorandom garbage instead of beacons

class serialConn:
    def __init__(self, monitor, portStr, baudrate, hasp):
        """ ==== SERIAL INITIALIZATION ==== """
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate  #19200
        self.ser.timeout = 1
        
        self.fileStr = fileStr
        
        self.monitor = monitor
        
        self.readInQ = queue.Queue()

        self.cmdQ = queue.Queue()
        
        self.ser.port = portStr
        
        if hasp:
            self.hasp = hasp
            self.haspPre = b'\x01\x02'
            self.haspSuf = b'\x03\x0d\x0a'
        
        threading.Thread(target=self.readOne).start()
        
        threading.Thread(target=self.cmdCheck).start()
        
        try:
            self.ser.open()
        except:
            raise Exception("Failed to open port {}".format(portStr)) 
        
    def readOne(self):
        # Reads in one line, should be running all the time in a thread
        while True:
            line = self.ser.readline()
            if line:
                if self.monitor:
                    self.checkHeader(line)
                self.readInQ.put(line + '\n')
        return 
        
    def checkHeader(self, line): # Will check line for beacon header and call parser if true
        # Will need to add more control in readIn if beacons are more than one line
        # Any chance of having a different header and footer?  Even one character difference.
        # Need to consider chance of connecting halfway through beacon.
        # Add saving to SAMBA share, will need to timestamp in proper order.
        #TODO Add monitoring stuff
        return
        """This will be the end-- after isolating a beacon, write to Samba share. """
#        self.t = str(time.time())
#        with open('//ODIN/PolarCube/beacon_' + self.t,'w+') as beaconF: # NEED forward slashes here because Windows hates you
#            beaconF.write(line)
#        return

    def cmdCheck(self):
        while True:
            if not self.cmdQ.empty():
                self.cmdSend(cmdQ.get())
        return
        
    def cmdSend(self, cmd):   
        if cmd[:2] == "0x" or cmd[:2] == "\\x":
            bytes = bytearray.fromhex(cmd.replace('0x',''))
        else:
            bytes = cmd.encode()
        if self.hasp:
            bytes = self.haspPre + bytes + self.haspSuf
        self.ser.write(bytes)
        return

class fakeConn:
    def __init__(self, monitor, port, baudrate, hasp):
        self.readInQ = queue.Queue()

        self.cmdQ = queue.Queue()
        
        if hasp:
            self.hasp = hasp
            self.haspPre = b'\x01\x02'
            self.haspSuf = b'\x03\x0d\x0a'
        
        threading.Thread(target=self.readOne).start()
        
        threading.Thread(target=self.cmdCheck).start()
        
    def readOne(self):
        while True:
            self.readInQ.put(('{:x}'.format(random.randrange(16**30))).encode())
            time.sleep(1)
        return 
        
    def cmdCheck(self):
        while True:
            if not self.cmdQ.empty():
                self.cmdSend(self.cmdQ.get())
        return
        
    def cmdSend(self, cmd):   
        if cmd[:2] == "0x" or cmd[:2] == "\\x":
            bytes = bytearray.fromhex(cmd.replace('0x',''))
        else:
            bytes = cmd.encode()
        if self.hasp:
            bytes = self.haspPre + bytes + self.haspSuf
        return bytes
         

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process data coming in from TNC. Options to analyze or display.') 
    parser.add_argument('-monitor', action="store_true", default=False) # Monitor for beacons
    parser.add_argument('-file', action="store", dest="fileStr", type=str, default=str(time.time())) # File specification
    parser.add_argument('-port', action="store", dest='port', type=str, help='COM port of serial connection, ex: COM3') # Specify port
    parser.add_argument('-b','--baud', action="store", dest='baudrate', type=str, help='Specify baudrate', default=19200)
    parser.add_argument('-hasp',action="store_true", default=False)
    args = parser.parse_args()

    # conn = serialConn(args.monitor, args.fileStr, args.port, args.baudrate)
    conn = fakeConn(args.monitor, args.fileStr, args.port, args.baudrate, args.hasp)
    
    root = tk.Tk()
    app = App(conn, master=root)
    app.master.title("Colorado Space Grant Consortium Serial Terminal")
    app.mainloop()
