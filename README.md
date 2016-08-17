# ChipKit_DAC_PostProcessing

* Run Analysis.py as main. (set the 'script' variable to 0 for UI or 1 for quickPlots of existing data)
* The UI will run the microcontroller to perform a binary up counter sweep (12 bits) on a DAC, and read back the results.
* The post processing portion of the UI is ready to use, but it will only plot one set at a time right now.
* Load 'Python_DAC_DAQ.pde' and 'Globals.h' onto a chipkit or arduino to run the python code.
* Load the Verilog files (Operating_DAC_Top.v is the toplevel) onto the Terrasic DE0 Nano board
* There is a pinout .csv file "DAC_DAQ_pinout.csv" that you can use to set up the pins for the FPGA
* The project requires:
* Python 3.4+
* Numpy
* Scipy
* Matplotlib
* Chipkit (Arduino) and respective IDE
* Terrasic DE0 Nano Board and Quartus IDE
