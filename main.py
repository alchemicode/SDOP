from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
label1 = QLabel("HALP")
label1.setFont(QFont("Arial", 24))

layout.addWidget(label1)
window.setWindowTitle("Prefabify")
window.setFixedWidth(600)
window.setFixedHeight(600)
window.setLayout(layout)
window.show()
app.exec_()