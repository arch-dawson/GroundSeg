import binascii

import openpyxl

from openpyxl.cell import get_column_letter, column_index_from_string

wb = openpyxl.load_workbook('BeaconDefinition.xlsx')

sheetList = wb.get_sheet_names() #Loads in the names of the sheets.

sheet = wb.get_sheet_by_name(sheetList[0])

f = open('fakeBeacon')

data = f.read()

if(data[0:12] == 'allstarcosgc'):
    print 'woo'

byte = data[13]
hexadecimal = binascii.hexlify(byte)

decimal = int(hexadecimal, 16)

binary = bin(decimal)

print binary

for rowOfCellObjects in sheet['F3':'F42']: #Going through the row of values.
    for cellObj in rowOfCellObjects: #Iterating through each cell of the row
        print(cellObj.value)
        print(type(cellObj.value))
f.close()
