from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt

class SDOPWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Silly Data Object Packager")
        self.setFixedWidth(800)
        self.setFixedHeight(720)

        bar = self.menuBar()
        file = bar.addMenu("File")

        new = QAction("New",self)
        new.setShortcut("Ctrl+N")
        file.addAction(new)

        file.addAction("Open")

        save = QAction("Save",self)
        save.setShortcut("Ctrl+S")
        file.addAction(save)

        file.addAction("Save As")
        file.addAction("Quit")

        edit = bar.addMenu("Edit")
        edit.addAction("Copy")
        edit.addAction("Cut")
        edit.addAction("Paste")

        editor = Editor()
        self.setCentralWidget(editor)


class Editor(QWidget):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.tabs.addTab(EditorTab("Yas"), "yas")
        self.tabs.resize(780,700)
        layout = QHBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)


class EditorTab(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        # Left side holds Name, Description, Data table, New and Delete buttons
        left_side = LeftLayout()
        self.layout = QHBoxLayout()
        self.layout.addLayout(left_side)
        
        # Add spacer between the two layouts to make nicer :)
        c_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(c_spacer)

        # Right side holds image + placeholder, blank scrolldown menu, new and delete buttons
        right_side = RightLayout()
        self.layout.addLayout(right_side)
        self.setLayout(self.layout)


class LeftLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        # Add name label and single line text box
        name_label = QLabel("Name")
        self.addWidget(name_label)
        name_line = QLineEdit()
        name_line.setPlaceholderText("Enter Name")
        self.addWidget(name_line)

        # Add description label and multiline text box
        desc_label = QLabel("Description")
        self.addWidget(desc_label)
        desc_box = QTextEdit()
        desc_box.setPlaceholderText("Type here")
        self.addWidget(desc_box)

        # Add data label and scrollable table
        data_label = QLabel("Data")
        self.addWidget(data_label)

        data_box = DataBox()
        self.addWidget(data_box)

        # Create HBox for buttons
        left_button_container = QHBoxLayout()
        left_new = QPushButton("New")
        left_delete = QPushButton("Delete")
        left_button_container.addWidget(left_new)
        left_button_container.addWidget(left_delete)
        l_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # add spacer to move buttons to left side
        left_button_container.addItem(l_spacer)
        self.addLayout(left_button_container)


class DataBox(QScrollArea):
    def __init__(self):
        super().__init__()
        # Set size and scroll policy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        #Fixes the internal table size problem
        self.setWidgetResizable(True)

        #Creates and adds table
        self.data_table = DataTable()
        self.setWidget(self.data_table)


class DataTable(QTableWidget):
    def __init__(self):
        super().__init__()
        #Makes vertical headers invisible, sets size policy, and initializes columns and 1 row
        self.verticalHeader().setVisible(False)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setColumnCount(3)
        self.setRowCount(1)
        
        h_name, h_type, h_val = QTableWidgetItem("Name"), QTableWidgetItem("Type"), QTableWidgetItem("Value")
        h_name.setBackground(QColor(128, 128, 128))
        h_type.setBackground(QColor(128, 128, 128))
        h_val.setBackground(QColor(128, 128, 128))
        self.setHorizontalHeaderItem(0,h_name)
        self.setHorizontalHeaderItem(1,h_type)
        self.setHorizontalHeaderItem(2,h_val)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def init_type_cells(self):
        r = self.rowCount()
        for i in range(r):
            self.setCellWidget(i,1,TypeBox())

            
class TypeBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.addItems(("Int", "Double", "String", "Boolean", "List"))

class RightLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.image_label = QLabel("Image")
        self.addWidget(self.image_label)
        default_image = QPixmap("default.png")
        image_display = QLabel()
        image_display.setPixmap(default_image.scaledToWidth(256))
        image_display.resize(256,256)
        self.addWidget(image_display)

        # Add text box under image with scroll bar
        image_list = QListWidget()
        image_list.addItem(QListWidgetItem("default"))
        image_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.addWidget(image_list)

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