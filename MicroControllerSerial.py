
# Source: https://github.com/vascop/Python-Arduino-Proto-API-v2
# vascop

import serial
from tkinter import messagebox
from tkinter import Tk
from Utils import serial_ports

class MicroControllerSerial(object):
    
    
    def __init__(self, port, baudrate=115200):
        self.connectCmd = b'0'
        self.conversionCmd = b'1'
        self.sampleCmd = b'2'
        self.resetCmd = b'3'
        self.progressCmd = b'4'
        
        try:
            if port in serial_ports():
                self.serial = serial.Serial(port, baudrate, timeout=5)
                self.serial.write(b'99')
            else:
                self.noComPortError()
        except:
            self.noConnectError()
    
    def txrx(self, cmd):
        self.__sendData(cmd)
        return self.__getData()
    
    def testConnection(self):
        self.__sendData(self.connectCmd)
        return self.__getData()
    
    def startConversion(self):
        self.__sendData(self.conversionCmd)
        return self.__getData()
        
    def readSample(self):
        self.__sendData(self.sampleCmd)
        return self.__getData()
        
    def stopAndReset(self):
        self.__sendData(self.resetCmd)
        return self.__getData()
        
    def checkProgress(self):
        self.__sendData(self.progressCmd)
        return self.__getData()
    
    
    def __sendData(self, serial_data):
        try:
            while(self.__getData()[0] != "w"):
                pass
            self.serial.write(serial_data)
        except IndexError:
            self.noConnectError()

    def __getData(self):
        try:
            input_string = self.serial.readline()
            input_string = input_string.decode('utf-8')
            return input_string.rstrip('\n')
        except:
            return "Not Connected"
        
    def flushInput(self):
        self.serial.flushInput()
    
    def flushOutput(self):
        self.serial.flushOutput()
    
    def close(self):
        self.serial.close()
        return True
    
    @classmethod
    def noConnectError(cls):
        root = Tk()
        root.withdraw()
        messagebox.showerror("No connection", "Could not connect to Micro.")
    
    @classmethod
    def noComPortError(cls):
        root = Tk()
        root.withdraw()
        messagebox.showerror("No Com Port", "The selected com port does not exist.")
        
    
    
    
    
    
    






