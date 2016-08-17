'''
Created on Jul 20, 2016

@author: maxr
'''
from tkinter import Tk
from ExtractData import ExtractData
from Utils import DNL, INL, quickPlot, quickNormal, writeFile
from PostProcessingUI import PostProcessingUI

ADC_PRECISION = 24
MAX_ADC_VALUE = 2**ADC_PRECISION-1
SAMPLES_PER_CODE = 10
MAX_VOLTAGE = 3.3
CHIP_SPECS = [ADC_PRECISION, MAX_ADC_VALUE, SAMPLES_PER_CODE, MAX_VOLTAGE]


FILE_NAME = "dac_data_spec.csv"
FILE = None
DAC_PRECISION = 12
MAX_DAC_VALUE = 2**DAC_PRECISION-1  
LSB = MAX_VOLTAGE / MAX_DAC_VALUE
SPECIAL_CASE = True
BREAK_WHEN_ERR = False

script = 0

if __name__ == '__main__':
    
    if script:
        ED = ExtractData(FILE_NAME, FILE, CHIP_SPECS, SPECIAL_CASE, BREAK_WHEN_ERR)
        avg = ED.averageSamples()
        _avg_sample_voltages = writeFile(exten='.csv', ftypes=[('comma separated value', '.csv'), \
                                        ('all files', '.*')], \
                                        ifilen='avg_sample_voltages.csv')
        dnl = []
        volt = []
        for k in avg:
            volt.append(avg[k])
        for line in volt:
            _avg_sample_voltages.write(str(line) + ',\n')
        _avg_sample_voltages.close()
        dnl = DNL(volt, LSB)
        quickPlot(dnl, ttl="DNL of 12 bit dac", xlbl="Code", ylbl="LSB")
        quickPlot(volt,ylbl='Volt')
    else:

    
        root = Tk()
        app = PostProcessingUI(master=root)
        app.mainloop()
    
    
    
    
