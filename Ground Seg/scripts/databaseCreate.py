#!/usr/bin/python3

import openpyxl

import MySQLdb as sql

fakeSatellite = sql.connect("localhost","root","P0l@r3ubE","fakeSatellite")

cursor = fakeSatellite.cursor()

cursor.execute("DROP TABLE IF EXISTS `fakeTelemetry`")

#New tables have the form `name datatype`

fakeSatellite.close()
