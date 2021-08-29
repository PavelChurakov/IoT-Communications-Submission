import bluetooth
import random
from gpiozero import CPUTemperature
import json
from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from picar import front_wheels
from picar import back_wheels
import time
import picar
import random
import socket
import threading

HOST = "192.168.1.105" # IP address of your Raspberry PI
PORT = 64035          # Port to listen on (non-privileged ports are > 1023)


picar.setup()

ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
fw.turning_max = 45
fw_speed = 50
bw_speed = 40
ang = 10


def server_bt():
    hostMACAddress = "B8:27:EB:FC:D9:A0" # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
    port = 1
    backlog = 1
    size = 1024
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.bind((hostMACAddress, port))
    s.listen(backlog)
    print("listening on port ", port)
    try:
        client, clientInfo = s.accept()
        while 1:
             tempCPU = CPUTemperature().temperature
             print("CPU temperature: ", tempCPU)
             params = str(round(tempCPU))
             print("data", params.encode())
             client.send(params)
             time.sleep(2)
    except: 
        print("Closing socket")
        client.close()
        s.close()


def server_wifi():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("listening port wifi")
        try:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            last_ang = 90
            while 1:
                data = client.recv(1024)      # receive 1024 Bytes of message in binary format
                if data != b"":
                    com = data.decode()
                    print(com)
                    if com == "L":
                        last_ang = last_ang - ang
                        fw.turn(last_ang)
                    elif com == "R":
                        last_ang = last_ang + ang
                        fw.turn(last_ang)
                    elif com == "F":
                        bw.backward()
                    elif com == "B":
                        bw.forward()
                    elif com == "S":
                        bw.speed = 0
                    else:
                        bw.speed = int(com)
                time.sleep(0.15)
        except: 
            print("Closing socket")
            client.close()
            s.close()


sth = threading.Thread(target=server_bt)
cth = threading.Thread(target=server_wifi)

sth.start()
cth.start()

cth.join()
sth.join()

print("Finish")

