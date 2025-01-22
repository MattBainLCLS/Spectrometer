from PyQt6 import QtWidgets, QtCore, QtGui

import numpy as np

class FROGTimeDelayControls(QtWidgets.QWidget):

    time_delays_updated = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        start_stop_time_validator = QtGui.QDoubleValidator()

        start_label = QtWidgets.QLabel("Start: ")
        self.start_time = QtWidgets.QLineEdit("0")
        self.start_time.setValidator(start_stop_time_validator)
        start_unit_label = QtWidgets.QLabel(" ps ")

        stop_time_label = QtWidgets.QLabel(" Stop: ")
        self.stop_time = QtWidgets.QLineEdit("1")
        self.stop_time.setValidator(start_stop_time_validator)
        stop_unit_label = QtWidgets.QLabel(" ps ")

        num_samples_label = QtWidgets.QLabel(" N Samples: ")
        self.num_samples = QtWidgets.QLineEdit("128")
        num_samples_validator = QtGui.QIntValidator()
        num_samples_validator.setBottom(2)
        self.num_samples.setValidator(num_samples_validator)

        time_resolution_label = QtWidgets.QLabel(" dT: ")
        self.time_resolution = QtWidgets.QLabel()
        time_resolution_unit = QtWidgets.QLabel(" fs ")

        FROGTimeDelayControlslayout = QtWidgets.QHBoxLayout()

        FROGTimeDelayControlslayout.addWidget(start_label)
        FROGTimeDelayControlslayout.addWidget(self.start_time)
        FROGTimeDelayControlslayout.addWidget(start_unit_label)

        FROGTimeDelayControlslayout.addWidget(stop_time_label)
        FROGTimeDelayControlslayout.addWidget(self.stop_time)
        FROGTimeDelayControlslayout.addWidget(stop_unit_label)

        FROGTimeDelayControlslayout.addWidget(num_samples_label)
        FROGTimeDelayControlslayout.addWidget(self.num_samples)

        FROGTimeDelayControlslayout.addWidget(time_resolution_label)
        FROGTimeDelayControlslayout.addWidget(self.time_resolution)
        FROGTimeDelayControlslayout.addWidget(time_resolution_unit)

        self.start_time.editingFinished.connect(self.generate)
        self.stop_time.editingFinished.connect(self.generate)
        self.num_samples.editingFinished.connect(self.generate)


        self.setLayout(FROGTimeDelayControlslayout)

        self.generate()

    
    def generate(self):
        start = float(self.start_time.text())
        stop = float(self.stop_time.text())

        self.times = np.linspace(start, stop, int(self.num_samples.text()))

        dt = (np.abs(self.times[1] - self.times[0]))*1000

        self.time_resolution.setText("%.3f" % (dt))

        self.time_delays_updated.emit()


    def __del__(self):
        pass
         