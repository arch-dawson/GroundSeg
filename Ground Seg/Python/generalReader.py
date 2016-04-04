import binascii  # Used for converting hex string to hexadecimal

import openpyxl  # Used for reading/writing excel files

import math  # Need to use log2 for conversions

# import datetime  # Used for creating the date stamp on the files


# ====== CHANGE THIS BIT ======

# SUB IN YOUR FILE NAME HERE WHERE THE BYTE LENGTHS ARE
xlsxFileName = 'BeaconDefinition.xlsx'

# INSERT THE MIN AND MAX OF INDICES WHERE THE BYTE LENGTHS ARE
minIndex = 'F2'
maxIndex = 'F42'

# CHANGE THE NAME OF THE FILE YOU WANT TO PARSE
parseFileName = 'fakeBeacon'

# timeLocation = 2  # Where the system time is located in the excel file. Used to generate the time stamp.

# --------------------------------------------------------

wb = openpyxl.load_workbook(xlsxFileName)  # Loads the beacon definition excel file

sheetList = wb.get_sheet_names()  # Loads in the names of the sheets.

sheet = wb.get_sheet_by_name(sheetList[0])  # As of 3/8/16 we only want the first sheet

f = open(parseFileName)  # Opens the hex beacon file to be read in.

data = f.read()
f.close()


# Pass only the raw data w/o header/footer?  Could remove some if statements
def beaconReader(beaconData, beaconSheet):
    beacLengths = []
    for beaconRow in beaconSheet[minIndex:maxIndex]:  # Going through the row of values.
        for cellBeacObj in beaconRow:  # Iterating through each cell of the row
            readBeacVal = int(cellBeacObj.value)
            beacLengths.append(readBeacVal)  # Appends all the lengths read in from the excel file

    beacTotal = 0  # Use this to keep track of where we are in the total number of bytes.

    outVals = []

    for beacLength in beacLengths:
        beacChunk = data[beacTotal:(beacTotal+beacLength-1)]
        beacTotal += beacLength
        if beacChunk == 'allstarcosgc':
            outVals.append(beacChunk)
            continue
        else:
            hexBeacVal = binascii.hexlify(beacChunk)
            decBeacVal = int(hexBeacVal, 16)
            outVals.append(decBeacVal)
    return


def generalReader(genData, genSheet):
    lengths = []
    for rowOfCellObjects in sheet[minIndex:maxIndex]:  # Going through the row of values.
        for cellObj in rowOfCellObjects:  # Iterating through each cell of the row
            readVal = int(cellObj.value)
            lengths.append(readVal)  # Appends all the lengths read in from the excel file

    total = 0  # Use this to keep track of where we are in the total number of bytes.

    binVals = []

    for length in lengths:  # Converts all of the data into binary
        chunk = data[total:(total+length-1)]
        total += length
        numBits = int(len(chunk) * 4.0)  # Defining the padding at the end of binary.
        binVal = bin(int(chunk, 16))[2:].zfill(numBits)
        binVals.append(binVal)

    print(binVals)

    # Now we have the full set of binary data, we can re-chop it up.  This is necessary to account for partial bytes.

    for length in lengths:
        length *= 8.0  # Bytes to bits
        if not round(length) == length:  # Checking if all the bits are whole numbers
            raise Exception('Non-whole number of bits')
        else:
            length = int(length)


generalReader(data, sheet)
"""
now = datetime.datetime.now()

dateString = str(now.month) + "." + str(now.day) + "." + str(now.year)

outFileName = dateString + "." + str(outVals[timeLocation])

print outFileName
"""