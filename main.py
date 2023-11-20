from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import sys
from editor import *
import data

if __name__ == "__main__":

    # Initializes Qt
    app = QApplication(sys.argv)
    app.setStyle("Breeze")
   
    # Loads default images into memory
    with open("default.png", "rb") as f:
        i = f.read()
        data.DEFAULT_IMAGE = bytearray(i)
    with open("lol.png", "rb") as f:
        i = f.read()
        data.EXAMPLE_IMAGE = bytearray(i)
    with open("logo.png", "rb") as f:
        i = f.read()
        data.LOGO_IMAGE = bytearray(i)

    # Initializes & executes main window
    main = SDOPWindow()
    main.show()
    sys.exit(app.exec_())