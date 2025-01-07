import MotionStage
import ui_ConnectDelayStage

from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication([])

window = ui_ConnectDelayStage.ui_ConnectDelayStage()

window.show()

app.exec()
#found_device_list = list()
#print(type(MotionStage.get_device_list(found_device_list)))

