#!/usr/bin/env python3
# RUN WITH SUDO FOR I/O PERMISSIONS
# CHANGE PERMISSIONS ON PORTS

# Written by Dawson Beatty Summer 2016 for use by Colorado Space Grant Consortium
# Questions? Gripes? Email me at dawson.beatty@colorado.edu or dawson.beatty@gmail.com 

import serial
import serial.tools.list_ports
import sys
import tkinter as tk
from tkinter import filedialog
from serialConn import *
import threading

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        # What was entered in the command box
        self.command = tk.StringVar()
        self.command.set('Enter a Command')
        
        self.portChoice = tk.StringVar()
        self.portChoice.set('Select Port')

        # Making scrollbar so display window is scrollable
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row=1,column=1)
        
        # Create option box for ports
        self.getPorts()
        self.refresh = tk.Button(self, text="Refresh Ports",command=self.getPorts)
        self.refresh.grid(row=4,column=0,sticky=tk.W)
        
        # Open port button
        self.portOpen = tk.Button(self, text="Open Port",bg='red',command=self.openPort)
        self.portOpen.grid(row=5,column=0,sticky=tk.W)
        
        # Make the listbox which displays all the incoming data
        self.listbox = tk.Listbox(self,bg='gray',fg='black')
        self.listbox.grid(row=1,column=0,columnspan=3)
        self.listbox['height'] = 35
        self.listbox['width'] = 80
        
        # Binding scrollbar to listbox
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
       
        # Creating box for user to enter command 
        self.commandBox = tk.Entry()
        self.commandBox.grid(row=2,column=0)
        self.commandBox['textvariable'] = self.command
        
        # Monitoring for beacons
        self.monitor = False # Temporary
        
        # HASP mode for adding header and footer
        self.hasp = False
        
        self.baudChoice = tk.IntVar()
        baudChoices = [1200, 2400, 4800, 19200, 38400, 57600, 115200]
        self.baudOption = tk.OptionMenu(self, self.baudChoice, *baudChoices)
        self.baudOption.grid(row=2,column=0,sticky=tk.W)
    
        # Making quit Buttons
        self.quitNS = tk.Button(self, text="Quit without saving", width=20, command=self.shutdownNS)
        self.quitNS.grid(row=2,column=1)
        self.quit = tk.Button(self, text="QUIT", fg="red",width=20,
                              command=self.shutdown)
        self.quit.grid(row=3,column=1)
        
    def serialRead(self, *args):
        # Read in a line from self.conn 
        print('\n') # This is needed for some reason. (???) 
        while True:
            if not self.conn.readInQ.empty():
                self.listbox.insert(tk.END, self.conn.readInQ.get())
            self.listbox.yview(tk.END)
        return
        
    def openPort(self):
        if not self.baudChoice.get():
            self.baudOption.config(bg='red')
            return
        else:
            self.baudOption.config(bg='light grey')
        if not self.portChoice.get():
            self.portOption.config(bg='red')
            return
        else:
            self.portOption.config(bg='light grey')
        self.conn = fakeConn(self.monitor, self.portChoice.get(), self.baudChoice.get(), self.hasp)
        self.portOpen.config(bg="green",text="Port Open")
        threading.Thread(target=self.serialRead,daemon=True).start()
        
    def getPorts(self):
        ports = list(serial.tools.list_ports.comports()) # List serial com ports
        
        out = [None,]
        
        for port in ports:
            out.append(str(port).split()[0])
            
        self.portOption = tk.OptionMenu(self,self.portChoice,*out)
        self.portOption.grid(row=3,column=0,sticky=tk.W)
        
        return
        
    def shutdown(self):
        # Copies and saves all data from the current session 
        filename = filedialog.asksaveasfilename(initialfile=str(time.time()),parent=root)
        
        data = self.listbox.get(0,tk.END)
        
        if filename:
            with open(filename,'w+') as f:
                for line in data:
                    f.write(line.decode(encoding='latin-1',errors='replace'))
                    f.write('\n')
        root.destroy()
        sys.exit(0)
        return
        
    def shutdownNS(self):
        # Quit without saving
        root.destroy()
        sys.exit(0)
        return
        

if __name__ == '__main__':
#    parser = argparse.ArgumentParser(description='Process data coming in from TNC. Options to analyze or display.') 
#    parser.add_argument('-monitor', action="store_true", default=False) # Monitor for beacons
#    parser.add_argument('-file', action="store", dest="fileStr", type=str, default=str(time.time())) # File specification
#    parser.add_argument('-port', action="store", dest='port', type=str, help='COM port of serial connection, ex: COM3') # Specify port
#    parser.add_argument('-b','--baud', action="store", dest='baudrate', type=str, help='Specify baudrate', default=19200)
#    parser.add_argument('-hasp',action="store_true", default=False)
#    args = parser.parse_args()

    # conn = serialConn(args.monitor, args.fileStr, args.port, args.baudrate)
#    conn = fakeConn(args.monitor, args.fileStr, args.port, args.baudrate, args.hasp)
    
    root = tk.Tk()
    #app = App(conn, master=root)
    app = App(master=root)
    app.master.title("Colorado Space Grant Consortium Serial Terminal")
    app.mainloop()
