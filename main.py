from rgbdriverkit.qseriesdriver import Qseries
from rgbdriverkit.calibratedspectrometer import SpectrometerProcessing

import sys

import numpy as np
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

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("QMini Spectrometer Interface")

        devices = Qseries.search_devices()

        self.Spectrometer = Qseries(devices[0])

        self.Spectrometer.open()

        self.nm = self.Spectrometer.get_wavelengths()
        self.Spectrometer.exposure_time = 0.1 # in seconds
        self.Spectrometer.processing_steps = SpectrometerProcessing.AdjustOffset # only adjust offset
        

        pagelayout = QtWidgets.QVBoxLayout()

        button_layout = QtWidgets.QHBoxLayout()

        grabButton = QtWidgets.QPushButton("Grab", self)
        grabButton.clicked.connect(self.grab)

        closeButton = QtWidgets.QPushButton("Close", self)
        closeButton.clicked.connect(self.close)

        button_layout.addWidget(grabButton)
        button_layout.addWidget(closeButton)

        #graph_layout = QtWidgets.QHBoxLayout()
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        #graph_layout.addWidget(self.sc)
        

        #pagelayout.addLayout(graph_layout)
        pagelayout.addWidget(self.sc)
        pagelayout.addLayout(button_layout)

        widget = QtWidgets.QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        self.line, = self.sc.axes.plot(self.nm, self.nm)

        self.show()

        

    def update_plot(self, xvals, yvals):
        #self.sc.axes.plot(xvals, yvals)
        self.line.set_xdata(xvals)
        self.line.set_ydata(yvals)
        self.sc.axes.set_ylim(0, 1.1*np.max(yvals))
        self.sc.draw()
        #self.cfig.canvas.draw_idle()

    def grab(self):
        self.Spectrometer.start_exposure(1)
        while not self.Spectrometer.available_spectra:
            time.sleep(0.01)
        spec = self.Spectrometer.get_spectrum_data() # Get spectrum with meta data
        self.update_plot(self.nm, spec.Spectrum)
        self.show()

    def close(self):
        self.Spectrometer.close()
        print('Closing...')
        sys.exit()



app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()