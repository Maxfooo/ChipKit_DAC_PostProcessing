# ChipKit_DAC_PostProcessing


Python

* Run Analysis.py as main. (set the 'script' variable to 0 for UI or 1 for quickPlots of existing data)
* The UI will run the microcontroller to perform a binary up counter sweep (12 bits) on a DAC, and read back the results.
* The post processing portion of the UI is ready to use, but it will only plot one set at a time right now.

Microcontroller (ADC control and communication to computer)

* Load 'Python_DAC_DAQ.pde' and 'Globals.h' onto a chipkit or arduino to run the python code.

FPGA (DAC code output)

* If possible, copy the 'DAC_DAQ.pin' file into the output folder of the Quartus project for operating the DAC
* Then just program the FPGA using the 'DAC_DAQ.sof'
* If this doesn't work try the following:
* Use the Verilog files: 'Operating_DAC_top.v' (toplevel), 'Operating_DAC.v', and 'pushbtnReset.v'
* There is a pinout .csv file "DAC_DAQ_pinout.csv" that you can use to set up the pins for the FPGA

The project requires:

* Python 3.4+
* Numpy
* Scipy
* Matplotlib
* Chipkit (Arduino) and respective IDE
* Terrasic DE0 Nano Board and Quartus IDE
