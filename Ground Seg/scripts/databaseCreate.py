#!/usr/bin/python3

import openpyxl

import MySQLdb as sql

#====== Loading in Telemetry Information ======
xlsxFileName = 'BeaconDefinition.xlsx'

wb = openpyxl.load_workbook(xlsxFileName)

sheetList = wb.get_sheet_names()

sheet = wb.get_sheet_by_name(sheetList[0])

maxRow = sheet.max_row

firstColCoords = tuple(sheet['A2':'A'+maxRow])

firstCol = []

for obj in firstColCoords:
    for temp in obj:
        firstCol.append(temp.value)

strOut = 'CREATE TABLE fakeTelemetry ('

for item in firstCol:
    strOut = strOut + item + ' VARCHAR(25), '

strOut = strOut + ');'

#====== mySQL Startup ======
fakeSatellite = sql.connect("localhost","root","P0l@r3ubE","fakeSatellite")

cursor = fakeSatellite.cursor()

cursor.execute("DROP TABLE IF EXISTS `fakeTelemetry`")

cursor.execute(strOut)

fakeSatellite.close()
