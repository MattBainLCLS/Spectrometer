from PyQt6 import QtCore, QtWidgets, QtGui
from . import frog_widgets
#from ._ui_spectrometer import *
import ui

import hardware.spectrometers
import hardware.motion

import numpy as np
import time


class ui_FROG(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.spectrometer_window = ui.ui_Spectrometer()
        self.delay_stage_window = ui.ui_MotionStage()


        self.frog_plot = frog_widgets.FrogPlot()
        self.frog_time_controls = frog_widgets.FROGTimeDelayControls()
        self.frog_controls = frog_widgets.FROGControls()

        self.run_button = QtWidgets.QPushButton()
        self.run_button.setText("Run")
        self.run_button.clicked.connect(self.run_frog)

        self.frog_layout = QtWidgets.QVBoxLayout()
        
        self.frog_layout.addWidget(self.frog_plot)
        self.frog_layout.addWidget(self.frog_controls)
        self.frog_layout.addWidget(self.frog_time_controls)
        self.frog_layout.addWidget(self.run_button)



        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.spectrometer_window)
        layout.addLayout(self.frog_layout)
        layout.addWidget(self.delay_stage_window)

        ### DELETE
        self.wavelengths = np.linspace(200, 1000, 512)

        self.spectrometer_window.spectrometer_connected.connect(self.on_spectrometer_connected)
        self.delay_stage_window.delay_stage_connected.connect(self.on_delay_stage_connected)

        self.frog_time_controls.time_delays_updated.connect(self.reset_plot)


        self.setLayout(layout)

        self.run_button.setEnabled(False)

    def on_spectrometer_connected(self):
        print("Here")
        self.wavelengths = self.spectrometer_window.spectrometer.wavelengths

        if self.delay_stage_window.delay_stage is not None:
            print("Spec Enabling Button")
            self.run_button.setEnabled(True)
        
        self.reset_plot()

    def on_delay_stage_connected(self):

        if self.spectrometer_window.spectrometer is not None:
            print("DS Enabling Button")
            self.run_button.setEnabled(True)

    def reset_plot(self):

        self.times = self.frog_time_controls.times

        X, Y = np.meshgrid(self.wavelengths, self.times)


        self.data = np.zeros(X.shape)

        print("data shape")
        print(self.data.shape)



        self.frog_mesh = self.frog_plot.frog_axes.pcolormesh(X, Y, self.data)
        self.frog_plot.frog_axes.set_xlim(np.min(self.wavelengths), np.max(self.wavelengths))
        self.frog_plot.frog_axes.set_ylim(np.min(self.times), np.max(self.times))
        self.frog_plot.fig.canvas.draw()

    def run_frog(self):
        print("Running Frog")

        X, Y = np.meshgrid(self.wavelengths, self.times)

        for i, time_delay in enumerate(self.frog_time_controls.times):
            self.delay_stage_window.goto_edit.setText("%.4f" % time_delay)
            self.delay_stage_window.onChangedGoto()
            test_data = self.spectrometer_window.on_clicked_grab()
            self.data[i, :] = test_data
            self.frog_mesh.remove()
            self.frog_mesh = self.frog_plot.frog_axes.pcolormesh(X, Y, self.data)
            self.frog_mesh.set_array(self.data)
            self.frog_plot.fig.canvas.draw()
            QtGui.QGuiApplication.processEvents()
        

    def __del__(self):
        pass

        

