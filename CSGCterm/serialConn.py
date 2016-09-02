

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
import math

# Can probably just get away with scanning lines for the 'allstarcosgc' header, low chance 1/(2**(12 * 8)) of same by chance

# IMPORTANT
# When running from MATLAB:
# command = 'start py -3 "C:\Users\Ground Comm\Documents\MATLAB\test.py"' // Change path to correct thing
# This will open the script in a new cmd.exe window and close it when done
# Really should specify the port for this unless you want pseudorandom garbage instead of beacons

class serialConn:
    def __init__(self, monitor, fileStr, portStr, baudrate, hasp):
        """ ==== SERIAL INITIALIZATION ==== """
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate  
        self.ser.timeout = 1

        self.logFile = 'beaconLog.log'
        
        self.fileStr = fileStr

        self.readingBeacon = False # To keep track of when checkHeader is looking for beacons. Needed if beacon >1 line. 
        self.monitor = monitor
        
        self.readInQ = queue.Queue()

        self.cmdQ = queue.Queue()
        
        self.ser.port = portStr

        self.header = b'616c6c73746172636f736763' # Remove b if string readin

        self.footer = b'' # DEFINE FOOTER HERE

        # Header and footer can be arbitrary, just made header and footer different in beacon definition

        self.headLength = len(self.header) # Need to use this alot, won't change

        self.footLength = len(self.footer)
        
        if hasp:
            self.hasp = hasp
            self.haspPre = b'\x01\x02'
            self.haspSuf = b'\x03\x0d\x0a'

        try:
            self.ser.open()
        except:
            raise Exception("Failed to open port {}".format(portStr)) 
        
        threading.Thread(target=self.readOne).start()
        
        threading.Thread(target=self.cmdCheck).start()
        
        
    def readOne(self):
        # Reads in one line, should be running all the time in a thread
        while True:
            line = self.ser.readline()
            if line:
                if self.monitor:
                    self.checkBeacon(line)
                self.readInQ.put(line + '\n')
        return 
        
    def checkBeacon(self, line): # Will check line for beacon header and send to Samba when read in

    # Adding old line to line if necessary
    line = self.previous + line
    
    # Vectors in indices for occurences of headers and footers
    headers = [m.start() for m in re.finditer(self.header, line)]

    if self.previous: # If carrying over, don't want to count the first one
        del(headers[0])

    footers = [n.start() for n in re.finditer(self.footer, line)]

    while len(footers) + len(headers) > 0:
        try:
            head = headers[0]
        except:
            head = math.inf
        try:
            foot = footers[0]
        except:
            foot = math.inf
        if head < foot: # Header occurs before footer
            if self.readingBeacon: # If we're in the process of reading a beacon
                self.log('Beacon Error: Expecting Footer')
            self.headIndex = headers[0]
            del(headers[0])
            self.readingBeacon = True
        else:
            if self.readingBeacon:
                self.footIndex = footers[0]
                del(footers[0])
                self.beacon = line[self.headIndex:self.footIndex+self.footLength]
                self.saveBeacon()
                self.readingBeacon = False
            else:
                self.log('Beacon Error: Expecting Header')
                del(footers[0])

    if self.readingBeacon: # Storing for the next set 
        self.previous = line[self.headIndex:]
        self.headIndex = 0
    else:
        self.previous = ''

    def log(self, message):
        with open(self.logFile,'w+') as f:
            f.write('[*] {}: {}\n'.format(str(time.time()),message))
        return


    def saveBeacon(self):
        self.t = str(time.time())
        fName = '//ODIN/PolarCube/beacon_' + self.t # NEED forward slashes here because Windows hates you
        with open(fName,'w+') as beaconF: 
            beaconF.write(self.beacon)
        self.log('Saved beacon {}'.format(fName))
        return

    def headCheck(self, line): # Checks if the start of a beacon is in given line
        # Inputs: Line
        # Outputs: Line after header
        index = line.find(self.header)

        if index > 0:
            return (True, line[index+self.headLength:])
        else:
            return line

    def footCheck(self, line): # Checks if the end of a beacon is in the given line
        # Inputs: Line read in over TNC. INCLUDE earlier parts of beacon including header
        # Outputs: Tuple with  line up to and including footer, and the rest of the line. Just line if no header found

        index = line.find(self.footer)

        if index > 0:
            return (line[0:index+self.footLength],line[index+self.footLength:])
        else:
            return ('', line)
            

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
