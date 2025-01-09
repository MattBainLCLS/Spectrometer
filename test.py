import Spectrometers
import matplotlib.pyplot as plt

#find_Avantes_devices()

spectrometer = Spectrometers.Avantes()

data = spectrometer.grab()

plt.plot(spectrometer.wavelengths, data)
plt.show()


        


