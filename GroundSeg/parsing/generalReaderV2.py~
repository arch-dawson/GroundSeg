#!/usr/bin/python3

import binascii  # Used for converting hex string to hexadecimal

import openpyxl  # Used for reading/writing excel files
from openpyxl.cell import get_column_letter 

import re  # Used for parsing unit conversions

import math  # Need to use log2 for conversions

import sys # For command line arguments

from bitstring import BitArray

import MySQLdb as sql  # For writing information to database

# COMMAND LINE ARGUMENTS
# python3 generalReader.py xlsxFileName parseFileName databaseName tableName
# EXAMPLE: python3 generalReader.py BeaconDefinition.xlsx mostRecent

# ====== CHANGE TO REFLECT LAYOUT OF TELEMETRY DEFINITION AND DATABASE ======

# DATABASE NAME IN MYSQL
databaseName = "fakeSatellite"

# TABLE NAME WITHIN DATABSE
tableName = "fakeTelemetry"

# SUB IN YOUR FILE NAME HERE WHERE THE BYTE LENGTHS ARE
xlsxFileName = 'BeaconDefinition.xlsx'

# CHANGE THE NAME OF THE FILE YOU WANT TO PARSE
parseFileName = 'mostRecent'

# NUMBER OF ROWS AT THE TOP WITHOUT DATA
descRows = 1

# ====== END OF USER CHANGES ======

wb = openpyxl.load_workbook(xlsxFileName)  # Loads the beacon definition excel file

sheetList = wb.get_sheet_names()  # Loads in the names of the sheets.

sheet = wb.get_sheet_by_name(sheetList[0])  # As of 3/8/16 we only want the first sheet

maxRow = sheet.max_row

maxCol = sheet.max_column

firstRowCoords = tuple(sheet['A1':get_column_letter(maxCol)+'1'])

firstRow = []

for obj in firstRowCoords:
    for temp in obj:
        firstRow.append(temp.value)

# MIN AND MAX OF INDICES WHERE THE BYTE LENGTHS ARE

byteColVal = [item for item in firstRow if 'byt' in str(item).lower()]
if byteColVal:
    minIndex = chr(ord(get_column_letter(firstRow.index(byteColVal[0]))) + 1) + str(1 + descRows)
    maxIndex = chr(ord(get_column_letter(firstRow.index(byteColVal[0]))) + 1) + str(maxRow)
else:
    minIndex = 'F' + str(1 + descRows)
    maxIndex = 'F' + str(maxRow)
    
# ADD INDICES FOR UNIT CONVERSIONS LINE
# USE 'E' OR 'e' FOR EXPONENTIAL NOTATION: '123e7', NOT '123*10^7'
# USE 'NaN' OR '1' IF NO CONVERSION
unitColVal = [item for item in firstRow if 'conv' in str(item).lower()]
if byteColVal:
    unitMinIndex = chr(ord(get_column_letter(firstRow.index(unitColVal[0]))) + 1) + str(1 + descRows)
    unitMaxIndex = chr(ord(get_column_letter(firstRow.index(unitColVal[0]))) + 1) + str(maxRow)
else:
    unitMinIndex = 'H' + str(1 + descRows)
    unitMaxIndex = 'H' + str(maxRow)

# INDICES FOR DATA TYPE 
typeColVal = [item for item in firstRow if 'type' in str(item).lower()]
if byteColVal:
    typeMinIndex = chr(ord(get_column_letter(firstRow.index(typeColVal[0]))) + 1) + str(1 + descRows)
    typeMaxIndex = chr(ord(get_column_letter(firstRow.index(typeColVal[0]))) + 1) + str(maxRow)
else:
    typeMinIndex = 'G' + str(1 + descRows)
    typeMaxIndex = 'G' + str(maxRow)

# INDICES FOR ROW LABELS
nameColVal = [item for item in firstRow if 'Field' in str(item).lower()]
if nameColVal:
    nameMinIndex = chr(ord(get_column_letter(firstRow.index(nameColVal[0]))) + 1) + str(1 + descRows)
    nameMaxIndex = chr(ord(get_column_letter(firstRow.index(nameColVal[0]))) + 1) + str(maxRows)
else:
    nameMinIndex = 'A' + str(1 + descRows)
    nameMaxIndex = 'A' + str(maxRow)


