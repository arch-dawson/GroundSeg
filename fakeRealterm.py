#!/usr/bin/env python3
# RUN WITH SUDO
# CHANGE PERMISSIONS ON PORTS

import serial
import serial.tools.list_ports
import signal
import sys
import binascii
import time
import sys
import re
from zlib import adler32
import openpyxl
from openpyxl import Workbook
import argparse

# Can probably just get away with scanning lines for the 'allstarcosgc' header, low chance 1/(2**(12 * 8)) of same by chance

# -monitor mode: Scan for beacon, parse if received
# -Display mode: Display incoming data
# -File Specification: Specify file to be saved into


class serialConn:
    def __init__(self, monitor, disp, fileStr):
        self.ser = serial.Serial()
        self.ser.baudrate = 19200 # 4800
        self.ser.timeout = 1
        
        self.monitor = monitor
        
        self.disp = disp
        
        ports = list(serial.tools.list_ports.comports()) # List serial com ports
        
        for port in ports:
            try:
                self.ser.port = port
                self.ser.open()
                break # If it gets to here without throwing exception, we're fine
            except:
                print('Port {} failed to open.'.format(port))
                self.ser.port = ''
        if not self.ser.port:
            self.ser.port = '/dev/ttyUSB0' # Default is what works on most linux machines
            self.ser.open()
            
        if fileStr == None:
            fileStr = str(time.time())
        
        self.outFile = fileStr+'.txt'

        signal.signal(signal.SIGINT, self.sig_handler) # Installs sig_handler as handler of SIGINT (CTRL + C)
        return

    def sig_handler(self, *signals):
        self.shutdown()

    def shutdown(self):
        str = self.ser.readline()
        while len(str) > 0:
            self.dataFile.write(str.decode(encoding='latin-1',errors='replace'))
            self.dataFile.write('\n')
            str = self.ser.readline()
        self.dataFile.close()
        dataAnly.parse(self.dataFile,self.outFile)
        sys.exit(0)
        return

    def readIn(self):
        # Defines number of lines to read in
        with open(self.outFile) as f:
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
    parser.add_argument('-disp', action="store_true", default=False) # Display
    parser.add_argument('-file', action="store", dest="fileStr", type=str) # File specification   
    args = parser.parse_args()
    
    #conn = serialConn(args.monitor, args.disp, args.fileStr)
    print(args.fileStr)
    #conn = serialConn()
