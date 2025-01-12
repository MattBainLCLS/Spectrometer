import hardware

import numpy as np
import scipy.constants as const

import time

from PyQt6 import QtCore



class Dummy(QtCore.QObject):
    spectrum_acquired = QtCore.pyqtSignal(np.ndarray)
    acquisition_finished = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.running = False
        self.paused = True

        self.number_of_pixels = 2048
        self.wavelengths = np.linspace(200, 1100, self.number_of_pixels)

        self.exposure = 10

    def set_exposure(self, exposure_ms):
        self.exposure = exposure_ms

    def grab(self):
        spectrum = np.random.randn(np.size(self.wavelengths))
        # Todo add spectral shape?
        return spectrum
    
    def run(self):
        
        self.running = True

        while self.running:
            #self.Spectrometer.processing_steps = self.processing
            
            if self.paused:
                time.sleep(0.1)
            else:
                time.sleep(self.exposure/1000)
                self.spectrum_acquired.emit(self.grab())

        return

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
    
    def go(self):
        self.running = True

    def end(self):
        self.running = False

    def close(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def find_devices():
        found_device_list = list()
        found_device_list.append(hardware.FoundDevice(manufacturer = "dummy", model = "spectrometer", serial = "00001"))
        found_device_list.append(hardware.FoundDevice(manufacturer = "dummy", model = "spectrometer", serial = "00002"))
        return found_device_list