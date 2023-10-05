from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import sys
from editor import *

if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    main = SDOPWindow()

    main.show()
    app.exec_()