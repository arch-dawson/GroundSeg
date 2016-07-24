#!/usr/bin/env python3
# RUN WITH SUDO FOR I/O PERMISSIONS
# CHANGE PERMISSIONS ON PORTS? 

import serial
import serial.tools.list_ports
import signal
import sys
import binascii
import time
import re
import openpyxl
from openpyxl import Workbook
import argparse

# Can probably just get away with scanning lines for the 'allstarcosgc' header, low chance 1/(2**(12 * 8)) of same by chance

# -monitor mode: Scan for beacon, parse if received
# -Display mode: Display incoming data
# -File Specification: Specify file to be saved into

# IMPORTANT
# When running from MATLAB:
# command = 'start py -3 "C:\Users\Ground Comm\Documents\MATLAB\test.py"' // Change path to correct thing
# This will open the script in a new cmd.exe window and close it when done
# Really should specify the port for this unless you want pseudorandom garbage instead of beacons


class serialConn:
    def __init__(self, monitor, disp, fileStr, portStr):
        self.ser = serial.Serial()
        self.ser.baudrate = 19200 
        self.ser.timeout = 1
        
        self.monitor = monitor
        
        self.disp = disp

        if not portStr:
            ports = list(serial.tools.list_ports.comports()) # List serial com ports
            
            for port in ports:
                try:
                    self.ser.port = str(port).split()[0]
                    self.ser.open()
                    break # If it gets to here without throwing exception, we're fine
                except:
                    print('Port {} failed to open.'.format(str(port).split()[0]))
                    self.ser.port = ''
            if not self.ser.port:
                self.ser.port = '/dev/ttyUSB0' # Default is what works on most linux machines
                self.ser.open()
        else:
            self.ser.port = portStr
            try:
                self.ser.open()
            except:
                raise Exception("Failed to open port {}".format(portStr))

        self.t = str(time.time())
            
        if fileStr == None: # Default file name if not specified
            fileStr = self.t 
        
        self.outFile = 'Polarcube_' + fileStr + '.txt'

        signal.signal(signal.SIGINT, self.sig_handler) # Installs sig_handler as handler of SIGINT (CTRL + C)

        if self.disp:
            self.readIn()
            

    def sig_handler(self, *signals):
        self.shutdown()


    def shutdown(self):
        str = self.ser.readline()
        with open(self.outFile) as f:
            while len(str) > 0:
                f.write(str.decode(encoding='latin-1',errors='replace'))
                f.write('\n')
                str = self.ser.readline()
        sys.exit(0)
        return

    def readIn(self):
        # Defines number of lines to read in
        with open(self.outFile, 'w+') as f:
            while True:
                line = self.ser.readline()
                print(line)
                f.write(line.decode(encoding='latin-1',errors='replace'))
                f.write('\n')
                if self.monitor:
                    checkHeader(line)
        return
        
    def headerCheck(self, line): # Will check line for beacon header and call parser if true
        # Will need to add more control in readIn if beacons are more than one line
        # Any chance of having a different header and footer?  Even one character difference.
        # Need to consider chance of connecting halfway through beacon.
        # Add saving to SAMBA share, will need to timestamp in proper order.
        self.t = str(time.time())
        with open('//ODIN/PolarCube/beacon_' + self.t,'w+') as beaconF: # NEED forward slashes here because Windows hates you
            beaconF.write(line)
        return 
        
    def cmdEntry(self,cmd):
        userIn = cmd
        cmdString = 'Please enter a command: '
        if not len(cmd) > 0:
            userIn = input(cmdString)
        bytes = userIn.split()
        cmd = bytearray.fromhex(bytes)
        print(cmd)
        self.ser.write(cmd)
        return
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process data coming in from TNC. Options to analyze or display.') 
    parser.add_argument('-monitor', action="store_true", default=False) # Monitor for beacons
    parser.add_argument('-disp', action="store_true", default=True) # Display
    parser.add_argument('-file', action="store", dest="fileStr", type=str) # File specification
    parser.add_argument('-port', action="store", dest='port', type=str, help='COM port of serial connection, ex: COM3') # Specify port
    args = parser.parse_args()

    
    conn = serialConn(args.monitor, args.disp, args.fileStr, args.port)
