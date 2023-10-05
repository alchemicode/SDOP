from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import sys

app = QApplication(sys.argv)
app.setStyle("Fusion")
window = QWidget()

# Define main outer container within window
container = QHBoxLayout()
window.setWindowTitle("Silly Data Object Packager")
window.setFixedWidth(640)
window.setFixedHeight(750)
window.setLayout(container)

# Left side holds Name, Description, Data table, New and Delete buttons
left_side = QVBoxLayout()
container.addLayout(left_side)

# Add spacer between the two layouts to make nicer :)
c_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
container.addItem(c_spacer)

# Right side holds image + placeholder, blank scrolldown menu, new and delete buttons
right_side = QVBoxLayout()
container.addLayout(right_side)

# 
# START LEFT SIDE
#
# Add name label and single line text box
name_label = QLabel("Name")
left_side.addWidget(name_label)
name_line = QLineEdit()
name_line.setPlaceholderText("Enter Name")
left_side.addWidget(name_line)

# Add description label and multiline text box
desc_label = QLabel("Description")
left_side.addWidget(desc_label)
desc_box = QTextEdit()
desc_box.setPlaceholderText("Type here")
left_side.addWidget(desc_box)

# Add data label and scrollable table
data_label = QLabel("Data")
left_side.addWidget(data_label)

# Create a scroll area
data_scroll_area = QScrollArea()
data_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set size policy
left_side.addWidget(data_scroll_area)

data_table = QTableWidget()
data_scroll_area.setWidget(data_table)

data_table.verticalHeader().setVisible(False)
data_table.horizontalHeader().setVisible(False)

data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

data_table.setColumnCount(2)
data_table.setRowCount(20)

headers = ["Name", "Value"]

# Create a custom header widget with grey background
for i in range(len(headers)):
    custom_header_item = QTableWidgetItem(headers[i])
    custom_header_item.setBackground(QColor(192, 192, 192))  # Grey background color
    data_table.setItem(0, i, custom_header_item)  # Set items in the top row

data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

# Create HBox for buttons
left_button_container = QHBoxLayout()
left_new = QPushButton("New")
left_delete = QPushButton("Delete")
left_button_container.addWidget(left_new)
left_button_container.addWidget(left_delete)
l_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
# add spacer to move buttons to left side
left_button_container.addItem(l_spacer)
left_side.addLayout(left_button_container)

#
# START RIGHT SIDE
#
image_label = QLabel("Image")
right_side.addWidget(image_label)
default_image = QPixmap("default.png")
image_display = QLabel()
image_display.setPixmap(default_image.scaledToWidth(256))
image_display.resize(256,256)
right_side.addWidget(image_display)

# Add text box under image with scroll bar
image_text_display = QTextEdit()
image_text_display.setPlainText("Image info lessgooooooooooooooooooooooooooooo\n" * 1000)
image_text_display.setVerticalScrollBarPolicy(2)
right_side.addWidget(image_text_display)

# Create HBox for buttons
right_button_container = QHBoxLayout()
right_new = QPushButton("New")
right_delete = QPushButton("Delete")
right_button_container.addWidget(right_new)
right_button_container.addWidget(right_delete)
r_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
# add spacer to move buttons to left side
right_button_container.addItem(r_spacer)
right_side.addLayout(right_button_container)


window.show()
app.exec_()