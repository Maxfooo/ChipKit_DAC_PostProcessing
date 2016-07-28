'''
Created on Jul 20, 2016

@author: maxr
'''

from ExtractData import ExtractData
from Utils import DNL, INL, quickPlot, quickNormal

FILE_NAME = "dac_data_spec.csv"
ADC_PRECISION = 24
MAX_ADC_VALUE = 2**ADC_PRECISION-1
MAX_VOLTAGE = 3.3
LSB = MAX_VOLTAGE / MAX_ADC_VALUE
SPECIAL_CASE = True

if __name__ == '__main__':
    ED = ExtractData(FILE_NAME, SPECIAL_CASE)
    avg = ED.averageSamples()
    dnl = []
    volt = []
    for k in avg:
        volt.append(avg[k])
    print(volt)
    dnl = DNL(volt, LSB)
    print(dnl)
    quickPlot(dnl)
    
    
    
