# Version 1.0
# GUI en Python

#!/usr/bin/python
from Tkinter import Tk, Label, Listbox, BOTH
from Tkinter import StringVar
from ttk import Frame, Button, Style
import MySQLdb
from datetime import date, datetime, timedelta
import time

import blescan
import sys

import bluetooth._bluetooth as bluez

dev_id = 0

NUM_MINX = -8
NUM_MAXX = 8
NUM_MINY = -8
NUM_MAXY = 8
NUM_MEDIDAS_MEDIA = 5
MAC_ADDRESS = ["0c:f3:ee:00:65:06","0c:f3:ee:00:89:52","0c:f3:ee:00:82:b8","0c:f3:ee:00:66:90"]
ListBT = []
ListSCAN = []

class Example(Frame):

    def __init__(self, parent, background = "white"):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()
        self.centerWindow()

    def centerWindow(self):

        w = 600
        h = 480

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def initUI(self):

        self.parent.title("Captura de datos")
        self.style = Style()
        self.pack(fill=BOTH, expand=1)

        BotonIncX = Button(self, text="+", command=IncX)
        BotonIncX.place(x=300, y=150)
        label1 = Label(self, text = "Incrementar X:")
        label1.place(x=150, y=150)
        global texto1, texto2, x, y
        x = 0
        y = 0
        texto1 = StringVar()
        texto1.set(x)
        label10 = Label(self, textvariable=texto1, width=5, relief="solid")
        label10.place(x=250, y=175)
        BotonDecX = Button(self, text="-", command=DecX)
        BotonDecX.place(x=300, y=200)
        label2 = Label(self, text = "Decrementar X:")
        label2.place(x=150, y=200)
        BotonIncY = Button(self, text="+", command=IncY)
        BotonIncY.place(x=300, y=250)
        label3 = Label(self, text = "Incrementar Y:")
        label3.place(x=150, y=250)
        texto2 = StringVar()
        texto2.set(y)
        label101 = Label(self, textvariable=texto2, width=5, relief="solid")
        label101.place(x=250, y=275)
        BotonDecY = Button(self, text="-", command=DecY)
        BotonDecY.place(x=300, y=300)
        label4 = Label(self, text = "Decrementar Y:")
        label4.place(x=150, y=300)
        Grabar = Button(self, text="Grabar Registro", command=GrabarRegistro)
        Grabar.place(x=150, y=340)
        global ListaMACs
        ListaMACs = Listbox(self,bd=2,relief="solid",height=4,width=82)
        ListaMACs.place(x=50,y=50)

        Scan = Button(self, text="Escanear RSSI en MAC", command=ScanMAC)
        Scan.place(x=350, y=340)

def IncX():
    global x, texto1
    x = x + 1
    if x > NUM_MAXX:
        x = NUM_MAXX
    texto1.set(x)

def DecX():
    global x, texto1
    x = x - 1
    if x < NUM_MINX:
        x = NUM_MINX
    texto1.set(x)

def IncY():
    global y, texto2
    y = y + 1
    if y > NUM_MAXY:
        y = NUM_MAXY
    texto2.set(y)

def DecY():
    global y, texto2
    y = y - 1
    if y < NUM_MINY:
        y = NUM_MINY
    texto2.set(y)

def GrabarRegistro():
    global x,y
    global ListBT
    TmSlot = datetime.now()
    add_registro = ("INSERT INTO Medidas (Time, MAC, X, Y, RSSI) VALUES (%s, %s, %s, %s, %s)")
    cnx = MySQLdb.connect('192.168.1.50','admin','memo6236','BTmedidas')
    cursor = cnx.cursor()
    for z in ListBT:
        data_registro = (TmSlot, z[0], z[1], z[2], z[3])
        cursor.execute(add_registro, data_registro)
    cnx.commit()
    cursor.close()
    cnx.close()

def ScanMAC():
    global ListBT, ListSCAN
    global x,y
    ListBT = []
    ListaMACs.delete(0,3)
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

    contador = 0

    for beacon in ListSCAN:
        ListaMACs.insert(contador, beacon[0:17]+" "+str(x)+" "+str(y)+" "+beacon[19:])
        ListBT.append([beacon[0:17], x, y, int(beacon[19:])])
        contador = contador + 1



def main():

    root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    try:
        sock = bluez.hci_open_dev(dev_id)
        print "ble thread started"
    except:
        print "error accessing bluetooth device..."
        sys.exit(1)
    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    main()