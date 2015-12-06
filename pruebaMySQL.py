import MySQLdb
from datetime import date, datetime, timedelta
import time

TmSlot = datetime.now()

add_registro = ("INSERT INTO Medidas (Time, MAC, X, Y, RSSI) VALUES (%s, %s, %s, %s, %s)")
cnx = MySQLdb.connect('192.168.1.50','admin','memo6236','BTmedidas')
cursor = cnx.cursor()
data_registro = (TmSlot,"A0:B0:C0:D0:E0:F0:AA:BB", 5, 10, -22)
cursor.execute(add_registro, data_registro)
cnx.commit()
cursor.close()
cnx.close()