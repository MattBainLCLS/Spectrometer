from rgbdriverkit.qseriesdriver import Qseries
from rgbdriverkit.calibratedspectrometer import SpectrometerProcessing, SpectrometerUnits
from rgbdriverkit import calibratedspectrometer

import numpy as np
import scipy.constants as const

import time

class Spectrometer():
    def __init__(self):
        devices = Qseries.search_devices()

        self.Spectrometer = Qseries(devices[0])

        self.Spectrometer.open()

        self.nm = self.Spectrometer.get_wavelengths()
        self.exposure_time = self.Spectrometer.exposure_time
        self.averaging = self.Spectrometer.averaging

        
        self.sample_frequencies = np.divide(const.c, self.nm)

    def grab(self):
        self.Spectrometer.start_exposure(1)
        while not self.Spectrometer.available_spectra:
            time.sleep(0.01)

        current_spectrum = self.Spectrometer.get_spectrum_data()
        return np.asarray(current_spectrum.Spectrum) # Get spectrum with meta data
    
    def get_wavelengths(self):
        return self.Spectrometer.get_wavelengths()
    
    def close(self):
        self.Spectrometer.close()