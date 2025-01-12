from PyQt6 import QtWidgets

class PlottingControls(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        plotting_controls_layout = QtWidgets.QGridLayout()

        yscale_layout = QtWidgets.QHBoxLayout()
        yscale_label = QtWidgets.QLabel()
        yscale_label.setText("Y Scale: ")
        self.combo_y_scale = QtWidgets.QComboBox(self)
        self.combo_y_scale.addItem('linear')
        self.combo_y_scale.addItem('symlog')
        self.combo_y_scale.setCurrentText('linear')
        yscale_layout.addWidget(yscale_label)
        yscale_layout.addWidget(self.combo_y_scale)

        self.button_reset_axes = QtWidgets.QPushButton()
        self.button_reset_axes.setText("Reset Axes")

        self.button_autoscale = QtWidgets.QPushButton()
        self.button_autoscale.setText("Autoscale")
        self.button_autoscale.setCheckable(True)

        self.button_normalize = QtWidgets.QPushButton()
        self.button_normalize.setText("Normalize")
        self.button_normalize.setCheckable(True)

        

        plotting_controls_layout.addLayout(yscale_layout, 1, 1)
        plotting_controls_layout.addWidget(self.button_reset_axes, 1, 2)
        plotting_controls_layout.addWidget(self.button_autoscale, 2, 1)
        plotting_controls_layout.addWidget(self.button_normalize, 2, 2)


        self.setLayout(plotting_controls_layout)

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.combo_y_scale.setEnabled(enabled)
        self.button_reset_axes.setEnabled(enabled)
        self.button_autoscale.setEnabled(enabled)
        self.button_normalize.setEnabled(enabled)