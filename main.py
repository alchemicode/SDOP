from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = QWidget()
    container = QHBoxLayout()
    left_side = QVBoxLayout()
    container.addLayout(left_side)
    right_side = QVBoxLayout()
    container.addLayout(right_side)
    window.setWindowTitle("Silly Data Object Packager")
    window.setFixedWidth(1280)
    window.setFixedHeight(720)
    window.setLayout(container)

    name_label = QLabel("Name")
    left_side.addWidget(name_label)
    name_line = QLineEdit("Enter Name")
    left_side.addWidget(name_line)
    desc_label = QLabel("Description")
    left_side.addWidget(desc_label)
    desc_box = QTextEdit()
    left_side.addWidget(desc_box)
    data_label = QLabel("Data")
    left_side.addWidget(data_label)

    image_label = QLabel("Image")
    right_side.addWidget(image_label)
    default_image = QPixmap("default.png")
    image_display = QLabel()
    image_display.setPixmap(default_image.scaledToWidth(256))
    image_display.resize(256,256)
    right_side.addWidget(image_display)


    window.show()
    app.exec_()