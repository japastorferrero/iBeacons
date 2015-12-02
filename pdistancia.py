# pruebas de distancia


import blescan
import sys

import bluetooth._bluetooth as bluez

dev_id = 0


# Metodo para realizar mediciones
# Esperar a pulsar una tecla y medir distancias para asignar RSSI
# Meterlo en una base de datos

# Dibujar una cuadricula x-y
# Colocar ibeacon en x-y conocidas
# Medir RSSI en ciertas cuadriculas
# Introducir valores
# Algoritmo de medida para otras aproximaciones x-y

# Cargar fichero de configuracion
# Aplicar configuracion a las variables

NUM_IBEACON = 4
NUM_MEDIDAS_MEDIA = 10
MAC_ADRESS = ["0C:F3:EE:00:65:06","0C:F3:EE:00:89:52","0C:F3:EE:00:82:B8","0C:F3:EE:00:66:90"]

# Define functions

# Initialize system
def init():
    try:
        sock = bluez.hci_open_dev(dev_id)
        print "ble thread started"
    except:
        print "error accessing bluetooth device..."
        sys.exit(1)
    return

# Scan iBeacon with MAC address
def scanBT():
    Measures = ""
    return Measures

# Record register in DBMS
def save(Measures):
    return





blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)



while True:
	media = 0
	raw_input ("Pulsa una tecla para continuar ...")
	returnedList = blescan.parse_events(sock, 10)
	print "----------"
	for beacon in returnedList:
		print beacon, " ", beacon[62:]
		media = media + int(beacon[62:])
	print "La media es: ", (media/10.0)
