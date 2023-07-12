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

class LiveAcquire(QtCore.QObject):
    finished = QtCore.pyqtSignal()  
    progress = QtCore.pyqtSignal(list)  

    def __init__(self, MySpectrometer):
        super().__init__()
        self.Spectrometer = MySpectrometer

    def run(self):
        for i in range(1,10):
            self.progress.emit(self.grab())
            time.sleep(1)

    def grab(self):
        self.Spectrometer.start_exposure(1)
        while not self.Spectrometer.available_spectra:
            time.sleep(0.01)
        return self.Spectrometer.get_spectrum_data().Spectrum # Get spectrum with meta data


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Initialize window

        self.setWindowTitle("QMini Spectrometer Interface")
        
        layout_exposure_button = QtWidgets.QHBoxLayout()
        exposure_title = QtWidgets.QLabel()
        self.exposure_field = QtWidgets.QLineEdit()
        self.exposure_field.returnPressed.connect(self.update_exposure)
        exposure_unit = QtWidgets.QLabel()
        exposure_title.setText("Exposure: ")
        exposure_unit.setText("s")
        layout_exposure_button.addWidget(exposure_title)
        layout_exposure_button.addWidget(self.exposure_field)
        layout_exposure_button.addWidget(exposure_unit)

        
        layout_averaging_button = QtWidgets.QHBoxLayout()
        averaging_title = QtWidgets.QLabel()
        self.averaging_field = QtWidgets.QLineEdit()
        self.averaging_field.returnPressed.connect(self.update_averaging)
        averaging_unit = QtWidgets.QLabel()
        averaging_title.setText("Averaging: ")
        averaging_unit.setText(" spectra")
        layout_averaging_button.addWidget(averaging_title)
        layout_averaging_button.addWidget(self.averaging_field)
        layout_averaging_button.addWidget(averaging_unit)

        layout_settings = QtWidgets.QVBoxLayout()
        layout_settings.addLayout(layout_exposure_button)
        layout_settings.addLayout(layout_averaging_button)

        controllayout = QtWidgets.QVBoxLayout()

        button_layout = QtWidgets.QHBoxLayout()

        page_layout = QtWidgets.QHBoxLayout()

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
        controllayout.addWidget(self.sc)
        controllayout.addLayout(button_layout)

        page_layout.addLayout(controllayout, stretch=1)
        page_layout.addLayout(layout_settings, stretch=0)

        widget = QtWidgets.QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

        # Initialize Spectrometer

        self.start_spectrometer()
        
        # Finalize
        self.mythread = QtCore.QThread()
        self.worker = LiveAcquire(self.Spectrometer)
        self.worker.moveToThread(self.mythread)

        self.mythread.started.connect(self.worker.run)

        self.worker.finished.connect(self.mythread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.mythread.finished.connect(self.mythread.deleteLater)
        self.worker.progress.connect(self.update_plot)

        self.mythread.start()
        print('here')

        #
        
        self.show()

    def start_spectrometer(self):
        devices = Qseries.search_devices()

        self.Spectrometer = Qseries(devices[0])

        self.Spectrometer.open()

        self.nm = self.Spectrometer.get_wavelengths()
        #print(self.Spectrometer.exposure_time)
        self.exposure_field.setText(str(self.Spectrometer.exposure_time))
        self.Spectrometer.processing_steps = SpectrometerProcessing.AdjustOffset # only adjust offset
        self.averaging_field.setText(str(self.Spectrometer.averaging))

        self.line, = self.sc.axes.plot(self.nm, np.zeros(np.size(self.nm)))

        

    def update_plot(self, yvals):
        #self.sc.axes.plot(xvals, yvals)
        #self.line.set_xdata(xvals)
        self.line.set_ydata(yvals)
        self.sc.axes.set_ylim(0, 1.1*np.max(yvals))
        self.sc.draw()
        #self.cfig.canvas.draw_idle()

    def update_exposure(self):
        pass
        #self.Spectrometer.exposure_time = float(self.exposure_field.text())
        #print(self.Spectrometer.exposure_time)

    def grab(self):
        self.Spectrometer.start_exposure(1)
        while not self.Spectrometer.available_spectra:
            time.sleep(0.01)
        spec = self.Spectrometer.get_spectrum_data() # Get spectrum with meta data
        self.update_plot(self.nm, spec.Spectrum)
        self.show()

    def update_averaging(self):
        self.Spectrometer.averaging = int(self.averaging_field.text())
        print(self.Spectrometer.averaging)

    def close(self):
        try:
            self.Spectrometer
        except AttributeError:
            print("Doesn't exist")
        else:
            print("Exists")
            self.Spectrometer.close()
        

        print('Closing...')
        sys.exit()



app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()