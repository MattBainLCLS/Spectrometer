from rgbdriverkit.qseriesdriver import Qseries
from rgbdriverkit.calibratedspectrometer import SpectrometerProcessing, SpectrometerUnits
from rgbdriverkit import calibratedspectrometer

import sys
import time
import json

import numpy as np
from PyQt6 import QtCore, QtWidgets, QtGui


import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')

class MplCanvas(FigureCanvasQTAgg):


    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

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

            x_bound_lower = self.axes.get_position().x0*fig_width_x1
            x_bound_upper = self.axes.get_position().x1*fig_width_x1
            y_bound_lower = self.axes.get_position().y0*fig_width_y1
            y_bound_upper = self.axes.get_position().y1*fig_width_y1

            ### Scale X
            if (self.pos_click_x > x_bound_lower) & (self.pos_click_x < x_bound_upper) & (self.pos_release_x > x_bound_lower) & (self.pos_release_x < x_bound_upper):

                xclick = (self.pos_click_x - x_bound_lower) / (x_bound_upper - x_bound_lower)
                xrelease = (self.pos_release_x - x_bound_lower) / (x_bound_upper - x_bound_lower)
                new_xlim_lower = (min([xclick, xrelease]) * (self.axes.get_xlim()[1] - self.axes.get_xlim()[0])) + self.axes.get_xlim()[0]
                new_xlim_upper = (max([xclick, xrelease]) * (self.axes.get_xlim()[1] - self.axes.get_xlim()[0])) + self.axes.get_xlim()[0]

                self.axes.set_xlim([new_xlim_lower, new_xlim_upper])
            ### Scale Y
            if (self.pos_click_y > y_bound_lower) & (self.pos_click_y < y_bound_upper) & (self.pos_release_y > y_bound_lower) & (self.pos_release_y < y_bound_upper):

                yclick = (self.pos_click_y - y_bound_lower) / (y_bound_upper - y_bound_lower)
                yrelease = (self.pos_release_y - y_bound_lower) / (y_bound_upper - y_bound_lower)
                new_ylim_lower = (min([yclick, yrelease]) * (self.axes.get_ylim()[1] - self.axes.get_ylim()[0])) + self.axes.get_ylim()[0]
                new_ylim_upper = (max([yclick, yrelease]) * (self.axes.get_ylim()[1] - self.axes.get_ylim()[0])) + self.axes.get_ylim()[0]
    
                self.axes.set_ylim([new_ylim_lower, new_ylim_upper])
                
            self.draw()
        else:
            pass

        

    

class LiveAcquire(QtCore.QObject):
    finished = QtCore.pyqtSignal()  
    spectrum = QtCore.pyqtSignal(calibratedspectrometer.SpectrumData)

    def __init__(self, MySpectrometer):
        super().__init__()
        self.Spectrometer = MySpectrometer
        self.running = False
        self.paused = True
        self.processing = 0

    def run(self):
        self.running = True

        while self.running:
            self.Spectrometer.processing_steps = self.processing
            if self.paused:
                time.sleep(0.1)
            else:
                self.spectrum.emit(self.grab())

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
    
    def go(self):
        self.running = True

    def end(self):
        self.running = False

    def update_processing(self, num):
        self.processing = num

    def grab(self):
        self.Spectrometer.start_exposure(1)
        while not self.Spectrometer.available_spectra:
            time.sleep(0.01)
        return self.Spectrometer.get_spectrum_data() # Get spectrum with meta data


