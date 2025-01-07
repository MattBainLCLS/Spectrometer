import ui_StartWindow
from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication([])

window = ui_StartWindow.ui_StartWindow()

window.show()

app.exec()