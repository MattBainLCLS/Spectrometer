from PyQt6 import QtCore, QtWidgets, QtGui
import MotionStage

class ui_MotionStage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QMini Spectrometer Interface")

        # Connect
        serial_label = QtWidgets.QLabel()
        serial_label.setText("Serial Number: ")
        self.serial = QtWidgets.QLineEdit()
        self.connect = QtWidgets.QPushButton()
        self.connect.setText("Connect")

        layout_connect = QtWidgets.QHBoxLayout()
        layout_connect.addWidget(serial_label)
        layout_connect.addWidget(self.serial)
        layout_connect.addWidget(self.connect)

        #   Connect slots
        self.connect.clicked.connect(self.on_clicked_connect)

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


        # Go To
        #   Home button

        self.button_home = QtWidgets.QPushButton()
        self.button_home.setText("Home")
        #   Go To
        goto_label = QtWidgets.QLabel("Go To: ")
        self.goto_edit = QtWidgets.QLineEdit()
        goto_edit_validator = QtGui.QDoubleValidator()
        goto_edit_validator.setDecimals(3)
        self.goto_edit.setValidator(goto_edit_validator)
        goto_label_unit = QtWidgets.QLabel(" fs")
        layout_goto = QtWidgets.QHBoxLayout()
        layout_goto.addWidget(goto_label)
        layout_goto.addWidget(self.goto_edit)
        layout_goto.addWidget(goto_label_unit)
        layout_goto.addWidget(self.button_home)

        # Readback
        readback_label = QtWidgets.QLabel("Current Position: ")
        readback_position = QtWidgets.QLabel("")
        readback_label_unit = QtWidgets.QLabel(" fs")

        layout_readback = QtWidgets.QHBoxLayout()
        layout_readback.addWidget(readback_label)
        layout_readback.addWidget(readback_position)
        layout_readback.addWidget(readback_label_unit)

        # Build

        layout_delay = QtWidgets.QVBoxLayout()
        layout_delay.addLayout(layout_connect)
        layout_delay.addLayout(layout_goto)
        layout_delay.addLayout(layout_readback)
        layout_delay.addLayout(layout_jog)

        widget = QtWidgets.QWidget()
        self.setLayout(layout_delay)

        # Member Variables
        self.delay_stage = None

        # Default state

        self.connect.setStyleSheet("color: #4ECE44")
        self.button_home.setEnabled(False)
        
        self.goto_edit.setEnabled(False)
        self.jog_size_edit.setEnabled(False)
        self.button_jog_back.setEnabled(False)
        self.button_jog_forward.setEnabled(False)

    def on_clicked_connect(self):
        
        if self.connect.text() == "Connect":
            print(self.serial.text())
            try:
                self.delay_stage = MotionStage.KDC101(self.serial.text())
            except:
                print("connection Failed")
            else:
                print("Connected successfully!")
                self.connect.setText("Disconnect")
                self.connect.setStyleSheet("color: #B91B1B")
                self.button_home.setEnabled(True)
                self.goto_edit.setEnabled(True)
                self.jog_size_edit.setEnabled(True)
                self.button_jog_back.setEnabled(True)
                self.button_jog_forward.setEnabled(True)

        elif self.connect.text() == "Disconnect":
            try:
                self.delay_stage = None
            except:
                print("Disconnection Failed")
                exit()
            else:
                print("Disconnected successfully.")
                self.connect.setText("Connect")
                self.connect.setStyleSheet("color: #4ECE44")
                self.button_home.setEnabled(False)
                self.goto_edit.setEnabled(False)
                self.jog_size_edit.setEnabled(False)
                self.button_jog_back.setEnabled(False)
                self.button_jog_forward.setEnabled(False)