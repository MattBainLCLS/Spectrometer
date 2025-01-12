from PyQt6 import QtWidgets

class SpectrometerButtons(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.grabButton = QtWidgets.QPushButton("Grab", self)
        #self.grabButton.clicked.connect(self.on_clicked_grab)

        # closeButton.clicked.connect(self.close_window)

        self.pauseButton = QtWidgets.QPushButton("Resume", self)
        self.pauseButton.setCheckable(True)
        # self.pauseButton.clicked.connect(self.interruptFunc)

        self.saveButton = QtWidgets.QPushButton("Save", self)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.grabButton)
        button_layout.addWidget(self.pauseButton)
        button_layout.addWidget(self.saveButton)

        self.setLayout(button_layout)

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.grabButton.setEnabled(enabled)
        self.pauseButton.setEnabled(enabled)
        self.saveButton.setEnabled(enabled)