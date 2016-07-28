'''
Created on Jul 26, 2016

@author: maxr
'''


"""
Format:

dac_code, dac_value, psw

dac_code = integer, 0 to 4095
dac_value = binary, 24 bits
psw = binray, 4-8 bits, specified in 
http://www.analog.com/media/en/technical-documentation/data-sheets/AD7780.pdf

"""
import re

BREAK_WHEN_ERR = False

ADC_PRECISION = 24
MAX_ADC_VALUE = 2**ADC_PRECISION-1
SAMPLES_PER_CODE = 10
MAX_VOLTAGE = 3.3
ERR_0 = 'Too Many Samples'
ERR_1 = 'Too Few Samples'
ERR_2 = 'Repeat Code'
ERR_3 = 'Out of Order Code'


class ExtractData(object):
    
    def __init__(self, fileName, specialCase=False):
        self.fileName = fileName
        self.specCase = specialCase
        self.extractData()
        self.generateErrorLog()
    
    def extractData(self):
        self.sampleDict = {}
        self.pswDict = {}
        prevCode = -1
        self.errorDict = {ERR_0 : [], ERR_1: [], ERR_2: [], ERR_3: []}
        with open(self.fileName, 'r') as f:
            lineNum = 0
            sampleCount = SAMPLES_PER_CODE-1
            for line in f:
                word = line.split(',')
                
                if re.search('[a-zA-Z]', word[0]):
                    continue
                
                word[0] = int(word[0])
                
                if self.specCase:
                    word[1] = word[1][1:] # remove first bit for special case
                    _max_adc_value = 2**(ADC_PRECISION-1)-1
                    voltage = (float(int(word[1], 2)) / _max_adc_value) * MAX_VOLTAGE
                else:                
                    voltage = (float(int(word[1], 2)) / MAX_ADC_VALUE) * MAX_VOLTAGE
                
                if prevCode == word[0]:
                    if sampleCount >= SAMPLES_PER_CODE:
                        self.errorDict[ERR_0].append('Line: {0}, Entry: {1}'.format(lineNum, line))
                        if BREAK_WHEN_ERR:
                            break
                    self.sampleDict[word[0]].append(voltage)
                    self.pswDict[word[0]].append(word[2])
                    sampleCount += 1
                        
                elif prevCode == word[0] - 1:
                    if sampleCount != SAMPLES_PER_CODE-1:
                        self.errorDict[ERR_1].append('Line: {0}, Entry: {1}'.format(lineNum, line))
                        if BREAK_WHEN_ERR:
                            break
                    if word[0] in self.sampleDict.keys():
                        self.errorDict[ERR_2].append('Line: {0}, Entry: {1}'.format(lineNum, line))
                        if BREAK_WHEN_ERR:
                            break
                    self.sampleDict[word[0]] = [voltage]
                    self.pswDict[word[0]] = [word[2]]
                    sampleCount = 0
                    
                else:
                    self.errorDict[ERR_3].append('Line: {0}, Entry: {1}'.format(lineNum, line))
                    if BREAK_WHEN_ERR:
                        break
                    self.sampleDict[word[0]] = [voltage]
                    self.pswDict[word[0]] = [word[2]]
                    sampleCount = 0
                
                prevCode = word[0]
                lineNum += 1
                    
        f.close()
        
    def getSamples(self):
        return self.sampleDict
    
    def getPsw(self):
        return self.pswDict
    
    def getErrors(self):
        return self.errorDict
    
    def averageSamples(self):
        self.avgSampleDict = {}
        for key, val in self.sampleDict.items():
            self.avgSampleDict[key] = sum(val)/len(val)
        return self.avgSampleDict
    
    def generateErrorLog(self):
        fName = 'ErrorLog.txt'
        f = open(fName, 'w')
        for key, val in self.errorDict.items():
            f.write("\n-------------------\n{}\n-------------------\n".format(key))
            if len(val) > 0:
                for err in val:
                    f.write(err)
            f.write("\n")
        f.close()
            
            
            
            
            
            
            
            
            
            
