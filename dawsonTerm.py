#!/usr/bin/env python3
# RUN WITH SUDO FOR I/O PERMISSIONS
# CHANGE PERMISSIONS ON PORTS

# Written by Dawson Beatty Summer 2016 for use by Colorado Space Grant Consortium
# Questions? Gripes? Email me at dawson.beatty@colorado.edu or dawson.beatty@gmail.com 

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

# -monitor mode: Scan for beacon, parse if received
# -File Specification: Specify file to be saved into
# -port: Specify port to connect to 
# -hasp: Adds header and footer to make the HASP people happy 

# IMPORTANT
# When running from MATLAB:
# command = 'start py -3 "C:\Users\Ground Comm\Documents\MATLAB\test.py"' // Change path to correct thing
# This will open the script in a new cmd.exe window and close it when done
# Really should specify the port for this unless you want pseudorandom garbage instead of beacons


class App(tk.Frame):
    def __init__(self, serialConn, master=None):
        super().__init__(master)
        self.grid()
        self.create_widgets()
        self.conn = serialConn
        
        # Enabling up/down key to view command history
        self.cmdHist = []
        self.cmdHistCounter = -1
        

    def create_widgets(self):
        # What was entered in the command box
        self.command = tk.StringVar()
        self.command.set('Enter a Command')

        # Making scrollbar so display window is scrollable
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row=1,column=1)
        
        # Make the listbox which displays all the incoming data
        self.listbox = tk.Listbox(self,bg='gray',fg='black')
        self.listbox.grid(row=1,column=0)
        self.listbox['height'] = 40
        self.listbox['width'] = 80
        
        # Binding scrollbar to listbox
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
       
        # Creating box for user to enter command 
        self.commandBox = tk.Entry()
        self.commandBox.grid(row=2,column=0)
        self.commandBox['textvariable'] = self.command
        
        # Binding <enter> key to sending command
        self.commandBox.bind('<Key-Return>', self.sendCmd)
        self.commandBox.bind('<Button-1>', self.clearEntry)
        self.commandBox.bind('<Up>', self.cmdHistUp)
        self.commandBox.bind('<Down>', self.cmdHistDown)
    
        # Making quit Button 
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.shutdown)
        self.quit.grid(row=3,column=0)
        
        threading.Thread(target=self.serialRead).start()
        
    def clearEntry(self, *args):
    	self.command.set('')
    	
    def cmdHistUp(self, *args):
    	if len(self.cmdHist) >= abs(self.cmdHistCounter):
    		self.command.set(self.cmdHist[self.cmdHistCounter])
    		self.cmdHistCounter -= 1
    	else:
    	    self.cmdHistCounter = -len(self.cmdHist)
    	return
    	
    def cmdHistDown(self, *args):
        print(self.cmdHistCounter)
        if self.cmdHistCounter >= 0:
            self.cmdHistCounter = -1
            self.command.set('')
        else:
            self.command.set(self.cmdHist[self.cmdHistCounter])
            self.cmdHistCounter += 1
           
    def sendCmd(self, *args):
        # Gets command from strVar when user pushes <enter>
        cmd = self.commandBox.get()
        if len(cmd) > 0:
            self.listbox.insert(tk.END, cmd)
            self.conn.cmdQ.put(cmd)
            self.listbox.itemconfig(self.listbox.size()-1,fg='blue')
            self.cmdHistCounter = -1
            self.cmdHist.append(cmd)
        self.listbox.yview(tk.END)
        self.clearEntry()
        #self.command.set('')
        return
        
    def serialRead(self, *args):
        # Read in a line from self.conn 
        print('\n') # This is needed for some reason. (???) 
        while True:
            if not self.conn.readInQ.empty():
                self.listbox.insert(tk.END, self.conn.readInQ.get())
            self.listbox.yview(tk.END)
        return
        
    def shutdown(self, *args):
        # Copies and saves all data from the current session 
        data = self.listbox.get(0,tk.END)
        with open(self.conn.fileStr) as f:
            for line in data:
                f.write(line.decode(encoding='latin-1',errors='replace'))
                f.write('\n')
        root.destroy()
        sys.exit(0)


class serialConn:
    def __init__(self, monitor, fileStr, portStr, baudrate, hasp):
        """ ==== SERIAL INITIALIZATION ==== """
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate  #19200
        self.ser.timeout = 1
        
        self.fileStr = fileStr
        
        self.monitor = monitor
        
        self.readInQ = queue.Queue()

        self.cmdQ = queue.Queue()
        
        if hasp:
            self.hasp = hasp
            self.haspPre = b'\x01\x02'
            self.haspSuf = b'\x03\x0d\x0a'

        # TODO: Add GUI thing for selection, options can come from list_ports
        
        threading.Thread(target=self.readOne).start()
        
        threading.Thread(target=self.cmdCheck).start()
        
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
        
        self.outFile = 'Polarcube_' + fileStr + '.txt'
        
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
        return bytes

class fakeConn:
    def __init__(self, monitor, fileStr, port, baudrate, hasp):
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
            self.readInQ.put('{:x}'.format(random.randrange(16**30)))
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
