'''
Created on Jul 28, 2016

@author: maxr
'''

from tkinter import *
from ExtractData import ExtractData
from menuTexts import *
from FileIO import FileIO
from tkinter import messagebox
from Utils import serial_ports, quickPlot, quickNormal, DNL, INL, readFile, writeFile
import re
from MicroControllerSerial import MicroControllerSerial as MCS
from time import sleep
import threading


class PostProcessingUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title('DAC Results Post Processing')
        self.pack()
        
        self.fio = FileIO()
        self.daqInputFilePath = "C:/Users/maxr/Desktop/PythonWorkspaces/ScriptForDACDAQ/ChipKit_DAC_PostProcessing/dac_data_spec.csv"
        self.daqInputFile = None
        self.comPort = 'No Com Port\nSelected'
        self.baudRate = '115200'
        self.microReceive = 'Not Connected'
        self.runningDACDAQ = False
        self.daqThreadActive = False
        
        self.postProcFilePath = "C:/Users/maxr/Desktop/PythonWorkspaces/ScriptForDACDAQ/ChipKit_DAC_PostProcessing/dac_data_spec.csv"
        self.postProcFile = None
        self.dnlFile = None
        self.inlFile = None
                
        self.buttonColor = 'light blue'
        
        self.menuBar()
        self.mainFrame()
        
        
    def mainFrame(self):
        
        "DAQ Frame*************************************************************"
        daqFrame = LabelFrame(self, text='Data Acquisition Field')
        
        daqPortFrame = Frame(daqFrame)
        daqPortLabel = Label(daqPortFrame, text="uC Comm Port:", anchor='w', width=15)
        daqPortLabel.pack(side='left', fill=BOTH)
        self.daqPortListBox = Listbox(daqPortFrame, selectmode=SINGLE)
        self.refreshComPorts()
        self.daqPortListBox.pack(side='left', fill=BOTH)
        self.daqSelectedPortLabel = Label(daqPortFrame, text=self.comPort, width=15, \
                                     anchor='w')
        self.daqSelectedPortLabel.pack(side='left', fill=BOTH)
        self.daqPortListBox.bind('<<ListboxSelect>>', self.setComPort)
        daqPortRefreshButton = Button(daqPortFrame, text='Refresh Ports', width=15, \
                                      command=self.refreshComPorts, bg=self.buttonColor)
        daqPortRefreshButton.pack(side='left', fill='y')
        daqPortFrame.pack(fill=BOTH)
        
        daqBaudRateFrame = Frame(daqFrame)
        daqBaudRateLabel = Label(daqBaudRateFrame, text='Serial Baud Rate:', anchor='w', \
                                 width=15)
        daqBaudRateLabel.pack(side='left', fill=BOTH)
        baudRateStrVar = StringVar()
        self.daqBaudRateEntry = Entry(daqBaudRateFrame, textvariable=baudRateStrVar)
        baudRateStrVar.set(self.baudRate)
        self.daqBaudRateEntry.pack(side='left', fill=BOTH)
        daqBaudRateFrame.pack(fill=BOTH)
        
        daqTestConnectionFrame = Frame(daqFrame)
        daqTestConnectionButton = Button(daqTestConnectionFrame, text='Test Connection', \
                                         width=15, bg=self.buttonColor, \
                                         command=self.testMicroConnection)
        daqTestConnectionButton.pack(side='left', fill=BOTH)
        self.daqTestConnectionLabel = Label(daqTestConnectionFrame, text=self.microReceive, \
                                            anchor='w', width=15)
        self.daqTestConnectionLabel.pack(side='left', fill=BOTH)
        daqTestConnectionFrame.pack(fill=BOTH)
        
        
        daqFileFrame = Frame(daqFrame)
        daqInputFileButton = Button(daqFileFrame, text='DAQ File Browse', \
                                    command=self.selectDaqFile, bg=self.buttonColor, \
                                    width=15)
        daqInputFileButton.pack(side='left')
        self.daqFilePathLabel = Label(daqFileFrame, text=self.daqInputFilePath, \
                                      wraplength=300, anchor='w')
        self.daqFilePathLabel.pack(side='left', fill=BOTH)
        daqFileFrame.pack(fill=BOTH)
        
        daqStopStartFrame = Frame(daqFrame)
        daqStopButton = Button(daqStopStartFrame, text='STOP', bg='#ee7676', \
                               command=self.stopDaq, width=15)
        daqStopButton.pack(side='left')
        self.daqCurrentModeLabel = Label(daqStopStartFrame, text="Mode: Stopped")
        self.daqCurrentModeLabel.pack(side='left')
        daqStartButton = Button(daqStopStartFrame, text='START', bg='#76ee81', \
                                command=self.startDaq, width=15)
        daqStartButton.pack(side='left', fill=BOTH)
        daqStopStartFrame.pack(fill=BOTH)
        
        
        
        daqFrame.pack(fill=BOTH)
        
        "Input Frame***********************************************************"
        paramInputFrame = LabelFrame(self, text='Post Processing Parameter Input Field')
        
        postProcFileFrame = Frame(paramInputFrame)
        postProcFileButton = Button(postProcFileFrame, text='Post Proc File',bg=self.buttonColor, \
                                command=self.selectPostProcFile, width=15)
        postProcFileButton.pack(side=LEFT)
        self.postProcFilePathLabel = Label(postProcFileFrame, text=self.postProcFilePath, \
                                           wraplength=300, anchor='w')
        self.postProcFilePathLabel.pack(side=LEFT)
        postProcFileFrame.pack(fill=BOTH)
        
        adcPrecisionFrame = Frame(paramInputFrame)
        adcPrecisionLabel_0 = Label(adcPrecisionFrame, text='ADC Precision: ', anchor='w', width=22)
        adcPrecisionLabel_0.pack(side=LEFT)
        adcPrecision = StringVar()
        self.adcPrecisionEntry = Entry(adcPrecisionFrame, textvariable=adcPrecision)
        self.adcPrecisionEntry.pack(side=LEFT)
        adcPrecisionLabel_1 = Label(adcPrecisionFrame, text='Bits')
        adcPrecisionLabel_1.pack(side=LEFT)
        adcPrecisionFrame.pack(fill=BOTH)
        
        dacPrecisionFrame = Frame(paramInputFrame)
        dacPrecisionLabel_0 = Label(dacPrecisionFrame, text='DAC Precision: ', anchor='w', width=22)
        dacPrecisionLabel_0.pack(side=LEFT)
        dacPrecision = StringVar()
        self.dacPrecisionEntry = Entry(dacPrecisionFrame, textvariable=dacPrecision)
        self.dacPrecisionEntry.pack(side=LEFT)
        dacPrecisionLabel_1 = Label(dacPrecisionFrame, text='Bits')
        dacPrecisionLabel_1.pack(side=LEFT)
        dacPrecisionFrame.pack(fill=BOTH)
        
        sampleFrame = Frame(paramInputFrame)
        sampleLabel_0 = Label(sampleFrame, text='Expected Samples Per Code: ', anchor='w', width=22)
        sampleLabel_0.pack(side=LEFT)
        samplesPerCode = StringVar()
        self.sampleEntry = Entry(sampleFrame, textvariable=samplesPerCode)
        self.sampleEntry.pack(side=LEFT)
        sampleLabel_1 = Label(sampleFrame, text='Samples')
        sampleLabel_1.pack(side=LEFT)
        sampleFrame.pack(fill=BOTH)
        
        maxVoltFrame = Frame(paramInputFrame)
        maxVoltLabel_0 = Label(maxVoltFrame, text='Maximum Output Voltage: ', anchor='w', width=22)
        maxVoltLabel_0.pack(side=LEFT)
        maxVolt = StringVar()
        self.maxVoltEntry = Entry(maxVoltFrame, textvariable=maxVolt)
        self.maxVoltEntry.pack(side=LEFT)
        maxVoltLabel_1 = Label(maxVoltFrame, text="Volts")
        maxVoltLabel_1.pack(side=LEFT)
        maxVoltFrame.pack(fill=BOTH)      
        
        specialCaseFrame = Frame(paramInputFrame)
        self.specialCase = IntVar()
        specialCaseCheckbutton = Checkbutton(specialCaseFrame, text='Special Case? (see help for details)', \
                                             variable=self.specialCase, onvalue=1, \
                                             offvalue=0, anchor='w', width=22) 
        specialCaseCheckbutton.select()
        specialCaseCheckbutton.pack(fill=BOTH)
        
        self.breakIfErrorVar = BooleanVar()
        breakIfErrorCheckbutton = Checkbutton(specialCaseFrame, text="Break if error in processing? (see help for details)", \
                                              variable=self.breakIfErrorVar, onvalue=True, \
                                              offvalue=False, anchor='w', width=22)
        breakIfErrorCheckbutton.pack( fill=BOTH)
        
        specialCaseFrame.pack(fill=BOTH) 
        
        paramInputFrame.pack(fill=BOTH)
        
        
        "Results Frame*********************************************************"
        resultOutputFrame = LabelFrame(self, text='Result Output Select Field')
        
                
        # ----------
        dnlFileFrame = Frame(resultOutputFrame)
        self.dnlFileCheck = IntVar()
        dnlFileCheckbutton = Checkbutton(dnlFileFrame, text='Save DNL to file?', \
                                         variable=self.dnlFileCheck, onvalue=1, \
                                         offvalue=0)
        dnlFileCheckbutton.pack(side=LEFT)
        dnlFileFrame.pack(fill=BOTH)
        
        # ----------
        inlFileFrame = Frame(resultOutputFrame)
        self.inlFileCheck = IntVar()
        inlFileCheckbutton = Checkbutton(inlFileFrame, text='Save INL to file?', \
                                         variable=self.inlFileCheck, onvalue=1, \
                                         offvalue=0)
        inlFileCheckbutton.pack(side=LEFT)
        inlFileFrame.pack(fill=BOTH)
        
        # ----------
        dataPlotFrame = Frame(resultOutputFrame)
        self.dataPlotRaw = IntVar()
        dataPlotRawCheckbutton = Checkbutton(dataPlotFrame, text='Plot Raw Samples?', \
                                         variable=self.dataPlotRaw, onvalue=1, \
                                         offvalue=0, anchor='w', width=20)
        dataPlotRawCheckbutton.pack(side=LEFT)
        self.dataPlotAverage = IntVar()
        dataPlotAverageCheckbutton = Checkbutton(dataPlotFrame, text='Plot Sample Averages?', \
                                         variable=self.dataPlotAverage, onvalue=1, \
                                         offvalue=0)
        dataPlotAverageCheckbutton.pack(side=LEFT)
        dataPlotFrame.pack(fill=BOTH)
        
        # ----------
        dnlPlotFrame = Frame(resultOutputFrame)
        self.dnlQuickPlotCheck = IntVar()
        dnlQuickPlotCheckbutton = Checkbutton(dnlPlotFrame, text='Plot DNL?', \
                                              variable=self.dnlQuickPlotCheck, \
                                              onvalue=1, offvalue=0, anchor='w', width=20)
        dnlQuickPlotCheckbutton.pack(side=LEFT)
        self.dnlNormalPlotCheck = IntVar()
        dnlNormalPlotCheckbutton = Checkbutton(dnlPlotFrame, text='Plot DNL Normal dist?', \
                                              variable=self.dnlNormalPlotCheck, \
                                              onvalue=1, offvalue=0)
        dnlNormalPlotCheckbutton.pack(side=LEFT)
        dnlPlotFrame.pack(fill=BOTH)
                
        # ----------
        inlPlotFrame = Frame(resultOutputFrame)
        self.inlQuickPlotCheck = IntVar()
        inlQuickPlotCheckbutton = Checkbutton(inlPlotFrame, text='Plot INL?', \
                                              variable=self.inlQuickPlotCheck, \
                                              onvalue=1, offvalue=0, anchor='w', width=20)
        inlQuickPlotCheckbutton.pack(side=LEFT)
        self.inlNormalPlotCheck = IntVar()
        inlNormalPlotCheckbutton = Checkbutton(inlPlotFrame, text='Plot INL Normal dist?', \
                                              variable=self.inlNormalPlotCheck, \
                                              onvalue=1, offvalue=0)
        inlNormalPlotCheckbutton.pack(side=LEFT)
        inlPlotFrame.pack(fill=BOTH)
        
        
        resultOutputFrame.pack(fill=BOTH)
        
        
        "Begin Processing Frame************************************************"
        beginProcessingButtonFrame = LabelFrame(self, text='Begin Processing')
        beginProcessingButton = Button(beginProcessingButtonFrame, text='Begin Processing', command=self.beginProcessing, bg=self.buttonColor)
        beginProcessingButton.pack(fill=BOTH)
        beginProcessingButtonFrame.pack(fill=BOTH)
        
        
        "Log Frame*************************************************************"
        logFrame = LabelFrame(self, text='Log')
        self.logLabel = Label(logFrame, text="App Log", anchor='nw', width=50, \
                         height=3, bg='white')
        self.logLabel.pack(fill=BOTH)
        logFrame.pack(fill=BOTH)
        
    def beginProcessing(self):
        try:
            self.postProcFile = open(self.postProcFilePath, 'r')
            _chipSpecs = [int(self.adcPrecisionEntry.get()),
                          2**int(self.adcPrecisionEntry.get()) - 1,
                          int(self.sampleEntry.get()),
                          float(self.maxVoltEntry.get())]
            self.ED = ExtractData(file=self.postProcFile, chipSpecs=_chipSpecs, \
                                  specialCase=self.specialCase.get(), \
                                  break_when_err=self.breakIfErrorVar.get())
        
            self.postProcFile.close()
            
            _avgSmpl = self.ED.averageSamples()
            _rawSmpl = self.ED.getSamples()

            _avgVolt = []
            _rawVolt = []
            for k in _rawSmpl:
                    _rawVolt.append(_rawSmpl[k])
            for k in _avgSmpl:
                _avgVolt.append(_avgSmpl[k])
            _lsb = _chipSpecs[3] / float(self.dacPrecisionEntry.get())
            _dnl = DNL(_avgVolt, _lsb)
            _inl = INL(_avgVolt, _lsb)
            
            if (self.dnlFileCheck.get() == 1):
                self.dnlFile = writeFile(exten='.csv', ftypes=[('comma separated value', '.csv'), \
                                                                       ('all files', '.*')], \
                                                 ifilen='DNL_File.csv')
                for line in _dnl:
                    self.dnlFile.write(str(line) + ',\n')
                self.dnlFile.close()
                
            if (self.inlFileCheck.get() == 1):
                self.inlFile = writeFile(exten='.csv', ftypes=[('comma separated value', '.csv'), \
                                                                       ('all files', '.*')], \
                                                 ifilen='INL_File.csv')
                for line in _inl:
                    self.inlFile.write(str(line) + ',\n')
                self.inlFile.close()
                
            if (self.dataPlotRaw.get() == 1):
                quickPlot(_rawVolt,xlbl='Code', ylbl='Volt')
                
            if (self.dataPlotAverage.get() == 1):
                quickPlot(_avgVolt,xlbl='Code', ylbl='Volt')
                
            if (self.dnlQuickPlotCheck.get() == 1):
                quickPlot(_dnl, ttl="DNL of {} bit DAC".format(self.dacPrecisionEntry.get()), \
                          xlbl="Code", ylbl="LSB")
                
            if (self.dnlNormalPlotCheck.get() == 1):
                quickNormal(_dnl, view=[-0.1, 0.1, 100], ttl="DNL Normal Dist of {} bit DAC".format(self.dacPrecisionEntry.get()))
            
            if (self.inlQuickPlotCheck.get() == 1):
                quickPlot(_dnl, ttl="INL of {} bit DAC".format(self.dacPrecisionEntry.get()), \
                          xlbl="Code", ylbl="LSB")
                
            if (self.inlNormalPlotCheck.get() == 1):
                quickNormal(_inl, view=[-5, 5, 100], ttl="INL Normal Dist of {} bit DAC".format(self.dacPrecisionEntry.get()))
            
        except IOError:
            messagebox.showerror("File Error", "Could not open file.")
        except ValueError:
            messagebox.showerror("Value Error", "Wrong value or type for post proc entry.")
        
    def refreshComPorts(self):
        try:
            self.comPort = 'No Com Port\nSelected'
            self.daqSelectedPortLabel.config(text=self.comPort)
            self.microNotConnectedLabel()
        except:
            pass
        availablePorts = serial_ports()
        self.daqPortListBox.delete(0, END)
        for ports in availablePorts:
            self.daqPortListBox.insert(END, ports)
        self.daqPortListBox.config(height=len(availablePorts))
    
    def setComPort(self, event):
        sel = self.daqPortListBox.curselection()
        self.comPort = self.daqPortListBox.get(sel)
        self.daqSelectedPortLabel.config(text=self.comPort)
        
    def selectDaqFile(self):
        self.fio.fileLocation()
        self.daqInputFilePath = self.fio.getFileLocation()
        self.daqFilePathLabel.config(text=self.daqInputFilePath)
    
    def testMicroConnection(self):
        if not re.match(r'COM\d+', self.comPort):
            messagebox.showerror("No Com Port", "Please select a com port!")
        else:
            try:
                self.baudRate = int(self.daqBaudRateEntry.get())
                if self.comPort in serial_ports():
                    self.mcs = MCS(self.comPort, self.baudRate)
                    self.mcs.testConnection()
                    self.mcs.close()
                    self.microWasConnectedLabel()
                else:
                    self.microNotConnectedLabel()
                    messagebox.showerror("No Com Port", "Please refresh com ports.")
                
            except ValueError:
                self.microNotConnectedLabel()
                messagebox.showerror('Type Error', 'Incorrect type for Baud Rate.')
    
    def microNotConnectedLabel(self):
        self.microReceive = "Not Connected"
        self.daqTestConnectionLabel.config(text=self.microReceive)
        
    def microWasConnectedLabel(self):
        self.microReceive = "Connected"
        self.daqTestConnectionLabel.config(text=self.microReceive)
    
    def stopDaq(self):
        if self.runningDACDAQ == True:
            self.runningDACDAQ = False
            while self.daqThreadActive:
                pass
            self.mcs.stopAndReset()
            self.mcs.close()
            self.daqCurrentModeLabel.config(text="Mode: Stopped")
            self.daqInputFile.close()
        else:
            pass
    
    def startDaq(self):
        self.testMicroConnection()
        
        if not self.microReceive == 'Connected':
            messagebox.showerror('Fix Connection', 'Make sure the Micro is actually connected.')
        else:
            try:
                if self.runningDACDAQ == False:
                    self.daqInputFile = open(self.daqInputFilePath, 'w')
                    self.daqCurrentModeLabel.config(text="Mode: Running")
                    self.mcs = MCS(self.comPort, self.baudRate)
                    self.runningDACDAQ = True
                    
                    threading.Thread(target=self.run_dac_experiment).start()
                    
                else:
                    messagebox.showerror('Still Running', 'The experiment is still running.')
                    
            except ValueError:
                messagebox.showerror('Type Error', 'Incorrect type for Baud Rate.')
            except IOError:
                messagebox.showerror("File Error", "Could not open file.")
    
    def run_dac_experiment(self):
        self.daqThreadActive = True
        self.mcs.stopAndReset()
        self.mcs.startConversion()
        _progress = self.mcs.checkProgress()
        _progressFF = _progress
        while(_progress == _progressFF and self.runningDACDAQ):
            _progressFF = _progress
            _sample = self.mcs.readSample()
            while("NoSample" not in _sample and self.runningDACDAQ):
                self.daqInputFile.write(_sample)
                _sample = self.mcs.readSample()
            self.mcs.startConversion()
            _progress = self.mcs.checkProgress()
        self.daqThreadActive = False
        self.stopDaq()
        
    
    def selectPostProcFile(self):
        self.fio.fileLocation()
        self.postProcFilePath = self.fio.getFileLocation()
        self.postProcFilePathLabel.config(text=self.postProcFilePath)
    
    def menuBar(self):
        self.menubar = Menu(self)

        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Set Initial Values", command=self.setInitValues)
        self.menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="How To Use", command=self.howToUseMenu)
        helpmenu.add_command(label="About", command=self.aboutMenu)
        helpmenu.add_separator()
        helpmenu.add_command(label='Special Case', command=self.specialCaseMenu)
        helpmenu.add_command(label='Break if error', command=self.breakIfErrorMenu)
        self.menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=self.menubar)
    
    def setInitValues(self):
        pass
    
    def aboutMenu(self):
        pass
    
    def howToUseMenu(self):
        pass
    
    def specialCaseMenu(self):
        messagebox.showinfo("Special Case", specialCaseText)
        
    def breakIfErrorMenu(self):
        messagebox.showinfo("Break If Error.", breakIfErrorText)
