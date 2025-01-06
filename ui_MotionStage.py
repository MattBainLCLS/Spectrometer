from PyQt6 import QtCore, QtWidgets, QtGui

class ui_MotionStage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QMini Spectrometer Interface")

        # Serial number entry
        serial_label = QtWidgets.QLabel()
        serial_label.setText("Serial Number: ")
        self.serial = QtWidgets.QLineEdit()
        serialHBox = QtWidgets.QHBoxLayout()

        serialHBox.addWidget(serial_label)
        serialHBox.addWidget(self.serial)

        # Home button

        self.button_home = QtWidgets.QPushButton()
        self.button_home.setText("Home")

        # Jog Buttons
        #   Jog backward
        self.button_jog_back = QtWidgets.QPushButton()
        self.button_jog_back.setText("<")
        #   Jog forward
        self.button_jog_forward = QtWidgets.QPushButton()
        self.button_jog_forward.setText(">")
        #   Button layout
        layout_jog_buttons = QtWidgets.QHBoxLayout()
        layout_jog_buttons.addWidget(self.button_jog_back)
        layout_jog_buttons.addWidget(self.button_jog_forward)

        #   Jog Size (fs)
        jog_label = QtWidgets.QLabel("Jog Size: ")
        self.jog_size_edit = QtWidgets.QLineEdit()
        jog_size_validator = QtGui.QDoubleValidator()
        jog_size_validator.setBottom(0.001)
        jog_size_validator.setDecimals(3) # Set 1 attosecond maximum precision
        self.jog_size_edit.setValidator(jog_size_validator)
        self.jog_size_edit.setText("10")
        jog_label_unit = QtWidgets.QLabel(" fs")
        layout_jog_size = QtWidgets.QHBoxLayout()
        layout_jog_size.addWidget(jog_label)
        layout_jog_size.addWidget(self.jog_size_edit)
        layout_jog_size.addWidget(jog_label_unit)

        layout_jog = QtWidgets.QVBoxLayout()
        layout_jog.addLayout(layout_jog_size)
        layout_jog.addLayout(layout_jog_buttons)


        


        layout_delay = QtWidgets.QVBoxLayout()
        layout_delay.addLayout(serialHBox)
        layout_delay.addLayout(layout_jog)

        widget = QtWidgets.QWidget()
        self.setLayout(layout_delay)