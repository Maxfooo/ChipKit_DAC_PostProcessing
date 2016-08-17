'''
Created on Jul 20, 2016

@author: maxr
'''

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from statistics import mean, stdev
import sys
import glob
import serial
from tkinter import filedialog
import tkinter

def readFile(exten='.hex', ftypes=[('all files', '.*')], idir='C:\\',
                 ifilen='myfile.hex', title='Open File'):
        root = tkinter.Tk()
        file_opt = options = {}
        options['defaultextension'] = exten
        options['filetypes'] = ftypes
        options['initialdir'] = idir
        options['initialfile'] = ifilen
        options['parent'] = root
        options['title'] = title
        root.withdraw()
        return filedialog.askopenfile(mode='r', **file_opt)

def writeFile(exten='.hex', ftypes=[('all files', '.*')], idir='C:\\',
                 ifilen='myfile.hex', title='Save File'):
        root = tkinter.Tk()
        file_opt = options = {}
        options['defaultextension'] = exten
        options['filetypes'] = ftypes
        options['initialdir'] = idir
        options['initialfile'] = ifilen
        options['parent'] = root
        options['title'] = title
        root.withdraw()
        return filedialog.asksaveasfile(mode='w', **file_opt)

def quickPlot(x,y=None, ttl='DAC Voltage', xlbl = 'Time (sec)', ylbl='VDC (V)'):
    plt.figure()
    if y == None:
        plt.plot(x)
    else:
        plt.plot(x,y)
    plt.title(ttl)
    plt.xlabel(xlbl)
    plt.ylabel(ylbl)
    plt.show()

def quickNormal(data, view=[-3, 3, 100], ttl='DAC', xlbl = 'Stdev', ylbl='Error', xbar=False):
    if xbar:
        mu = mean(data)
    else:
        mu = 0
    sig = stdev(data, mu)
    x = np.linspace(view[0],view[1], view[2])
    norm = mlab.normpdf(x, mu, sig)
    plt.plot(x, norm)
    plt.title(ttl)
    plt.xlabel(xlbl)
    plt.ylabel(ylbl)
    plt.annotate('mu={}'.format(round(mean(data), 4)), xy=(sig,max(norm)))
    plt.show()

def findSlope(x,y):
    horizSpan = x.index(max(x)) - x.index(min(x))
    print(horizSpan)
    m = (max(y) - min(y)) / (x[y.index(max(y))] - x[y.index(min(y))])
    return m
    
def DNL(volt, lsb):
    # volt is a list
    # lsb is a voltage
    """ DNL
    The first value of dnl is 0. 
    The rest of the values are determined by taking the current voltage value, 
    subtracting the previous voltage from it, then subtracting the lsb from that. 
    After the subtraction, divide everything by the lsb.
    """
    dnl = []
    for i, v in enumerate(volt):
        if i > 0:
            calc = (v - volt[i-1] - lsb) / lsb
            dnl.append(calc)
        else:
            dnl.append(0)
    return dnl


def INL(volt, lsb):
    """ INL
    The first value of inl is 0.
    The rest of the values are determined by taking the current voltage value,
    subtracting the product of the index of that value (dac code) and the lsb, 
    then subtracting the voltage value for the dac code of 0, which is the offset. 
    After the subtraction, divide everything by the lsb.
    """
    offset = volt[0]
    inl = []
    for i, v in enumerate(volt):
        if i > 0:
            calc = (v - (i*lsb) - offset) / lsb
            inl.append(calc)
        else:
            inl.append(0)
    return inl


def serial_ports():
    """ 
    @Source: http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