class MainWindow(QtWidgets.QMainWindow):

    #interrupt = QtCore.pyqtSignal()

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

        layout_temperature = QtWidgets.QHBoxLayout()
        temperature_title = QtWidgets.QLabel()
        self.temperature_field = QtWidgets.QLineEdit()
        self.temperature_field.setReadOnly(True)
        temperature_unit = QtWidgets.QLabel()
        temperature_title.setText("Temperature: ")
        temperature_unit.setText(" C")
        layout_temperature.addWidget(temperature_title)
        layout_temperature.addWidget(self.temperature_field)
        layout_temperature.addWidget(temperature_unit)

        layout_load_level = QtWidgets.QHBoxLayout()
        load_level_title = QtWidgets.QLabel()
        self.load_level_field = QtWidgets.QLineEdit()
        self.load_level_field.setReadOnly(True)
        load_level_unit = QtWidgets.QLabel()
        load_level_title.setText("Load Level: ")
        load_level_unit.setText(" Keep < 1")
        layout_load_level.addWidget(load_level_title)
        layout_load_level.addWidget(self.load_level_field)
        layout_load_level.addWidget(load_level_unit)

        ## Calibration check boxes
        layout_checkboxes = QtWidgets.QVBoxLayout()

        self.checkbox_adjust_offset = QtWidgets.QCheckBox("Adjust Offset")
        self.checkbox_adjust_offset.stateChanged.connect(self.set_processing_from_checkboxes)
        self.checkbox_correct_nonlinearity = QtWidgets.QCheckBox("Correct Nonlinearity")
        self.checkbox_correct_nonlinearity.stateChanged.connect(self.set_processing_from_checkboxes)
        self.checkbox_remove_perm_bad_pixels = QtWidgets.QCheckBox("Remove Permanent Bad Pixels")
        self.checkbox_remove_perm_bad_pixels.stateChanged.connect(self.set_processing_from_checkboxes)
        self.checkbox_subtract_dark = QtWidgets.QCheckBox("Subtract Dark")
        self.checkbox_subtract_dark.stateChanged.connect(self.set_processing_from_checkboxes)
        self.checkbox_remove_temp_bad_pixels = QtWidgets.QCheckBox("Remove Temporary Bad Pixels")
        self.checkbox_remove_temp_bad_pixels.stateChanged.connect(self.set_processing_from_checkboxes)
        self.checkbox_compensate_stray_light = QtWidgets.QCheckBox("Compensate Stray Light")
        self.checkbox_compensate_stray_light.stateChanged.connect(self.set_processing_from_checkboxes)
        self.checkbox_normalize_exposure = QtWidgets.QCheckBox("Normalize Exposure Time")
        self.checkbox_normalize_exposure.stateChanged.connect(self.set_processing_from_checkboxes)
        self.checkbox_sensitivity_calibration = QtWidgets.QCheckBox("Sensitivity Calibration")
        self.checkbox_sensitivity_calibration.stateChanged.connect(self.set_processing_from_checkboxes)
        self.checkbox_sensitivity_smoothing = QtWidgets.QCheckBox("Sensitivity Smoothing")
        self.checkbox_sensitivity_smoothing.stateChanged.connect(self.set_processing_from_checkboxes)
        self.checkbox_additional_filtering = QtWidgets.QCheckBox("Additional Filtering")
        self.checkbox_additional_filtering.stateChanged.connect(self.set_processing_from_checkboxes)
        self.checkbox_scale_to_16bit_range = QtWidgets.QCheckBox("Scale to 16 bit range")
        self.checkbox_scale_to_16bit_range.stateChanged.connect(self.set_processing_from_checkboxes)

        layout_checkboxes.addWidget(self.checkbox_adjust_offset)
        layout_checkboxes.addWidget(self.checkbox_correct_nonlinearity)
        layout_checkboxes.addWidget(self.checkbox_remove_perm_bad_pixels)
        layout_checkboxes.addWidget(self.checkbox_subtract_dark)
        layout_checkboxes.addWidget(self.checkbox_remove_temp_bad_pixels)
        layout_checkboxes.addWidget(self.checkbox_compensate_stray_light)
        layout_checkboxes.addWidget(self.checkbox_normalize_exposure)
        layout_checkboxes.addWidget(self.checkbox_sensitivity_calibration)
        layout_checkboxes.addWidget(self.checkbox_sensitivity_smoothing)
        layout_checkboxes.addWidget(self.checkbox_additional_filtering)
        layout_checkboxes.addWidget(self.checkbox_scale_to_16bit_range)

        ##


        layout_settings = QtWidgets.QVBoxLayout()
        layout_settings.addLayout(layout_exposure_button)
        layout_settings.addLayout(layout_averaging_button)
        layout_settings.addLayout(layout_temperature)
        layout_settings.addLayout(layout_load_level)
        layout_settings.addLayout(layout_checkboxes)

        controllayout = QtWidgets.QVBoxLayout()

        button_layout = QtWidgets.QHBoxLayout()
        plotting_layout = QtWidgets.QHBoxLayout()

        interact_layout = QtWidgets.QVBoxLayout()

        page_layout = QtWidgets.QHBoxLayout()

        grabButton = QtWidgets.QPushButton("Grab", self)
        grabButton.clicked.connect(self.grab)

        closeButton = QtWidgets.QPushButton("Close", self)
        closeButton.clicked.connect(self.close)

        self.pauseButton = QtWidgets.QPushButton("Resume", self)
        self.pauseButton.setCheckable(True)
        self.pauseButton.clicked.connect(self.interruptFunc)

        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.clicked.connect(self.save_spectrum)

        self.resetAxesButton = QtWidgets.QPushButton("Reset", self)
        self.resetAxesButton.clicked.connect(self.reset_axes)

        self.yScale = QtWidgets.QComboBox(self)
        self.yScale.addItem('linear')
        self.yScale.addItem('symlog')
        self.yScale.setCurrentText('linear')

        button_layout.addWidget(grabButton)
        button_layout.addWidget(self.pauseButton)
        button_layout.addWidget(self.saveButton)
        button_layout.addWidget(closeButton)

        plotting_layout.addWidget(self.yScale)
        plotting_layout.addWidget(self.resetAxesButton)

        interact_layout.addLayout(button_layout)
        interact_layout.addLayout(plotting_layout)
        
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        controllayout.addWidget(self.sc)
        controllayout.addLayout(interact_layout)

        page_layout.addLayout(controllayout, stretch=1)
        page_layout.addLayout(layout_settings, stretch=0)

        widget = QtWidgets.QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

        # Initialize Spectrometer

        self.start_spectrometer()

        
        # Start threading
        self.mythread = QtCore.QThread()
        self.worker = LiveAcquire(self.Spectrometer)

        self.set_checkboxes_from_number(847)
        self.set_processing_from_checkboxes()


        self.worker.moveToThread(self.mythread)
        self.mythread.started.connect(self.worker.run)

        self.worker.finished.connect(self.mythread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.mythread.finished.connect(self.mythread.deleteLater)
        self.worker.spectrum.connect(self.update_plot)

        self.mythread.start()
        
        self.show()

    

    def start_spectrometer(self):
        devices = Qseries.search_devices()

        self.Spectrometer = Qseries(devices[0])

        self.Spectrometer.open()

        self.nm = self.Spectrometer.get_wavelengths()
        self.exposure_field.setText(str(self.Spectrometer.exposure_time))
        self.averaging_field.setText(str(self.Spectrometer.averaging))

        self.line, = self.sc.axes.plot(self.nm, np.zeros(np.size(self.nm)))

    def set_checkboxes_from_number(self, number):
        my_binary = str(format(number, '011b'))[::-1]
        self.checkbox_adjust_offset.setChecked(int(my_binary[0]))
        self.checkbox_correct_nonlinearity.setChecked(int(my_binary[1]))
        self.checkbox_remove_perm_bad_pixels.setChecked(int(my_binary[2]))
        self.checkbox_subtract_dark.setChecked(int(my_binary[3]))
        self.checkbox_remove_temp_bad_pixels.setChecked(int(my_binary[4]))
        self.checkbox_compensate_stray_light.setChecked(int(my_binary[5]))
        self.checkbox_normalize_exposure.setChecked(int(my_binary[6]))
        self.checkbox_sensitivity_calibration.setChecked(int(my_binary[7]))
        self.checkbox_sensitivity_smoothing.setChecked(int(my_binary[8]))
        self.checkbox_additional_filtering.setChecked(int(my_binary[9]))
        self.checkbox_scale_to_16bit_range.setChecked(int(my_binary[10]))
    
    def set_processing_from_checkboxes(self):
        binary = ""
        binary += str(int(self.checkbox_adjust_offset.isChecked())) 
        binary += str(int(self.checkbox_correct_nonlinearity.isChecked()))
        binary += str(int(self.checkbox_remove_perm_bad_pixels.isChecked()))
        binary += str(int(self.checkbox_subtract_dark.isChecked()))
        binary += str(int(self.checkbox_remove_temp_bad_pixels.isChecked()))
        binary += str(int(self.checkbox_compensate_stray_light.isChecked()))
        binary += str(int(self.checkbox_normalize_exposure.isChecked()))
        binary += str(int(self.checkbox_sensitivity_calibration.isChecked()))
        binary += str(int(self.checkbox_sensitivity_smoothing.isChecked()))
        binary += str(int(self.checkbox_additional_filtering.isChecked()))
        binary += str(int(self.checkbox_scale_to_16bit_range.isChecked()))

        self.worker.update_processing(int(binary[::-1], 2))


    def update_plot(self, spectrum):
        
        self.current_spectrum = spectrum
        self.line.set_ydata(spectrum.Spectrum)
        self.temperature_field.setText(str(round(spectrum.Temperature, 2)))
        self.load_level_field.setText(str(round(spectrum.LoadLevel, 2)))
        self.sc.axes.set_ylim(0, 1.1*np.max(spectrum.Spectrum))
        self.sc.axes.set_yscale(self.yScale.currentText())
        self.sc.draw()

    def reset_axes(self):
        self.sc.axes.set_xlim([min(self.nm), max(self.nm)])
        self.sc.axes.set_ylim(0, 1.1*np.max(self.spectrum.Spectrum))
        self.sc.draw()

    def update_exposure(self):
        self.worker.Spectrometer.exposure_time = float(self.exposure_field.text())

    def grab(self):
        self.Spectrometer.start_exposure(1)
        while not self.Spectrometer.available_spectra:
            time.sleep(0.01)
        spec = self.Spectrometer.get_spectrum_data() # Get spectrum with meta data
        self.update_plot(spec)
        self.show()

    def update_averaging(self):
        self.worker.Spectrometer.averaging = int(self.averaging_field.text())

    def interruptFunc(self):
        if self.pauseButton.isChecked():
            self.worker.resume()
            self.pauseButton.setText("Pause")
        else:
            self.worker.pause()
            self.pauseButton.setText("Resume")

    def save_spectrum(self):
        data_to_save = {
            "Timestamp": str(self.current_spectrum.TimeStamp),
            "Wavelengths": self.nm,
            "Intensities": self.current_spectrum.Spectrum
        }
        print(self.current_spectrum.TimeStamp)

        json_obj = json.dumps(data_to_save)
        outfile, _ = QtWidgets.QFileDialog.getSaveFileName()
        if outfile:
            with open(outfile, "w") as f:
                f.write(json_obj)

    def close(self):
        try:
            self.Spectrometer
        except AttributeError:
            print("Doesn't exist")
        else:
            print("Exists")
            self.worker.end()
            self.Spectrometer.close()
        

        print('Closing...')
        sys.exit()



app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()