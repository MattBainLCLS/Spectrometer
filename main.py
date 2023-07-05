from rgbdriverkit.qseriesdriver import Qseries
from rgbdriverkit.calibratedspectrometer import SpectrometerProcessing

import sys
import matplotlib
matplotlib.use('Qt5Agg')

import time






from PyQt6 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, xvals, yvals, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(xvals, yvals)
        self.setCentralWidget(sc)

        self.show()

devices = Qseries.search_devices()

Spectrometer = Qseries(devices[0])

Spectrometer.open()

nm = Spectrometer.get_wavelengths()
Spectrometer.exposure_time = 0.1 # in seconds
print("Starting exposure with t=" + str(Spectrometer.exposure_time) + "s")
Spectrometer.processing_steps = SpectrometerProcessing.AdjustOffset # only adjust offset
Spectrometer.start_exposure(1)
print("Waiting for spectrum...")
while not Spectrometer.available_spectra:
    time.sleep(0.1)

print("Spectrum available")
spec = Spectrometer.get_spectrum_data() # Get spectrum with meta data

Spectrometer.close() # Close device connection

app = QtWidgets.QApplication(sys.argv)
w = MainWindow(nm, spec.Spectrum)
app.exec()