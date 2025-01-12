from PyQt6 import QtCore, QtWidgets, QtGui
from . import spectrometer_widgets
from ._ui_spectrometer import *

import hardware.spectrometers

import numpy as np

from pulse import *

## 

import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
matplotlib.use('QtAgg')

class PulseDiagnosticPlot(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.temporal_axes = self.fig.add_subplot()
        self.temporal_axes.set_xlabel("Time / ps")
        super(PulseDiagnosticPlot, self).__init__(self.fig)

        self.pos_click_x = None
        self.pos_click_y = None
        self.pos_release_x = None
        self.pos_release_y = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.pos_click_x = event.pos().x()/100
            self.pos_click_y = event.pos().y()/100
        else:
            pass
        
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.pos_release_x = event.pos().x()/100
            self.pos_release_y = event.pos().y()/100

            fig_width_x0 = 0
            fig_width_x1 = self.fig.get_figwidth()
            fig_width_y0 = 0
            fig_width_y1 = self.fig.get_figheight()

            x_bound_lower = self.temporal_axes.get_position().x0*fig_width_x1
            x_bound_upper = self.temporal_axes.get_position().x1*fig_width_x1
            y_bound_lower = self.temporal_axes.get_position().y0*fig_width_y1
            y_bound_upper = self.temporal_axes.get_position().y1*fig_width_y1

            ### Scale X
            if (self.pos_click_x > x_bound_lower) & (self.pos_click_x < x_bound_upper) & (self.pos_release_x > x_bound_lower) & (self.pos_release_x < x_bound_upper):

                xclick = (self.pos_click_x - x_bound_lower) / (x_bound_upper - x_bound_lower)
                xrelease = (self.pos_release_x - x_bound_lower) / (x_bound_upper - x_bound_lower)
                new_xlim_lower = (min([xclick, xrelease]) * (self.temporal_axes.get_xlim()[1] - self.temporal_axes.get_xlim()[0])) + self.temporal_axes.get_xlim()[0]
                new_xlim_upper = (max([xclick, xrelease]) * (self.temporal_axes.get_xlim()[1] - self.temporal_axes.get_xlim()[0])) + self.temporal_axes.get_xlim()[0]

                self.temporal_axes.set_xlim([new_xlim_lower, new_xlim_upper])
            ### Scale Y
            if (self.pos_click_y > y_bound_lower) & (self.pos_click_y < y_bound_upper) & (self.pos_release_y > y_bound_lower) & (self.pos_release_y < y_bound_upper):

                yclick = (self.pos_click_y - y_bound_lower) / (y_bound_upper - y_bound_lower)
                yrelease = (self.pos_release_y - y_bound_lower) / (y_bound_upper - y_bound_lower)
                new_ylim_lower = (min([yclick, yrelease]) * (self.temporal_axes.get_ylim()[1] - self.temporal_axes.get_ylim()[0])) + self.temporal_axes.get_ylim()[0]
                new_ylim_upper = (max([yclick, yrelease]) * (self.temporal_axes.get_ylim()[1] - self.temporal_axes.get_ylim()[0])) + self.temporal_axes.get_ylim()[0]
    
                self.temporal_axes.set_ylim([new_ylim_lower, new_ylim_upper])
                
            self.draw()
        else:
            pass


class ui_PulseMeasure(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.spectrometer_window = ui_Spectrometer()

        self.pulse_diagnostic_figure = PulseDiagnosticPlot(self, width=5, height=4, dpi=100)

        grid_size_layout = QtWidgets.QHBoxLayout()
        grid_size_label = QtWidgets.QLabel("Grid size: ")
        self.grid_size_field = QtWidgets.QLineEdit()
        grid_size_validator = QtGui.QIntValidator()
        grid_size_validator.setBottom(64)
        self.grid_size_field.setValidator(grid_size_validator)
        self.grid_size_field.setText("4096")

        grid_size_layout.addWidget(grid_size_label)
        grid_size_layout.addWidget(self.grid_size_field)


        time_span_layout = QtWidgets.QHBoxLayout()
        time_span_label = QtWidgets.QLabel("Time span: ")
        self.time_span_field = QtWidgets.QLineEdit()
        time_span_field_validator = QtGui.QDoubleValidator()
        time_span_field_validator.setBottom(0.001)
        self.time_span_field.setValidator(time_span_field_validator)
        time_span_unit = QtWidgets.QLabel(" fs")
        self.time_span_field.setText("1000")
        self.time_span_field.editingFinished.connect(self.on_time_span_text_edited)

        time_span_layout.addWidget(time_span_label)
        time_span_layout.addWidget(self.time_span_field)
        time_span_layout.addWidget(time_span_unit)


        time_resolution_layout = QtWidgets.QHBoxLayout()
        time_resolution_label = QtWidgets.QLabel("dT: ")
        self.time_resolution_field = QtWidgets.QLineEdit()
        time_resolution_validator = QtGui.QDoubleValidator()
        time_resolution_validator.setBottom(0.001)
        self.time_resolution_field.setValidator(time_resolution_validator)
        time_resolution_unit = QtWidgets.QLabel(" fs")
        self.time_resolution_field.editingFinished.connect(self.on_time_resolution_text_edited)

        time_resolution_layout.addWidget(time_resolution_label)
        time_resolution_layout.addWidget(self.time_resolution_field)
        time_resolution_layout.addWidget(time_resolution_unit)


        central_frequency_layout = QtWidgets.QHBoxLayout()
        central_frequency_label = QtWidgets.QLabel("Carrier frequency: ")
        self.central_frequency_field = QtWidgets.QLineEdit()
        central_frequency_validator = QtGui.QDoubleValidator()
        central_frequency_validator.setBottom(1)
        self.central_frequency_field.setValidator(central_frequency_validator)
        central_frequency_unit =  QtWidgets.QLabel(" THz")
        self.central_frequency_field.editingFinished.connect(self.on_central_frequency_editing_finished)


        field_setup_layout = QtWidgets.QVBoxLayout()
        field_setup_layout.addLayout(grid_size_layout)
        field_setup_layout.addLayout(time_span_layout)
        field_setup_layout.addLayout(time_resolution_layout)


        diagnostic_label = QtWidgets.QLabel("Temporal Profile")
        pulse_diagnostic_layout = QtWidgets.QVBoxLayout()
        pulse_diagnostic_layout.addWidget(diagnostic_label)
        pulse_diagnostic_layout.addWidget(self.pulse_diagnostic_figure)
        pulse_diagnostic_layout.addLayout(field_setup_layout)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.spectrometer_window)
        layout.addLayout(pulse_diagnostic_layout)

        self.setLayout(layout)

        self.pulse = Pulse(int(self.grid_size_field.text()), float(self.time_span_field.text()))

        self.spectrometer_window.spectrometer_connected.connect(self.on_spectrometer_connected)
        self.spectrometer_window.spectrum_received.connect(self.on_spectrum_received)

        self.line = None

    def on_time_span_text_edited(self):
        self.time_resolution_field.setText(str(float(self.time_span_field.text()) / int(self.grid_size_field.text())))
        self.pulse = Pulse(int(self.grid_size_field.text()), float(self.time_span_field.text())*1E-15)


    def on_time_resolution_text_edited(self):
        self.time_span_field.setText(str(int(self.grid_size_field.text()) * float(self.time_resolution_field.text())))
        self.pulse = Pulse(int(self.grid_size_field.text()), float(self.time_span_field.text())*1E-15)

    def on_spectrometer_connected(self):
        self.pulse.set_sample_frequencies(self.spectrometer_window.spectrometer.wavelengths)
        if self.central_frequency_field.text() == "":
            self.central_frequency_field.setText(str(np.divide(np.max(self.pulse.sample_frequencies) + np.min(self.pulse.sample_frequencies), 2)))
        self.line, = self.pulse_diagnostic_figure.temporal_axes.plot(self.pulse.times, np.zeros(np.shape(self.pulse.times)))

    def on_central_frequency_editing_finished(self):
        self.pulse.set_central_frequency(1E12*float(self.central_frequency_field.text()))

    def on_spectrum_received(self, spectrum):
        print("received")
        self.pulse.from_spectrum(spectrum)
        self.update_plot()
    
    def update_plot(self):
        
        self.line.set_xdata(self.pulse.times)
        self.line.set_data(self.pulse.times, np.power(np.abs(self.pulse.Et), 2))
        self.pulse_diagnostic_figure.temporal_axes.set_ylim(0, 1.1*np.max(self.line.get_ydata()))
        self.pulse_diagnostic_figure.draw()
