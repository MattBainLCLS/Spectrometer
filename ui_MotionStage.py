from PyQt6 import QtCore, QtWidgets, QtGui
import MotionStage
import ui_ConnectDelayStage
import time

class ui_MotionStage(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Delay Stage Interface")

        # Connect
        self.connect = QtWidgets.QPushButton()
        self.connect.setText("Connect")

        layout_connect = QtWidgets.QHBoxLayout()
        #layout_connect.addWidget(serial_label)
        #layout_connect.addWidget(self.serial)
        layout_connect.addWidget(self.connect)

        #   Connect slots
        self.connect.clicked.connect(self.on_clicked_connect)
        #self.serial.returnPressed.connect(self.on_clicked_connect)

        # Jog Buttons
        #   Jog backward
        self.button_jog_backward = QtWidgets.QPushButton()
        self.button_jog_backward.setText("<")
        #   Jog forward
        self.button_jog_forward = QtWidgets.QPushButton()
        self.button_jog_forward.setText(">")
        #   Button layout
        layout_jog_buttons = QtWidgets.QHBoxLayout()
        layout_jog_buttons.addWidget(self.button_jog_backward)
        layout_jog_buttons.addWidget(self.button_jog_forward)

        #   Jog Size (ps)
        jog_label = QtWidgets.QLabel("Jog Size: ")
        self.jog_size_edit = QtWidgets.QLineEdit()
        jog_size_validator = QtGui.QDoubleValidator()
        jog_size_validator.setBottom(0.0001)
        jog_size_validator.setDecimals(4) # Set 100 attosecond maximum precision
        self.jog_size_edit.setValidator(jog_size_validator)
        self.jog_size_edit.setText("0.010")
        jog_label_unit = QtWidgets.QLabel(" ps")
        layout_jog_size = QtWidgets.QHBoxLayout()
        layout_jog_size.addWidget(jog_label)
        layout_jog_size.addWidget(self.jog_size_edit)
        layout_jog_size.addWidget(jog_label_unit)

        layout_jog = QtWidgets.QVBoxLayout()
        layout_jog.addLayout(layout_jog_size)
        layout_jog.addLayout(layout_jog_buttons)

        #   Connect Jog Slots
        self.button_jog_backward.clicked.connect(self.jog_backward)
        self.button_jog_forward.clicked.connect(self.jog_forward)


        # Go To
        #   Home button

        self.button_home = QtWidgets.QPushButton()
        self.button_home.setText("Home")

        #   Reverse
        self.label_reverse = QtWidgets.QLabel()
        self.label_reverse.setText("Reverse?")
        self.checkbox_reverse = QtWidgets.QCheckBox()
        self.checkbox_reverse.setCheckable(True)

        #   Go To
        goto_label = QtWidgets.QLabel("Go To: ")
        self.goto_edit = QtWidgets.QLineEdit()
        goto_edit_validator = QtGui.QDoubleValidator()
        goto_edit_validator.setDecimals(4)
        self.goto_edit.setValidator(goto_edit_validator)
        goto_label_unit = QtWidgets.QLabel(" ps")
        self.button_set_time_zero = QtWidgets.QPushButton()
        self.button_set_time_zero.setText("Set t0")
        layout_goto = QtWidgets.QHBoxLayout()
        layout_goto.addWidget(goto_label)
        layout_goto.addWidget(self.goto_edit)
        layout_goto.addWidget(goto_label_unit)
        layout_goto.addWidget(self.button_home)
        layout_goto.addWidget(self.label_reverse)
        layout_goto.addWidget(self.checkbox_reverse)

        #   Connect Goto Slots
        self.goto_edit.editingFinished.connect(self.onChangedGoto)
        self.button_home.clicked.connect(self.onClickedHome)
        self.button_set_time_zero.clicked.connect(self.onClickedSetTimeZero)
        self.checkbox_reverse.stateChanged.connect(self.onCheckboxReverseStateChanged)

        # Readback
        readback_label = QtWidgets.QLabel("Current Position: ")
        self.readback_position = QtWidgets.QLabel("")
        readback_label_unit = QtWidgets.QLabel(" ps")
        limit_label = QtWidgets.QLabel("Limits")
        self.limit_lower = QtWidgets.QLabel()
        limit_label_separator = QtWidgets.QLabel(" - ")
        self.limit_upper = QtWidgets.QLabel()
        limit_label_unit = QtWidgets.QLabel(" ps")

        layout_readback = QtWidgets.QHBoxLayout()
        layout_readback.addWidget(readback_label)
        layout_readback.addWidget(self.readback_position)
        layout_readback.addWidget(readback_label_unit)

        layout_readback.addWidget(limit_label)
        layout_readback.addWidget(self.limit_lower)
        layout_readback.addWidget(limit_label_separator)
        layout_readback.addWidget(self.limit_upper)
        layout_readback.addWidget(limit_label_unit)

        
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
        self.time_zero_mm = 8
        self.c_mm_ps = 0.299792458
        self.checkbox_reverse.setChecked(False)

        # Default state

        self.connect.setStyleSheet("color: #4ECE44")
        self.button_home.setEnabled(False)
        
        self.goto_edit.setEnabled(False)
        self.jog_size_edit.setEnabled(False)
        self.button_jog_backward.setEnabled(False)
        self.button_jog_forward.setEnabled(False)

    def on_clicked_connect(self):
        
        if self.connect.text() == "Connect":
            self.window_connect_delay_stage = ui_ConnectDelayStage.ui_ConnectDelayStage()
            self.window_connect_delay_stage.device_found.connect(self.onDeviceSelected)
            self.window_connect_delay_stage.show()

        elif self.connect.text() == "Disconnect":
            try:
                self.delay_stage.close()
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
                self.button_jog_backward.setEnabled(False)
                self.button_jog_forward.setEnabled(False)

    def onDeviceSelected(self, device):
        try:
                self.delay_stage = MotionStage.MotionStage(device)
        except:
            print("connection Failed")
        else:
            print("Connected successfully!")
            self.connect.setText("Disconnect")
            self.connect.setStyleSheet("color: #B91B1B")
            self.button_home.setEnabled(True)
            self.goto_edit.setEnabled(True)
            self.jog_size_edit.setEnabled(True)
            self.button_jog_backward.setEnabled(True)
            self.button_jog_forward.setEnabled(True)
            self.updatePosition()
            self.updateLimits()

    def onClickedHome(self):
        self.button_home.setText("Homing...")
        print("Homing...")
        self.delay_stage.home()
        while self.delay_stage.isMotionDone():
            self.updatePosition()
            time.sleep(0.25)
        self.button_home.setText("Home")
        print("Homed")

    def onChangedGoto(self):

        pos_mm = self.mm_from_ps(self.goto_edit.text())
        self.delay_stage.goTo(pos_mm)
        i=0
        while not self.delay_stage.isMotionDone():
            time.sleep(0.25)
        self.updatePosition()

    def updatePosition(self):
        self.readback_position.setText("%.4f" % (self.ps_from_mm(self.delay_stage.currentPosition())))

    def onClickedSetTimeZero(self):
        self.time_zero_mm = self.delay_stage.currentPosition()
        self.updatePosition()
        self.updateLimits()

    def onCheckboxReverseStateChanged(self):
        self.updatePosition()
        self.updateLimits()

    def updateLimits(self):
        limits = self.delay_stage.getLimits()

        limits_time = tuple(map(self.ps_from_mm, limits))
        self.limit_lower.setText("%.4f" % min(limits_time))
        self.limit_upper.setText("%.4f" % max(limits_time))

    def jog_forward(self):
        current_time = self.ps_from_mm(self.delay_stage.currentPosition())
        new_position = self.mm_from_ps(current_time + float(self.jog_size_edit.text()))
        self.delay_stage.goTo(new_position)
        while not self.delay_stage.isMotionDone():
            time.sleep(0.25)
        self.updatePosition()

    def jog_backward(self):
        current_time = self.ps_from_mm(self.delay_stage.currentPosition())
        new_position = self.mm_from_ps(current_time - float(self.jog_size_edit.text()))
        self.delay_stage.goTo(new_position)
        while not self.delay_stage.isMotionDone():
            time.sleep(0.25)
        self.updatePosition()

    def mm_from_ps(self, time):
        return ((-1 if self.checkbox_reverse.isChecked() else 1) * float(time) * 0.5*self.c_mm_ps) + self.time_zero_mm

    def ps_from_mm(self, distance):
        return ((-1 if self.checkbox_reverse.isChecked() else 1) * (distance - self.time_zero_mm))/(0.5*self.c_mm_ps)

