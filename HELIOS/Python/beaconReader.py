import binascii

import openpyxl

import datetime

timeLocation = 2  # Where the system time is located in the excel file.

# Min and max indices in the .xlsx file of the byte lengths
minIndex = 'F2'
maxIndex = 'F42'

wb = openpyxl.load_workbook('BeaconDefinition.xlsx')

sheetList = wb.get_sheet_names()  # Loads in the names of the sheets.

sheet = wb.get_sheet_by_name(sheetList[0])

f = open('fakeBeacon')

data = f.read()

f.close()

lengths = []

for rowOfCellObjects in sheet[minIndex:maxIndex]:  # Going through the row of values.
    for cellObj in rowOfCellObjects:  # Iterating through each cell of the row
        readVal = int(cellObj.value)
        lengths.append(readVal)  # Appends all the lengths read in from the
"""
if (data[0:12] == 'allstarcosgc'):
    print "This is a Beacon!  Mild success!"
else:
    raise Exception('Not a beacon')
"""

total = 0  # Use this to keep track of where we are in the total number of bytes.

outVals = []

print data[136:148]

for length in lengths:
    chunk = data[total:(total+length-1)]
    print str(total) + ":" + str(total+length-1)
    total += length
    if chunk == 'allstarcosgc':
        outVals.append(chunk)
        print 'woot'
        continue
    else:
        hexVal = binascii.hexlify(chunk)
        decVal = int(hexVal, 16)
        outVals.append(decVal)
        print decVal

"""
    If we were worried about partial bytes, right here we would read everything into a string of binary
    This is all in distinct bytes though, so we can parse it normally.
    That would look like:
    binary = bin(decVal)
    <3  Past Dawson
"""

now = datetime.datetime.now()

datestring = str(now.month) + "." + str(now.day) + "." + str(now.year)

#fileName = datestring + "." + outVals[timeLocation]

#print fileName

"""
THEORY
Strongly suspect that random values aren't necessarily the number of bytes they're supposed to be, especially if it was
randomly a small number in the range.  We may have to find some way of padding out? Or go back to the old plan of dumping
everything into binary. 
"""