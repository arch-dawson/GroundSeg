#!/usr/bin/python3

import openpyxl

import MySQLdb as sql

def createTable(telemetryDef, tableName):
    wb = openpyxl.load_workbook(telemetryDef)
    
    sheetList = wb.get_sheet_names()

    sheet = wb.get_sheet_by_name(sheetList[0])

    maxRow = sheet.max_row

    firstColCoords = tuple(sheet['A2':'A'+str(maxRow)])

    firstCol = []

    for obj in firstColCoords:
        for temp in obj:
            firstCol.append(temp.value)

    strOut = 'CREATE TABLE '+tableName+' ('

    for item in firstCol:
        strOut = strOut + item + ' VARCHAR(25), '

    strOut = strOut[:-2]  # On extra space and comma

    strOut = strOut + ');'

    return strOut

def main(dbQueue, dbName, tableName, telemetryDef)
#====== mySQL Startup ======
dataBase = sql.connect("localhost","root","P0l@r3ubE","fakeSatellite")

cursor = dataBase.cursor()

#cursor.execute("DROP TABLE IF EXISTS fakeTelemetry;")

#cursor.execute(strOut)

#fakeSatellite.close()
