import sys
import socket
import json
import bluetooth
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QLCDNumber, QPushButton, QSlider, QHBoxLayout, QLabel)
from PyQt5.QtGui import QPixmap
 
class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        temperature = QLabel('temperature CPU  C')
        distance = QLabel('distance to obstacle cm')
        
        
        temperature_cpu =  QLCDNumber(self)
        temperature_cpu.setDigitCount(6)
        temperature_cpu.display(get_temperature())

        distance_obst = QLCDNumber(self)
        distance_obst.setDigitCount(6)
        distance_obst.display(get_distance())

        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(10)

        button_fw = QPushButton("FORWARD")
        grid.addWidget(button_fw, 3, 1)
        button_fw.clicked.connect(bw_forward)

        button_st = QPushButton("STOP")
        grid.addWidget(button_st, 4, 1)
        button_st.clicked.connect(stop)

        button_lf = QPushButton("LEFT")
        grid.addWidget(button_lf, 4, 0)
        button_lf.clicked.connect(fw_left)

        button_rg = QPushButton("RIGHT")
        grid.addWidget(button_rg, 4, 2)
        button_rg.clicked.connect(fw_right)

        button_bk = QPushButton("BACK")
        grid.addWidget(button_bk, 5, 1)
        button_bk.clicked.connect(bw_backward)

        lcd_speed = QLCDNumber(self)
        sld_speed = QSlider(Qt.Horizontal, self)
        sld_speed.valueChanged.connect(lcd_speed.display)
        sld_speed.valueChanged.connect(set_speed, sld_speed.value())

        grid.addWidget(sld_speed, 3, 7)
        grid.addWidget(lcd_speed, 3, 8)

        grid.addWidget(temperature, 4, 7)
        grid.addWidget(temperature_cpu, 4, 8)
        grid.addWidget(distance, 5, 7)
        grid.addWidget(distance_obst, 5, 8)

        pixmap = QPixmap("car.png")
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        grid.addWidget(lbl, 2, 3)
        
        self.setLayout(grid) 
        
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Picar2S')    
        self.show()

def fw_left():
    s.send("L".encode())
    print("left")

def fw_right():
    s.send("R".encode())
    print("right")

def bw_forward():
    s.send("F".encode())
    print("forward")

def bw_backward():
    s.send("B".encode())
    print("back")

def stop():
    s.send("S".encode())
    print("stop")

def get_temperature():
    data = sock.recv(1024)
    t = data.decode()
    print("temperature  ####", t)
    return t
    

def get_distance():
    return "100"

def set_speed(speed):
    s.send(str(speed).encode())
    print(speed)

#bloutooth
host = "B8:27:EB:FC:D9:A0" # The address of Raspberry PI Bluetooth adapter on the server.
port = 1


#wifi
HOST = "192.168.1.105" # IP address of your Raspberry PI
PORT = 64035     # The port used by the server


if __name__ == '__main__':
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))
    print("Bloototh connect!")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
