from PyQt6 import QtCore, QtWidgets, QtGui
import hardware.motion

import platform

system = platform.system()

class ui_ConnectDelayStage(QtWidgets.QWidget):

    # Signals
    device_found = QtCore.pyqtSignal(hardware.FoundDevice)
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Find Motion Stage")

        self.found_device_list = list()

        if platform.system() == "Windows":
            self.found_device_list += hardware.motion.ThorlabsMotionStage.find_devices()

        self.found_device_list += hardware.motion.Dummy.find_devices()

        # Space for more "find devices" functions for other manufacturers

        self.device_list_widget = QtWidgets.QListWidget()

        for device in self.found_device_list:
            device_cell = QtWidgets.QListWidgetItem(device.manufacturer + " - " + str(device.model) + " - " + device.serial)
            self.device_list_widget.addItem(device_cell)

        connect_button = QtWidgets.QPushButton()
        connect_button.setText("Connect")
        connect_button.clicked.connect(self.onClickedConnect)


        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.device_list_widget)
        layout.addWidget(connect_button)

        self.setLayout(layout)

    def onClickedConnect(self):
        self.device_found.emit(self.found_device_list[self.device_list_widget.currentRow()])
        self.close()