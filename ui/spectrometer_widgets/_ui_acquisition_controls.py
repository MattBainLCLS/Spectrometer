from PyQt6 import QtWidgets, QtCore, QtGui

class AcquisitionControls(QtWidgets.QWidget):
        
    def __init__(self):
        super().__init__()

        acquisition_controls_layout = QtWidgets.QHBoxLayout()

        # Exposure
        exposure_layout = QtWidgets.QHBoxLayout()
        
        exposure_label = QtWidgets.QLabel()
        exposure_label.setText("Exposure: ")

        self.exposure_field = QtWidgets.QLineEdit("100")
        exposure_field_validator = QtGui.QDoubleValidator()
        exposure_field_validator.setDecimals(3)
        exposure_field_validator.setBottom(0.01)
        self.exposure_field.setValidator(exposure_field_validator)

        exposure_unit = QtWidgets.QLabel()
        exposure_unit.setText("ms")

        exposure_layout.addWidget(exposure_label)
        exposure_layout.addWidget(self.exposure_field)
        exposure_layout.addWidget(exposure_unit)

        # Averaging
        averaging_layout = QtWidgets.QHBoxLayout()

        averaging_label = QtWidgets.QLabel()
        averaging_label.setText("Average: ")

        self.averaging_field = QtWidgets.QLineEdit("1")
        averaging_field_validator = QtGui.QIntValidator()
        averaging_field_validator.setBottom(1)
        self.averaging_field.setValidator(averaging_field_validator)

        self.averaging_unit = QtWidgets.QLabel()
        self.averaging_unit.setText(" spectra ")

        averaging_layout.addWidget(averaging_label)
        averaging_layout.addWidget(self.averaging_field)
        averaging_layout.addWidget(self.averaging_unit)

        self.averaging_field.editingFinished.connect(self.update_averaging_unit)

        # Finalize

        acquisition_controls_layout.addLayout(exposure_layout)
        acquisition_controls_layout.addLayout(averaging_layout)
        self.setLayout(acquisition_controls_layout)

        

    @QtCore.pyqtSlot()
    def update_averaging_unit(self):
        if self.averaging_field.text() == 1:
            self.averaging_unit.setText(" spectrum")
        else:
            self.averaging_unit.setText(" spectra ")
