
import ui_MotionStage
from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication([])

window = ui_MotionStage.ui_MotionStage()

window.show()

app.exec()