import serial, sys
import time
import random
import subprocess
from subprocess import Popen, PIPE
import re
import shlex

devRe = re.compile(r'/dev/pts/\d{1,3}')

out = Popen(shlex.split('socat -d -d pty,raw,echo=0 pty,raw,echo=0'),stdout=PIPE,stderr=PIPE)

# Write to first, read from second

ports = []

for line in iter(out.stderr.readline, ''):
    port = devRe.search(line.decode())
    if port:
        ports.append(port.group())
    if len(ports) == 2:
        break
    
print('Read from port {}'.format(ports[1]))

while True:
    print('Writing')
    Popen(shlex.split('echo {:x} > {}'.format(random.randrange(16**30),ports[0])),stdout=PIPE)
    time.sleep(3)

out.kill()
sys.exit(0)
