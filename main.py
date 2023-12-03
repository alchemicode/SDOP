from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys
from editor import *
import data

if __name__ == "__main__":
   
    # Loads default images into memory
    with open("res/default.png", "rb") as f:
        i = f.read()
        data.DEFAULT_IMAGE = bytearray(i)
    with open("res/empty.png", "rb") as f:
        i = f.read()
        data.EMPTY_IMAGE = bytearray(i)
    with open("res/logo.png", "rb") as f:
        i = f.read()
        data.LOGO_IMAGE = bytearray(i)
    
    # Loads stylesheet
    with open("res/style.qss", "r") as f:
        style = f.read()


    # Initializes Qt
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Initializes & executes main window
    main = SDOPWindow(style)
    main.show()
    sys.exit(app.exec_())