# --------------------------------------------------------

f = open(parseFileName)  # Opens the hex beacon file to be read in.

data = f.read()
f.close()

def generalReader(genData, genSheet):
    lengths = []
    for rowOfCellObjects in sheet[minIndex:maxIndex]:  # Going through the row of values.
        for cellObj in rowOfCellObjects:  # Iterating through each cell of the row
            readVal = int(cellObj.value)
            readVal *= 2 # Bytes are two hex characters
            lengths.append(readVal)  # Appends all the lengths read in from the excel file

    total = 0  # Use this to keep track of where we are in the total number of bytes.

    binVals = []

    for length in lengths:  # Converts all of the data into binary
        chunk = data[total:(total+length)]
        total += length
        numBits = int(len(chunk) * 4.0)  # Defining the padding at the end of binary.
        binVal = bin(int(chunk, 16))[2:].zfill(numBits)
        binVals.append(binVal)

#    for length in lengths:
#        length *= 8.0  # Bytes to bits
#        if not round(length) == length:  # Checking if all the bits are whole numbers
#            raise Exception('Non-whole number of bits')
#        else:
#            length = int(length)

    # JUST MAKE SURE THAT THE DATA TYPES HAVE THESE IN THEM
    # MAKE SURE THERE'S A 'u' IN THE STRING IF IT'S UINT
    strRe = re.compile('str')
    intRe = re.compile('int')
    doubleRe = re.compile('doub')
    boolRe = re.compile('bool')

    dataCount = 0;

    decVals = [] # TODO: Format output into a list of tuples, including value and type 
    
    for dataConvRow in sheet[typeMinIndex:typeMaxIndex]:
        for dataObj in dataConvRow:
            binArray = BitArray(bin=binVals[dataCount])
            if intRe.search(dataObj.value): # Narrows it down to uint/int
                if 'u' in dataObj.value: # Checking if it's unsigned.  Elegant? No. Effective? Yes.
                    decVals.append(binArray.uint)
                else:
                    decVals.append(binArray.int)
            elif doubleRe.search(dataObj.value):
                decVals.append(binArray.float)
            elif boolRe.search(dataObj.value):
                decVals.append(binArray.uint) # This value should just be 0 or 1
            #else:
                #print(binVals[dataCount])
                #decVals.append(binArray.bytes)
                # 'allstarcosgc' is 12 characters long.  Imma kill someone
            dataCount += 1

    # Now we have the full set of binary data, we can re-chop it up.  This is necessary to account for partial bytes.

    convVals = []

    p = re.compile('\d+(\.\d+)? +(e|E)? +(\d+)?')  # Regular expression for number, optional decimal and exponent

    for convRow in sheet[unitMinIndex:unitMaxIndex]:
        for convObj in convRow:
            if convObj.value == 'NaN':
                convVals.append(1)  # We're going to be multiplying by this, so just a 1 is fine for no conversion
            elif not p.search(convObj.value):
                raise Exception('Weird value in unit conversions.  Use \'NaN\' if no conversion, ')
            else:
                mo = p.search(convObj.value)
                convVals.append(float(mo.group()))

    # Use [a*b for a,b in zip(lista,listb)] for converting
    convertedVals = [a*b for a,b in zip(decVals,convVals)]
    return convertedVals


def dbWrite(dataList):
    database = sql.connect("localhost","root","P0l@r3ubE",databaseName)

    cursor = database.cursor()

    nameStr = '('
    for nameRow in sheet[nameMinIndex:nameMaxIndex]:
        for nameValue in nameRow:
            nameStr = nameStr + nameValue + ', '
    nameStr = nameStr[:-2] + ')' # One extra space and comma
    

    valuesStr = "VALUES ("
    
    for dataVal in dataList:
        valuesStr = valuesStr + dataVal + ', '

    valuesStr = valuesStr[:-2] + ')'

    dbString = "INSERT INTO " + tableName + nameStr + valuesStr

    print(dbString)

values = generalReader(data, sheet)
dbLineGen(values)


"""
now = datetime.datetime.now()

dateString = str(now.month) + "." + str(now.day) + "." + str(now.year)

outFileName = dateString + "." + str(outVals[timeLocation])

print outFileName
"""
