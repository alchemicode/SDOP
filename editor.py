from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
from data import *

class SDOPWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Silly Data Object Packager")
        self.setFixedWidth(760)
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
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        p1 = Package("Sley", "me when I slay", {"Pog" : 1, "Pog2" : 1.5, "Funny" : True, "Silly" : "ylliS", "Goofy" : [1,2,3]}, [])
        self.open_tabs = []
        self.add_tab(EditorTab(p1))
        self.tab_widget.resize(780,700)
        layout = QHBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    def add_tab(self, tab):
        self.open_tabs.append(tab)
        self.tab_widget.addTab(tab, tab.package.name)


class EditorTab(QWidget):
    def __init__(self, package):
        super().__init__()
        self.package = package
        # Left side holds Name, Description, Data table, New and Delete buttons
        left_side = LeftLayout(package)
        self.layout = QHBoxLayout()
        self.layout.addLayout(left_side)
        
        # Add spacer between the two layouts to make nicer :)
        c_spacer = QSpacerItem(50, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.layout.addItem(c_spacer)

        # Right side holds image + placeholder, blank scrolldown menu, new and delete buttons
        right_side = RightLayout(package.images)
        self.layout.addLayout(right_side)
        self.setLayout(self.layout)


class LeftLayout(QVBoxLayout):
    def __init__(self, package):
        super().__init__()
        # Add name label and single line text box
        name_label = QLabel("Name")
        self.addWidget(name_label)
        name_line = QLineEdit()
        name_line.setPlaceholderText("Enter Name")
        if package.name != "":
            name_line.setText(package.name)
        self.addWidget(name_line)

        # Add description label and multiline text box
        desc_label = QLabel("Description")
        self.addWidget(desc_label)
        desc_box = QTextEdit()
        desc_box.setPlaceholderText("Type here")
        if package.desc != "":
            desc_box.setText(package.desc)
        desc_box.setMaximumHeight(100)
        self.addWidget(desc_box)

        # Add data label and scrollable table
        data_label = QLabel("Data")
        self.addWidget(data_label)

        data_box = DataBox(package.data)
        self.addWidget(data_box)

        # Create HBox for buttons
        left_button_container = QHBoxLayout()
        left_new = QPushButton("New")
        left_new.setToolTip("Creates a new data row")
        left_new.clicked.connect(data_box.data_table.add_row)
        left_delete = QPushButton("Delete")
        left_delete.setToolTip("Deletes selected data row")
        left_delete.clicked.connect(data_box.data_table.delete_row)
        left_button_container.addWidget(left_new)
        left_button_container.addWidget(left_delete)
        l_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # add spacer to move buttons to left side
        left_button_container.addItem(l_spacer)
        self.addLayout(left_button_container)


class DataBox(QScrollArea):
    def __init__(self, pdata):
        super().__init__()
        # Set size and scroll policy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        #Fixes the internal table size problem
        self.setWidgetResizable(True)          

        #Creates and adds table
        self.data_table = DataTable(pdata)
        self.setWidget(self.data_table)


class DataTable(QTableWidget):
    def __init__(self, pdata):
        super().__init__()

        self.selectedRow = -1

        #Makes vertical headers invisible, sets size policy, and initializes columns and 1 row
        #self.verticalHeader().setVisible(False)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setColumnCount(3)
        self.setRowCount(0)

        self.cellClicked.connect(self.cell_clicked)

        h_name, h_type, h_val = QTableWidgetItem("Name"), QTableWidgetItem("Type"), QTableWidgetItem("Value")
        h_name.setBackground(QColor(128, 128, 128))
        h_type.setBackground(QColor(128, 128, 128))
        h_val.setBackground(QColor(128, 128, 128))
        self.setHorizontalHeaderItem(0,h_name)
        self.setHorizontalHeaderItem(1,h_type)
        self.setHorizontalHeaderItem(2,h_val)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        if len(pdata.keys()) == 0:
            self.add_row()
        else:
            for key in pdata:
                i = self.add_row()
                val = pdata[key]
                self.item(i,0).setText(key)
                self.item(i,2).setText(str(val))
                self.cellWidget(i,1).set_from_string(type(val).__name__)


    def cell_clicked(self, row, _):
        self.selectedRow = row

    def add_row(self):
        i = self.rowCount()
        self.insertRow(i)
        self.setItem(i,0, QTableWidgetItem())
        self.setItem(i,2, QTableWidgetItem())
        self.setCellWidget(i, 1, TypeBox())
        return i

    def delete_row(self):
        if self.selectedRow > -1:
            self.removeRow(self.selectedRow)
        self.selectedRow = -1

            
class TypeBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.list = ("Int", "Float", "String", "Bool", "List")
        self.addItems(self.list)
    def set_from_string(self, type_string):
        print(type_string)
        if type_string == "str":
            self.setCurrentIndex(2)
        self.setCurrentText(str.capitalize(type_string))

class RightLayout(QVBoxLayout):
    def __init__(self, images):
        super().__init__()
        self.image_label = QLabel("Image")
        self.addWidget(self.image_label)

        self.selected = 0

        self.images = images

        # Add text box under image with scroll bar
        image_list = QListWidget()
        for tuple in self.images:
            image_list.addItem(QListWidgetItem(tuple[0]))

        # attempting to load images as bytes
        self.pixmap = QPixmap()
        self.image_display = QLabel()
        self.image_display.resize(256,256)
        self.addWidget(self.image_display)
        self.render_image(0)
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

    def render_image(self, index):
        self.pixmap.loadFromData(self.images[index][1])
        self.image_display.setPixmap(self.pixmap.scaledToWidth(256))