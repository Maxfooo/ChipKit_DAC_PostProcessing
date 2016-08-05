'''
Created on Jul 29, 2016

@author: maxr
'''

import time
from MicroControllerSerial import MicroControllerSerial as MCS


COM_PORT = 'COM7'
BAUD_RATE = 115200
ser = MCS(COM_PORT, BAUD_RATE)

data = ''
while(data == ''):
    data = ser.readline()
    print(data)
    ser.close()
    data = 'd'
