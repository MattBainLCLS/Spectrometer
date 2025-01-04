from Spectrometer import Spectrometer
from LiveAcquire import *

import sys
import time
import json

import numpy as np
from PyQt6 import QtCore, QtWidgets, QtGui

from MPLCanvas import *

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
        #layout_settings.addLayout(layout_checkboxes)

        layout_settings_master = QtWidgets.QHBoxLayout()
        layout_settings_master.addLayout(layout_settings)
        layout_settings_master.addLayout(layout_checkboxes)

        controllayout = QtWidgets.QVBoxLayout()

        button_layout = QtWidgets.QHBoxLayout()
        plotting_layout = QtWidgets.QHBoxLayout()

        interact_layout = QtWidgets.QVBoxLayout()

        page_layout = QtWidgets.QVBoxLayout()

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
        page_layout.addLayout(layout_settings_master, stretch=0)

        widget = QtWidgets.QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

        # Initialize Spectrometer

        #self.start_spectrometer()

        self.mySpectrometer = Spectrometer()
        self.line, = self.sc.spectral_axes.plot(self.mySpectrometer.nm, np.zeros(np.size(self.mySpectrometer.nm)))

        
        self.exposure_field.setText(str(self.mySpectrometer.exposure_time))
        self.averaging_field.setText(str(self.mySpectrometer.averaging))

        # Set up Fourier Transform basis
        self.times = np.linspace(-500E-15, 500E-15, 4096)
        self.frequencies = np.fft.fftfreq(4096, abs(self.times[1]-self.times[0]))

        self.plot_time, = self.sc.temporal_axes.plot(self.times, np.zeros(np.size(self.times)))

        # Start threading
        self.mythread = QtCore.QThread()
        #self.worker = LiveAcquire(self.Spectrometer)
        self.worker = LiveAcquire(self.mySpectrometer)

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
        
        #self.current_spectrum = spectrum
        #self.line.set_ydata(spectrum.Spectrum)
        self.line.set_ydata(spectrum)
        #self.temperature_field.setText(str(round(spectrum.Temperature, 2)))
        #self.load_level_field.setText(str(round(spectrum.LoadLevel, 2)))
        #self.sc.spectral_axes.set_ylim(0, 1.1*np.max(spectrum.Spectrum))
        #self.sc.spectral_axes.set_yscale(self.yScale.currentText())
        self.sc.spectral_axes.set_ylim(0, 1.1*np.max(spectrum))
        self.sc.spectral_axes.set_yscale(self.yScale.currentText())

        # Plot Fourier transform
        self.I_frequencies = np.interp(self.frequencies, np.flip(self.mySpectrometer.sample_frequencies), np.flip(spectrum))
        self.E_frequencies = np.sqrt(self.I_frequencies)
        self.E_times = np.fft.fftshift(np.fft.fft(self.E_frequencies))
        self.I_times = np.power(np.abs(self.E_times), 2)
        self.plot_time.set_ydata(self.I_times)
        #self.sc.temporal_axes.set_ylim(0, 1.1*np.max(self.I_times))
        #self.plot_time.set_ylim(0, 1.1*np.max(self.I_times))
        self.sc.draw()

    def reset_axes(self):
        self.sc.spectral_axes.set_xlim([min(self.nm), max(self.nm)])
        self.sc.spectral_axes.set_ylim(0, 1.1*np.max(self.spectrum.Spectrum))
        self.sc.draw()

    def update_exposure(self):
        self.worker.Spectrometer.exposure_time = float(self.exposure_field.text())

    def grab(self):
        #self.MySpectrometer.start_exposure(1)
        #while not self.MySpectrometer.available_spectra:
        #    time.sleep(0.01)
        #spec = self.Spectrometer.get_spectrum_data() # Get spectrum with meta data
        spec = self.mySpectrometer.grab()
        print(type(spec))
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
            self.mySpectrometer
        except AttributeError:
            print("Doesn't exist")
        else:
            print("Exists")
            self.worker.end()
            self.mySpectrometer.close()
        

        print('Closing...')
        sys.exit()



app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()