
#import ui_MotionStage
#import ui_Spectrometer
import ui_StartWindow
from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication([])

#window = ui_MotionStage.ui_MotionStage()
#window = ui_Spectrometer.ui_Spectrometer()
window = ui_StartWindow.ui_StartWindow()

window.show()

app.exec()