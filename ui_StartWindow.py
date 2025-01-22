from PyQt6 import QtCore, QtWidgets, QtGui

import platform

system = platform.system()

# match system:
#     case "Windows":
#         import ui.spectrometer_widgets as spectrometer_widgets
#         import ui_MotionStage
#     case "Darwin":
#         import ui.spectrometer_widgets as spectrometer_widgets

import ui

class ui_StartWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.spectrometer_window = None
        self.pulse_measure_window = None
        self.delay_stage_window = None
        self.frog_window = None

        self.button_spectrometer = QtWidgets.QPushButton()
        self.button_spectrometer.setText("Spectrometer")
        self.button_spectrometer.setEnabled(False)
        self.button_spectrometer.clicked.connect(self.on_spectrometer_clicked)

        self.button_pulse_measure = QtWidgets.QPushButton()
        self.button_pulse_measure.setText("Pulse Measurement")
        self.button_pulse_measure.setEnabled(False)
        self.button_pulse_measure.clicked.connect(self.on_pulse_measure_clicked)
        
        self.button_delay_stage = QtWidgets.QPushButton()
        self.button_delay_stage.setText("Delay Stage")
        self.button_delay_stage.setEnabled(False)
        self.button_delay_stage.clicked.connect(self.on_delay_stage_clicked)

        self.button_frog = QtWidgets.QPushButton()
        self.button_frog.setText("FROG")
        self.button_frog.setEnabled(False)
        self.button_frog.clicked.connect(self.on_FROG_clicked)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.button_spectrometer)
        layout.addWidget(self.button_pulse_measure)
        layout.addWidget(self.button_delay_stage)
        layout.addWidget(self.button_frog)

        self.setLayout(layout)

        # match system:
        #     case "Windows":
        #         self.button_spectrometer.setEnabled(True)
        #         self.button_pulse_measure.setEnabled(True)
        #         self.button_delay_stage.setEnabled(True)
        #         self.button_frog.setEnabled(True)
        #     case "Linux":
        #         self.button_spectrometer.setEnabled(False)
        #         self.button_pulse_measure.setEnabled(False)
        #         self.button_delay_stage.setEnabled(False)
        #         self.button_frog.setEnabled(False)
        #     case "Darwin":
                
        #         self.button_spectrometer.setEnabled(True)
        #         self.button_pulse_measure.setEnabled(True)
        #         self.button_delay_stage.setEnabled(False)
        #         self.button_frog.setEnabled(False)

        self.button_spectrometer.setEnabled(True)
        self.button_pulse_measure.setEnabled(True)
        self.button_delay_stage.setEnabled(True)
        self.button_frog.setEnabled(True)        

        self.show()

    def on_spectrometer_clicked(self):
        if self.spectrometer_window is None:
            self.spectrometer_window = ui.ui_Spectrometer()
        self.spectrometer_window.show()

    def on_pulse_measure_clicked(self):
        if self.pulse_measure_window is None:
            self.pulse_measure_window = ui.ui_PulseMeasure()
        self.pulse_measure_window.show()

    def on_delay_stage_clicked(self):
        if self.delay_stage_window is None:
            self.delay_stage_window = ui.ui_MotionStage()
        self.delay_stage_window.show()

    def on_FROG_clicked(self):
        if self.frog_window is None:
            self.frog_window = ui.ui_FROG()
        self.frog_window.show()

    def __del__(self):
        pass