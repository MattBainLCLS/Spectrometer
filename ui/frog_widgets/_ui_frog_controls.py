from PyQt6 import QtWidgets, QtCore, QtGui


class FROGControls(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.start_button = QtWidgets.QPushButton()
        self.start_button.setText("Start")
        self.start_button.setStyleSheet("color: #4ECE44")

        frog_controls_layout = QtWidgets.QVBoxLayout()
        frog_controls_layout.addWidget(self.start_button)

        self.start_button.clicked.connect(self.toggle_start)

        self.setLayout(frog_controls_layout)

    def toggle_start(self):
        if self.start_button.text() == "Start":
            
            ## Code to start 
            self.start_button.setText("Stop")
            self.start_button.setStyleSheet("color: #B91B1B")
        else:
            self.start_button.setText("Start")
            self.start_button.setStyleSheet("color: #4ECE44")

    def __del__(self):
        pass