from PyQt5 import QtWidgets
import sys
from huya.spiders.ui_middleware import LiveSpiderWindow

app = QtWidgets.QApplication(sys.argv)
home = LiveSpiderWindow()
print("ui_main")
home.show()
sys.exit(app.exec_())
