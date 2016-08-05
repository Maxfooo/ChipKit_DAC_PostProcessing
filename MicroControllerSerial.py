
# Source: https://github.com/vascop/Python-Arduino-Proto-API-v2
# vascop

import serial
from tkinter import messagebox
from tkinter import Tk
from Utils import serial_ports

class MicroControllerSerial(object):
    
    def __init__(self, port, baudrate=115200):
        try:
            if port in serial_ports():
                self.serial = serial.Serial(port, baudrate, timeout=5)
                self.serial.write(b'99')
            else:
                self.noComPortError()
        except:
            self.noConnctError()
        
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
            self.noConnctError()

    def __getData(self):
        try:
            input_string = self.serial.readline()
            input_string = input_string.decode('utf-8')
            return input_string.rstrip('\n')
        except:
            return "Not Connected"
    
    def close(self):
        self.serial.close()
        return True
    
    @classmethod
    def noConnctError(cls):
        root = Tk()
        root.withdraw()
        messagebox.showerror("No connection", "Could not connect to Micro.")
    
    @classmethod
    def noComPortError(cls):
        root = Tk()
        root.withdraw()
        messagebox.showerror("No Com Port", "The selected com port does not exist.")
        
    
    
    
    
    
    






