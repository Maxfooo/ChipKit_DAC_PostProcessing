

import threading
import time

class DAC_Experiment(threading.Thread):
    def __init__(self, mcsObj, file, threadID, name="DAC_Experiment", delay=0.2):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.mcs = mcsObj
        self.file = file
        self.delay = delay
        
    def run(self):
        while(self.mcs.checkProgress() == '0'):
            self.mcs.startConversion()
            _sample = self.mcs.readSample()
            while(_sample != "NoSample"):
                self.file.write(str(_sample))
            
            time.sleep(self.delay)
        
                
