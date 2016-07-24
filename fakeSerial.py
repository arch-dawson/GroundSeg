import os, pty, serial
import time

master, slave = pty.openpty()

sName = os.ttyname(slave)

ser = serial.Serial(sName, 4800)

ser.timeout = 1

print(sName)

print(os.ttyname(master))

while True:
    time.sleep(3)
    ser.write(b'testing')
