
# Source: https://github.com/vascop/Python-Arduino-Proto-API-v2
# vascop

import serial
from tkinter import messagebox

class MicroControllerSerial(object):
    
    def __init__(self, port, baudrate=115200):
        self.serial = serial.Serial(port, baudrate, timeout=2)
        self.serial.write(b'99')
        
    def readline(self):
        self.__sendData(b'0')
        return self.__getData()
    
    def testConnection(self):
        self.__sendData(b'1')
        return self.__getData()
    
    def __sendData(self, serial_data):
        try:
            while(self.__getData()[0] != "w"):
                pass
            serial_data = str(serial_data).encode('utf-8')
            self.serial.write(serial_data)
        except IndexError:
            messagebox.showerror("No connection", "Could not connect to Micro.")

    def __getData(self):
        input_string = self.serial.readline()
        input_string = input_string.decode('utf-8')
        return input_string.rstrip('\n')
        
    
    
    
    
    
    






