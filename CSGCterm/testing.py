import re
import math

def checkBeacon(line): # Will check line for beacon header and send to Samba when read in

    header = 'head'

    footer = 'foot'

    footLength = len(footer)

    global readingBeacon

    global previous

    global headIndex

    # Adding old line to line if necessary
    line = previous + line

    # Vectors in indices for occurences of headers and footers
    headers = [m.start() for m in re.finditer(header, line)]

    footers = [n.start() for n in re.finditer(footer, line)]

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
            if readingBeacon: # If we're in the process of reading a beacon
                print('Beacon Error: Expecting Footer')
            headIndex = headers[0]
            del(headers[0])
            readingBeacon = True
        else:
            if readingBeacon:
                footIndex = footers[0]
                del(footers[0])
                beacon = line[headIndex:footIndex+footLength]
                print('Beacon: {}'.format(beacon))
                readingBeacon = False
            else:
                print('Beacon Error: Expecting header')
                del(footers[0])

    if readingBeacon: # Storing for the next set 
        previous = line[headIndex:]
        headIndex = 0
    else:
        previous = ''


readingBeacon = False
previous = ''
headIndex = 0

checkBeacon('adlkfj ldf foot afgsfdg dkfl j head afg sfgs')
checkBeacon('sfgjksfhgj foot adflkajdlk head  dalkfjladjkfjajd foot  adjkfhakdjf ')
