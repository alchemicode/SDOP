from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import data
from data import Package
import os

# List Widget for image_list
class ImageListItem(QListWidgetItem):
    def __init__(self, name, bytes):
        super().__init__()
        self.image_tuple = (name,bytes)
        self.setText(name)

# Right half of Editor GUI
class RightLayout(QVBoxLayout):
    def __init__(self, package : Package):
        super().__init__()
        self.image_label = QLabel("Image")
        self.addWidget(self.image_label)

        self.selected = -1

        # Add text box under image with scroll bar
        self.image_list = QListWidget()
        for tuple in package.images:
            self.image_list.addItem(ImageListItem(tuple[0], tuple[1]))

        # attempting to load images as bytes & sets up list widget
        self.pixmap = QPixmap()
        self.image_display = QLabel()
        self.image_display.resize(256,256)
        self.addWidget(self.image_display)
        self.render_image(0)
        self.image_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.image_list.itemDoubleClicked.connect(self.render_widget)
        self.addWidget(self.image_list)

        # Create HBox for buttons
        right_button_container = QHBoxLayout()
        right_new = QPushButton("New")
        right_delete = QPushButton("Delete")
        right_button_container.addWidget(right_new)
        right_button_container.addWidget(right_delete)
        r_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # add spacer to move buttons to left side
        right_button_container.addItem(r_spacer)
        self.addLayout(right_button_container)

    # Converts image list into list for comparison to Package
    def to_list(self):
        l = []
        for i in range(self.image_list.count()):
            item : ImageListItem = self.image_list.item(i)
            l.append(item.image_tuple)
        return l

    # Renders image by index in list
    def render_image(self, index):
        self.pixmap.loadFromData(self.image_list.item(index).image_tuple[1])
        self.image_display.setPixmap(self.pixmap.scaledToWidth(256))
    
    # Renders image contained in ImageListItem
    def render_widget(self, widget : ImageListItem):
        self.pixmap.loadFromData(widget.image_tuple[1])
        self.image_display.setPixmap(self.pixmap.scaledToWidth(256))
    
    # Deletes image by index
    def delete_image(self,index):
        # Probably gonna change this to be like in data_table, using selectedRow
        self.image_list.takeItem(index)
        self.images.remove(index)


