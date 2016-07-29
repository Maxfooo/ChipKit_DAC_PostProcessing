'''
Created on Jul 28, 2016

@author: maxr
'''

from tkinter import *
from ExtractData import ExtractData
from menuTexts import specialCaseText
from FileIO import FileIO
from tkinter import messagebox

class PostProcessingUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title('DAC Results Post Processing')
        self.pack()
        
        self.fileIO = FileIO()
        self.inputFile = None
        self.dnlFile = None
        self.inlFile = None
        
        self.buttonColor = '#000fff000'
        
        self.menuBar()
        self.mainFrame()
        
        
    def mainFrame(self):
        
        "Input Frame***********************************************************"
        paramInputFrame = LabelFrame(self, text='Chip Parameter Input Field')
        
        openFileFrame = Frame(paramInputFrame)
        openFileLabel_0 = Label(openFileFrame, text='Open File: ', anchor='w', width=22)
        openFileLabel_0.pack(side=LEFT)
        openFileButton = Button(openFileFrame, text='Open',bg=self.buttonColor, command=self.getFile, width=16)
        openFileButton.pack(side=LEFT)
        openFileLabel_1 = Label(openFileFrame, text='File')
        openFileLabel_1.pack(side=LEFT)
        openFileFrame.pack(fill=BOTH)
        
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
        specialCaseCheckbutton.pack(fill=BOTH)
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
        dataPlotAverageCheckbutton = Checkbutton(dataPlotFrame, text='Plot Average Samples?', \
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
        self.logMessage = 'App Log.'
        logLabel = Label(logFrame, text=self.logMessage, anchor='nw', width=50, \
                         height=3, bg='white')
        logLabel.pack(fill=BOTH)
        logFrame.pack(fill=BOTH)
        
    def beginProcessing(self):
        pass
    
    def getFile(self):
        pass
    
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
