import binascii  # Used for converting hex string to hexadecimal

import openpyxl  # Used for reading/writing excel files

import datetime  # Used for creating the date stamp on the files

# --------------------------------------------------------
timeLocation = 2  # Where the system time is located in the excel file. Used to generate the time stamp.

# Min and max indices in the .xlsx file of the byte lengths
minIndex = 'F2'
maxIndex = 'F42'
# Could aim to make this system more general in the future.

xlsxFileName = 'BeaconDefinition.xlsx'

beaconFileName = 'fakeBeacon'

# --------------------------------------------------------

wb = openpyxl.load_workbook(xlsxFileName)  # Loads the beacon definition excel file

sheetList = wb.get_sheet_names()  # Loads in the names of the sheets.

sheet = wb.get_sheet_by_name(sheetList[0])  # As of 3/8/16 we only want the first sheet

f = open(beaconFileName)  # Opens the hex beacon file to be read in.

data = f.read()
f.close()
lengths = []

for rowOfCellObjects in sheet[minIndex:maxIndex]:  # Going through the row of values.
    for cellObj in rowOfCellObjects:  # Iterating through each cell of the row
        readVal = int(cellObj.value)
        lengths.append(readVal)  # Appends all the lengths read in from the excel file
"""
if (data[0:12] == 'allstarcosgc'):
    print "This is a Beacon!  We don't suck at file labelling!"
else:
    raise Exception('Not a beacon')
"""

total = 0  # Use this to keep track of where we are in the total number of bytes.

outVals = []

for length in lengths:
    chunk = data[total:(total+length-1)]
    total += length
    if chunk == 'allstarcosgc':
        outVals.append(chunk)
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

dateString = str(now.month) + "." + str(now.day) + "." + str(now.year)

fileName = dateString + "." + str(outVals[timeLocation])

# print fileName

