'''
Created on Jul 20, 2016

@author: maxr
'''
from tkinter import Tk
from ExtractData import ExtractData
from Utils import DNL, INL, quickPlot, quickNormal
from PostProcessingUI import PostProcessingUI

ADC_PRECISION = 24
MAX_ADC_VALUE = 2**ADC_PRECISION-1
SAMPLES_PER_CODE = 10
MAX_VOLTAGE = 3.3
CHIP_SPECS = [ADC_PRECISION, MAX_ADC_VALUE, SAMPLES_PER_CODE, MAX_VOLTAGE]


FILE_NAME = "dac_data_spec.csv"
FILE = None
LSB = MAX_VOLTAGE / MAX_ADC_VALUE
SPECIAL_CASE = True
BREAK_WHEN_ERR = False

if __name__ == '__main__':
    
    ED = ExtractData(FILE_NAME, FILE, CHIP_SPECS, SPECIAL_CASE, BREAK_WHEN_ERR)
    avg = ED.averageSamples()
    dnl = []
    volt = []
    for k in avg:
        volt.append(avg[k])
    print(volt)
    dnl = DNL(volt, LSB)
    print(dnl)
    quickPlot(dnl, ttl="DNL of 12 bit dac", xlbl="Code", ylbl="LSB")
    quickPlot(volt,ylbl='Volt')
    """

    
    root = Tk()
    app = PostProcessingUI(master=root)
    app.mainloop()
    """
    
    
    
    
