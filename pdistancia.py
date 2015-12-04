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


NUM_MEDIDAS_MEDIA = 5
MAC_ADDRESS = ["0c:f3:ee:00:65:06","0c:f3:ee:00:89:52","0c:f3:ee:00:82:b8","0c:f3:ee:00:66:90"]


# Define functions

# Initialize system

try:
    sock = bluez.hci_open_dev(dev_id)
    print "ble thread started"
except:
    print "error accessing bluetooth device..."
    sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
    raw_input("pulsa una tecla ...")
    ListSCAN = []
    RSSI = []
    media = []
    MAC = []
    total = 0
    size = len(MAC_ADDRESS)
    for x in range(0, size):
        media.append(0)
        RSSI.append(0)
        MAC.append(0)

    while total < (size*10):
        returnedList = blescan.parse_events(sock, 1)
        for x in range(0,size):
            if ((MAC_ADDRESS[x] in returnedList[0]) & (MAC[x] < NUM_MEDIDAS_MEDIA)):
                media[x] = media[x] + int(returnedList[0][62:])
                MAC[x] = MAC[x] + 1
                print MAC[x],returnedList[0][0:17]+" "+ returnedList[0][62:]
        total = total + 1


    for z in range(0,(size)):
        RSSI[z] = int(media[z] / float(NUM_MEDIDAS_MEDIA))
        ListSCAN.append(MAC_ADDRESS[z]+" "+str(RSSI[z]))

    for beacon in ListSCAN:
        print beacon[0:17]+" "+beacon[19:]
