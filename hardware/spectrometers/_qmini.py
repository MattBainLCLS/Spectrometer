import hardware

from hardware.spectrometers.rgbdriverkit.qseriesdriver import Qseries
#from rgbdriverkit.calibratedspectrometer import SpectrometerProcessing, SpectrometerUnits
#from rgbdriverkit import calibratedspectrometer

import numpy as np
import scipy.constants as const

import time

from PyQt6 import QtCore



class QMini():

    spectrum_acquired = QtCore.pyqtSignal(np.ndarray)
    acquisition_finished = QtCore.pyqtSignal()

    def __init__(self, serial = None):

        self.running = False
        self.paused = True

        try:
            devices = Qseries.search_devices(serial)
            self.device = Qseries(devices[0])
        except:
            raise NameError("No hardware devices found.")
        

        self.device.open()

        self.wavelengths = self.device.get_wavelengths()
        self.exposure_time = self.device.exposure_time
        self.averaging = self.device.averaging

        
        self.sample_frequencies = np.divide(const.c, np.multiply(self.nm, 1E-9))

        self.central_frequency = np.divide(np.max(self.sample_frequencies) + np.min(self.sample_frequencies), 2)


    def grab(self):
        self.device.start_exposure(1)
        while not self.device.available_spectra:
            time.sleep(0.01)

        current_spectrum = self.device.get_spectrum_data()
        return np.asarray(current_spectrum.Spectrum) # Get spectrum with meta data
    
    def get_wavelengths(self):
        return self.device.get_wavelengths()
    
    def close(self):
        self.device.close()

    @staticmethod
    def find_devices():

        found_device_list = list()
        try:
            devices = Qseries.search_devices()
        except:
            for device in Qseries.search_devices():
                found_device_list.append(hardware.FoundDevice(manufacturer = device.manufacturer, model = device.product, serial = device.serial_number))
            
        return found_device_list