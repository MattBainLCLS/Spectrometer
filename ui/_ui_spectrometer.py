from PyQt6 import QtCore, QtWidgets, QtGui
#import ui_spectrometer._ui_spectrometer_plot as _ui_spectrometer_plot
#import _ui_spectrometer_plot
#import _ui_connect_spectrometer

#import ui_spectrometer._ui_connect_spectrometer as _ui_connect_spectrometer
from . import spectrometer_widgets

import hardware.spectrometers

import json
import numpy as np



class ui_Spectrometer(QtWidgets.QWidget):

    spectrometer_connected = QtCore.pyqtSignal()
    spectrum_received = QtCore.pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()

        # Initialize window

        self.setWindowTitle("Spectrometer")

        self.button_connect = QtWidgets.QPushButton()
        self.button_connect.setText("Connect")
        self.button_connect.setStyleSheet("color: #4ECE44")
        # Todo add connected light
        layout_connect = QtWidgets.QHBoxLayout()
        layout_connect.addWidget(self.button_connect)

        self.button_connect.clicked.connect(self.on_clicked_connect)


        # Custom Widgets
        
        self.mybuttons = spectrometer_widgets.SpectrometerButtons()
        self.mybuttons.grabButton.clicked.connect(self.on_clicked_grab)
        self.mybuttons.pauseButton.clicked.connect(self.on_clicked_run)
        self.mybuttons.setEnabled(False)

        self.plotting_controls = spectrometer_widgets.PlottingControls()
        self.plotting_controls.button_reset_axes.clicked.connect(self.reset_axes)
        self.plotting_controls.setEnabled(False)

        self.acquisition_controls = spectrometer_widgets.AcquisitionControls()
        self.acquisition_controls.averaging_field.editingFinished.connect(self.on_averaging_changed)
        self.acquisition_controls.exposure_field.editingFinished.connect(self.on_exposure_updated)

        
        self.spectrum_figure = spectrometer_widgets.SpectrometerPlot(self, width=5, height=4, dpi=100)
        

        # controllayout.addWidget(self.sc)
        # controllayout.addLayout(interact_layout)

        page_layout = QtWidgets.QVBoxLayout()

        page_layout.addWidget(self.button_connect)
        page_layout.addWidget(self.spectrum_figure)
        page_layout.addWidget(self.mybuttons)
        page_layout.addWidget(self.plotting_controls)
        page_layout.addWidget(self.acquisition_controls)

        self.setLayout(page_layout)

        # Set Defaults
        

        # Create a thread on which to run the spectrometer

        self.spectrometer_thread = QtCore.QThread(parent=self)

        # # Initialize Spectrometer

        # #self.start_spectrometer()

        # self.mySpectrometer = Spectrometer()
        # self.line, = self.sc.spectral_axes.plot(self.mySpectrometer.nm, np.zeros(np.size(self.mySpectrometer.nm)))

        
        # self.exposure_field.setText(str(self.mySpectrometer.exposure_time))
        # self.averaging_field.setText(str(self.mySpectrometer.averaging))

        # # Set up Fourier Transform basis
        # self.times = np.linspace(-500E-15, 500E-15, 4096)
        # self.frequencies = np.fft.fftshift(np.fft.fftfreq(4096, abs(self.times[1]-self.times[0])))
        # self.I_frequencies = np.zeros(np.size(self.times))

        # self.plot_time, = self.sc.temporal_axes.plot(self.times, self.I_frequencies)

        # Start threading
        
        # self.worker = LiveAcquire(self.mySpectrometer)
        # self.set_checkboxes_from_number(847)
        # self.set_processing_from_checkboxes()

        # self.worker.moveToThread(self.mythread)
        # self.mythread.started.connect(self.worker.run)
        # self.worker.finished.connect(self.mythread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.mythread.finished.connect(self.mythread.deleteLater)
        # self.worker.spectrum.connect(self.update_plot)
        # self.mythread.start()
        # #self.show()

        self.spectrometer = None

    def on_clicked_connect(self):
        
        if self.button_connect.text() == "Connect":
            self.window_connect_spectrometer = spectrometer_widgets.ui_ConnectSpectrometer()
            self.window_connect_spectrometer.device_found.connect(self.on_device_selected)
            self.window_connect_spectrometer.show()

        elif self.button_connect.text() == "Disconnect":
            try:
                # Todo: disconnect spectrometer
                print("disconnecting")
                self.spectrometer.end()
                #self.delay_stage.close()
                #self.delay_stage = None
                self.button_connect.setText("Connect")
                self.button_connect.setStyle("color: #4ECE44")
            except:
                print("Disconnection Failed")
                exit()
            else:
                print("Disconnected successfully.")
                self.button_connect.setText("Connect")
                self.button_connect.setStyleSheet("color: #4ECE44")
                # self.button_home.setEnabled(False)
                # self.goto_edit.setEnabled(False)
                # self.jog_size_edit.setEnabled(False)
                # self.button_jog_backward.setEnabled(False)
                # self.button_jog_forward.setEnabled(False)

    def on_device_selected(self, device):

        print(device.manufacturer)

        try:
            match device.manufacturer:
                case "dummy":
                    self.spectrometer = hardware.spectrometers.Dummy()
                case "Avantes":
                    self.spectrometer = hardware.spectrometers.Avantes(device.serial)
                case "Broadcom":
                    self.spectrometer = hardware.spectrometers.QMini(device.serial)
        except:
            print("connection Failed")
        else:
            print("Connected successfully!")
            self.button_connect.setText("Disconnect")
            self.button_connect.setStyleSheet("color: #B91B1B")

            self.spectrometer.set_exposure(float(self.acquisition_controls.exposure_field.text()))

            self.spectrum_buffer = hardware.spectrometers.SpectrumBuffer(self.spectrometer.number_of_pixels, int(self.acquisition_controls.averaging_field.text()))

            self.line, = self.spectrum_figure.spectral_axes.plot(self.spectrometer.wavelengths, np.zeros(np.shape(self.spectrometer.wavelengths)))
            self.reset_axes()
            self.spectrum_figure.spectral_axes.set_ylim([0, 1])
            
            # Enable controls
            self.mybuttons.setEnabled(True)
            self.plotting_controls.setEnabled(True)

            self.spectrometer.moveToThread(self.spectrometer_thread)
            self.spectrometer_thread.started.connect(self.spectrometer.run)
            self.spectrometer.acquisition_finished.connect(self.spectrometer_thread.quit)
            self.spectrometer.acquisition_finished.connect(self.spectrometer.deleteLater)
            self.spectrometer_thread.finished.connect(self.spectrometer_thread.deleteLater)
            self.spectrometer.spectrum_acquired.connect(self.update_plot)
            self.spectrometer_thread.start()

            self.spectrometer_connected.emit()


    def on_clicked_grab(self):
        spectrum = self.spectrometer.grab()
        self.spectrum_buffer.append_spectrum(spectrum)
        self.update_plot(self.spectrum_buffer.mean())
        return spectrum
        

    def on_clicked_run(self):
        if self.mybuttons.pauseButton.isChecked():
            self.spectrometer.resume()
            self.mybuttons.pauseButton.setText("Pause")
        else:
            self.spectrometer.pause()
            self.mybuttons.pauseButton.setText("Resume")

    def update_plot(self, spectrum):
        if self.plotting_controls.button_normalize.isChecked():
            try:
                spectrum = np.divide(spectrum, np.max(spectrum))
            except:
                spectrum = spectrum

        self.spectrum_received.emit(spectrum)
        self.line.set_ydata(spectrum)

        if self.plotting_controls.button_autoscale.isChecked():
            self.spectrum_figure.spectral_axes.set_ylim(0, 1.1*np.max(self.line.get_ydata()))
        
        self.spectrum_figure.spectral_axes.set_yscale(self.plotting_controls.combo_y_scale.currentText())
        self.spectrum_figure.draw()

    def on_averaging_changed(self):
        self.spectrum_buffer.resize(int(self.acquisition_controls.averaging_field.text()))

    def on_exposure_updated(self):
        self.spectrometer.set_exposure(float(self.acquisition_controls.exposure_field.text()))



    # def set_checkboxes_from_number(self, number):
    #     my_binary = str(format(number, '011b'))[::-1]
    #     self.checkbox_adjust_offset.setChecked(int(my_binary[0]))
    #     self.checkbox_correct_nonlinearity.setChecked(int(my_binary[1]))
    #     self.checkbox_remove_perm_bad_pixels.setChecked(int(my_binary[2]))
    #     self.checkbox_subtract_dark.setChecked(int(my_binary[3]))
    #     self.checkbox_remove_temp_bad_pixels.setChecked(int(my_binary[4]))
    #     self.checkbox_compensate_stray_light.setChecked(int(my_binary[5]))
    #     self.checkbox_normalize_exposure.setChecked(int(my_binary[6]))
    #     self.checkbox_sensitivity_calibration.setChecked(int(my_binary[7]))
    #     self.checkbox_sensitivity_smoothing.setChecked(int(my_binary[8]))
    #     self.checkbox_additional_filtering.setChecked(int(my_binary[9]))
    #     self.checkbox_scale_to_16bit_range.setChecked(int(my_binary[10]))
    
    # def set_processing_from_checkboxes(self):
    #     binary = ""
    #     binary += str(int(self.checkbox_adjust_offset.isChecked())) 
    #     binary += str(int(self.checkbox_correct_nonlinearity.isChecked()))
    #     binary += str(int(self.checkbox_remove_perm_bad_pixels.isChecked()))
    #     binary += str(int(self.checkbox_subtract_dark.isChecked()))
    #     binary += str(int(self.checkbox_remove_temp_bad_pixels.isChecked()))
    #     binary += str(int(self.checkbox_compensate_stray_light.isChecked()))
    #     binary += str(int(self.checkbox_normalize_exposure.isChecked()))
    #     binary += str(int(self.checkbox_sensitivity_calibration.isChecked()))
    #     binary += str(int(self.checkbox_sensitivity_smoothing.isChecked()))
    #     binary += str(int(self.checkbox_additional_filtering.isChecked()))
    #     binary += str(int(self.checkbox_scale_to_16bit_range.isChecked()))

    #     self.worker.update_processing(int(binary[::-1], 2))



    # def update_plot(self, spectrum):
        
    #     #self.current_spectrum = spectrum
    #     #self.line.set_ydata(spectrum.Spectrum)
    #     self.line.set_ydata(spectrum)
    #     #self.temperature_field.setText(str(round(spectrum.Temperature, 2)))
    #     #self.load_level_field.setText(str(round(spectrum.LoadLevel, 2)))
    #     #self.sc.spectral_axes.set_ylim(0, 1.1*np.max(spectrum.Spectrum))
    #     #self.sc.spectral_axes.set_yscale(self.yScale.currentText())
    #     self.sc.spectral_axes.set_ylim(0, 1.1*np.max(spectrum))
    #     self.sc.spectral_axes.set_yscale(self.yScale.currentText())

    #     # Plot Fourier transform
    #     #   Jacobian xform
    #     self.sample_frequency_Is = spectrum
   
    #     #   Interpolation subtracting central frequency
    #     self.I_frequencies = np.interp(self.frequencies, np.flip(self.mySpectrometer.sample_frequencies - self.mySpectrometer.central_frequency), np.flip(self.sample_frequency_Is))

    #     self.I_frequencies[np.argwhere(self.I_frequencies < 0.05*np.max(self.I_frequencies))] = 0
    #     self.E_frequencies = np.sqrt(self.I_frequencies - np.min(self.I_frequencies))

    #     self.E_times = np.fft.fftshift(np.fft.ifft(self.E_frequencies))

    #     self.I_times = np.power(np.abs(self.E_times), 2)
    #     self.plot_time.set_ydata(self.I_times)

    #     self.sc.temporal_axes.set_ylim(0, 1.1*np.max(self.I_times))
    #     self.sc.temporal_axes.set_xlim(-50E-15, 50E-15)
    #     #self.plot_time.set_ylim(0, 1.1*np.max(self.I_times))
    #     self.sc.draw()

    def reset_axes(self):
        self.spectrum_figure.spectral_axes.set_xlim([min(self.spectrometer.wavelengths), max(self.spectrometer.wavelengths)])
        try:
            self.spectrum_figure.spectral_axes.set_ylim(0, 1.1*np.max(self.line.get_ydata()))
        except:
            self.spectrum_figure.spectral_axes.set_ylim(0, 1.1)
        self.spectrum_figure.draw()

    # def update_exposure(self):
    #     self.worker.Spectrometer.exposure_time = float(self.exposure_field.text())

    # def grab(self):
    #     #self.MySpectrometer.start_exposure(1)
    #     #while not self.MySpectrometer.available_spectra:
    #     #    time.sleep(0.01)
    #     #spec = self.Spectrometer.get_spectrum_data() # Get spectrum with meta data
    #     spec = self.mySpectrometer.grab()

    #     self.update_plot(spec)
    #     self.show()

    # def update_averaging(self):
    #     self.worker.Spectrometer.averaging = int(self.averaging_field.text())

    # def interruptFunc(self):
    #     if self.pauseButton.isChecked():
    #         self.worker.resume()
    #         self.pauseButton.setText("Pause")
    #     else:
    #         self.worker.pause()
    #         self.pauseButton.setText("Resume")

    # def save_spectrum(self):
    #     data_to_save = {
    #         "Timestamp": str(self.current_spectrum.TimeStamp),
    #         "Wavelengths": self.nm,
    #         "Intensities": self.current_spectrum.Spectrum
    #     }
    #     print(self.current_spectrum.TimeStamp)

    #     json_obj = json.dumps(data_to_save)
    #     outfile, _ = QtWidgets.QFileDialog.getSaveFileName()
    #     if outfile:
    #         with open(outfile, "w") as f:
    #             f.write(json_obj)

    # def close_window(self):
    #     try:
    #         self.mySpectrometer
    #     except AttributeError:
    #         print("Doesn't exist")
    #     else:
    #         print("Exists")
    #         self.worker.end()
    #         self.mySpectrometer.close()
        

    #     print('Closing...')
    #     self.close()

    def closeEvent(self, event):
        try:
            self.spectrometer
        except AttributeError:
            pass
        else:
            self.spectrometer.end()
            self.spectrometer.close()


    def __del__(self):
        self.spectrometer_thread.exit()
        pass