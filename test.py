from Spectrometer import Spectrometer
import numpy as np

mySpectrometer = Spectrometer()

spectrum = mySpectrometer.grab()
wavelengths = mySpectrometer.get_wavelengths()
print(np.shape(spectrum))
print(np.shape(wavelengths))