from PyQt6 import QtCore, QtWidgets, QtGui

import platform

system = platform.system()

match system:
    case "Windows":
        import ui_Spectrometer
        import ui_MotionStage
    case "Darwin":
        import ui_Spectrometer

class ui_StartWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.spectrometer_window = None

        self.button_spectrometer = QtWidgets.QPushButton()
        self.button_spectrometer.setText("Spectrometer")
        self.button_spectrometer.setEnabled(False)
        self.button_spectrometer.clicked.connect(self.onSpectrometerClicked)
        
        self.button_delay_stage = QtWidgets.QPushButton()
        self.button_delay_stage.setText("Delay Stage")
        self.button_delay_stage.setEnabled(False)
        self.button_delay_stage.clicked.connect(self.onDelayStageClicked)

        self.button_frog = QtWidgets.QPushButton()
        self.button_frog.setText("FROG")
        self.button_frog.setEnabled(False)
        self.button_frog.clicked.connect(self.onFROGClicked)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.button_spectrometer)
        layout.addWidget(self.button_delay_stage)
        layout.addWidget(self.button_frog)

        self.setLayout(layout)

        match system:
            case "Windows":
                self.button_spectrometer.setEnabled(True)
                self.button_delay_stage.setEnabled(True)
                self.button_delay_stage.setEnabled(True)
            case "Linux":
                self.button_spectrometer.setEnabled(False)
                self.button_delay_stage.setEnabled(False)
                self.button_delay_stage.setEnabled(False)
            case "Darwin":
                
                self.button_spectrometer.setEnabled(True)
                self.button_delay_stage.setEnabled(False)
                self.button_delay_stage.setEnabled(False)

        self.show()

    def onSpectrometerClicked(self):
        if self.spectrometer_window is None:
            self.spectrometer_window = ui_Spectrometer.ui_Spectrometer()
            
        self.spectrometer_window.show()

    def onDelayStageClicked(self):
        delay_stage_window = ui_MotionStage.ui_MotionStage()

    def onFROGClicked(self):
        pass

    def __del__(self):
        pass