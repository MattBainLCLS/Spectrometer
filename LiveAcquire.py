from PyQt6 import QtCore
import numpy as np
from Spectrometer import Spectrometer
import time

class LiveAcquire(QtCore.QObject):

    spectrum = QtCore.pyqtSignal(np.ndarray)
    finished = QtCore.pyqtSignal()  
    
    def __init__(self, Spectrometer = None):
        super().__init__()

    
        if Spectrometer == None:
            Spectrometer = Spectrometer()
        self.Spectrometer = Spectrometer

        self.running = False
        self.paused = True
        self.processing = 0

    def run(self):
        self.running = True

        while self.running:
            #self.Spectrometer.processing_steps = self.processing
            if self.paused:
                time.sleep(0.1)
            else:
                self.spectrum.emit(self.grab())

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
    
    def go(self):
        self.running = True

    def end(self):
        self.running = False

    def update_processing(self, num):
        self.processing = num

    def grab(self):
        return self.Spectrometer.grab()