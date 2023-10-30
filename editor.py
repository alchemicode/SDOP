from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import data
from data import Package
import os


# Main Application container
class SDOPWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Silly Data Object Packager")
        self.setFixedWidth(1280)
        self.setFixedHeight(720)
        self.editor = Editor()
        bar = self.menuBar()
        file = bar.addMenu("File")

        # Toolbar Menu
        # New Package button
        new = QAction("New",self)
        new.setShortcut("Ctrl+N")
        new.setStatusTip("Creates a new package tab")
        new.triggered.connect(self.editor.new_tab)
        file.addAction(new)

        # Open Package button
        open = QAction("Open", self)
        open.setShortcut("Ctrl+O")
        open.setStatusTip("Opens a package tab")
        #open.triggered.connect(self.editor.open_tab)
        file.addAction(open)

        # Save Package button
        save = QAction("Save",self)
        save.setShortcut("Ctrl+S")
        save.setStatusTip("Saves the current package tab")
        save.triggered.connect(self.editor.save_tab)
        file.addAction(save)

        # To be implemented
        file.addAction("Save As")
        file.addAction("Quit")
        edit = bar.addMenu("Edit")
        edit.addAction("Copy")
        edit.addAction("Cut")
        edit.addAction("Paste")
        
        # Adds widget and status bar to bottom left
        self.setCentralWidget(self.editor)
        self.setStatusBar(QStatusBar(self))

#Editor Window
class Editor(QWidget):
    def __init__(self):
        super().__init__()
        # Sets up tabs
        self.tab_widget : QTabWidget = QTabWidget()
        self.tab_widget.tabCloseRequested.connect(self.tab_widget.removeTab)
        self.tab_widget.setTabsClosable(True)

        # Sample package for testing
        p1 = Package("Sley", "me when I slay", {"Pog" : 1, "Pog2" : 1.5, "Funny" : True, "Silly" : "ylliS", "Goofy" : [1,"heck",3.7]}, [("default", data.DEFAULT_IMAGE), ("lol", data.EXAMPLE_IMAGE)])
        self.add_tab(EditorTab(p1, True, self.tab_widget))


        self.tab_widget.resize(1100,650)
        layout = QHBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        # Sets up error message
        self.error = QMessageBox()
        self.error.setIcon(3)
        self.error.setText("Packaging Error\n\nPlease Enter a Package Name")
        self.error.setWindowTitle("Error")

    # Creates a new tab and new Package Object
    def new_tab(self):
        n = EditorTab(Package("","",{},[]), False, self.tab_widget)
        self.tab_widget.addTab(n, "New Package")
        self.tab_widget.setCurrentWidget(n)

    # Creates a tab based off a Package Object
    def add_tab(self, tab):
        if tab.package.filepath != "":
            self.tab_widget.addTab(tab, os.path.basename(tab.package.filepath))
        else:
            self.tab_widget.addTab(tab, "New Package")

    # Collects editor data and makes it into a Package object
    def save_tab(self):
        tab = self.tab_widget.currentWidget()
        if not tab.saved:
            if tab.package.name == "":
                self.error.show()
            else:
                if tab.package.filepath == "":
                    name, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Silly Data Object Package (*.sdop)")
                    with open(name, 'wb') as f:
                        f.write(tab.package.convert_data_to_bytes())
                        for i in tab.package.images:
                            f.write(i[1])
                        tab.package.filepath = name
                        self.tab_widget.setTabText(os.path.basename(name))
                        tab.saved = True
                else:
                    with open(tab.package.filepath, 'wb') as f:
                        f.write(tab.package.convert_data_to_bytes())
                        for i in tab.package.images:
                            f.write(i[1])
                        tab.saved = True

# Tab Widget
class EditorTab(QWidget):
    def __init__(self, package : Package, saved, tabWidget : QTabWidget):
        super().__init__()
        self.package : Package = package
        self.saved : bool = saved
        self.tabWidget = tabWidget
        # Left side holds Name, Description, Data table, New and Delete buttons
        self.left_side = LeftLayout(package, self)
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.left_side)
        
        # Add spacer between the two layouts to make nicer :)
        c_spacer = QSpacerItem(50, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.layout.addItem(c_spacer)

        # Right side holds image + placeholder, blank scrolldown menu, new and delete buttons
        self.right_side = RightLayout(package)
        self.layout.addLayout(self.right_side)
        self.setLayout(self.layout)

        # Sets up save asterisk signals (* at the beginning of tab names)
        self.left_side.name_line.textChanged.connect(self.file_changed)
        self.left_side.desc_box.textChanged.connect(self.file_changed)
        self.left_side.data_box.data_table.itemChanged.connect(self.file_changed)
        self.right_side.image_list.itemChanged.connect(self.file_changed)
    
    # Checks if the UI boxes match with the Package object data
    def check_for_changes(self):
        return self.left_side.name_line.text() != self.package.name \
            or self.left_side.desc_box.toPlainText() != self.package.desc \
            or self.left_side.data_box.data_table.to_dict() != self.package.data \
            or self.right_side.to_list() != self.package.images

    # Changed tab name and sets tab.saved depending on check_for_changes
    def file_changed(self):
        if self.check_for_changes():
            i = self.tabWidget.indexOf(self)
            if self.package.filepath != "":
                self.tabWidget.setTabText(i, "*" + os.path.basename(self.package.filepath))
            else:
                self.tabWidget.setTabText(i, "*New Package")
            self.saved = False
        else:
            if self.package.filepath != "":
                self.tabWidget.setTabText(i, os.path.basename(self.package.filepath))
                self.saved = True
    def package_data(self):
        self.package.name = self.left_side.name_line.text()
        self.package.desc = self.left_side.desc_box.toPlainText()
        self.package.data = self.left_side.data_box.data_table.to_dict()
        self.package.images = self.right_side.to_list()
                
# Left half of editor GUI
class LeftLayout(QVBoxLayout):
    def __init__(self, package : Package, tab : EditorTab):
        super().__init__()
        self.package = package

        # Add name label and single line text box
        name_label : QLabel = QLabel("Name")
        self.addWidget(name_label)
        self.name_line = QLineEdit()
        self.name_line.setPlaceholderText("Enter Name")
        if package.name != "":
            self.name_line.setText(package.name)
        self.addWidget(self.name_line)

        # Add description label and multiline text box
        desc_label = QLabel("Description")
        self.addWidget(desc_label)
        self.desc_box = QTextEdit()
        self.desc_box.setPlaceholderText("Type here")
        if package.desc != "":
            self.desc_box.setText(package.desc)
        self.desc_box.setMaximumHeight(100)
        self.addWidget(self.desc_box)

        # Add data label and scrollable table
        data_label = QLabel("Data")
        self.addWidget(data_label)

        # Adds box for data table
        self.data_box = DataBox(package)
        self.addWidget(self.data_box)

        # Create HBox for buttons
        left_button_container = QHBoxLayout()
        left_new = QPushButton("New")
        left_new.setToolTip("Creates a new data row")
        left_new.clicked.connect(self.data_box.data_table.add_row)

        left_delete = QPushButton("Delete")
        left_delete.setToolTip("Deletes selected data row")
        left_delete.clicked.connect(self.data_box.data_table.delete_row)
        left_button_container.addWidget(left_new)
        left_button_container.addWidget(left_delete)
        # Adds space between buttons
        l_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # add spacer to move buttons to left side

        left_button_container.addItem(l_spacer)
        self.addLayout(left_button_container)

# Container for data table for sizing reasons
class DataBox(QScrollArea):
    def __init__(self, package : Package):
        super().__init__()
        self.package = package
        # Set size and scroll policy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        #Fixes the internal table size problem
        self.setWidgetResizable(True)          

        #Creates and adds table
        self.data_table = DataTable(self.package.data)
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

        # Sets up headers for columns
        h_name, h_type, h_val = QTableWidgetItem("Name"), QTableWidgetItem("Type"), QTableWidgetItem("Value")
        h_name.setBackground(QColor(128, 128, 128))
        h_type.setBackground(QColor(128, 128, 128))
        h_val.setBackground(QColor(128, 128, 128))
        self.setHorizontalHeaderItem(0,h_name)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setHorizontalHeaderItem(1,h_type)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.setHorizontalHeaderItem(2,h_val)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        # Populates data_table with values from Package
        if len(pdata.keys()) == 0:
            self.add_row()
        else:
            for key in pdata:
                i = self.add_row()
                val = pdata[key]
                self.item(i,0).setText(key)
                self.item(i,2).setText(str(val))
                self.cellWidget(i,1).set_type_from_string(type(val).__name__)

    # Converts data to a dictionary
    def to_dict(self):
        d = {}
        for i in range(self.rowCount()):
            key = self.item(i,0).text()
            data_type = self.cellWidget(i,1).get_type()
            val = self.item(i,2).text()
            d[key] = data_type.__call__(val)
        return d
    
    # Selects the cell clicked by user
    def cell_clicked(self, row, _):
        self.selectedRow = row

    # Adds row of data
    def add_row(self):
        i = self.rowCount()
        self.insertRow(i)
        self.setItem(i,0, QTableWidgetItem())
        self.setItem(i,2, QTableWidgetItem())
        self.setCellWidget(i, 1, TypeBox())
        return i

    # Removes row by index selected
    def delete_row(self):
        if self.selectedRow > -1:
            self.removeRow(self.selectedRow)
        self.selectedRow = -1

# Dropdown for Type field of data_table        
class TypeBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.list = ("Int", "Float", "String", "Bool", "List")
        self.addItems(self.list)

    # Converts integer to typename
    def get_type(self):
        if self.currentIndex() == 0:
            return int
        elif self.currentIndex() == 1:
            return float
        elif self.currentIndex() == 2:
            return str
        elif self.currentIndex() == 3:
            return bool
        elif self.currentIndex() == 4:
            return list
        else:
            return int
        
    def set_type_from_string(self, type_string):
        if type_string == "str":
            self.setCurrentIndex(2)
        self.setCurrentText(str.capitalize(type_string))

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
        self.pixmap.loadFromData(self.image_list.item(index).image[1])
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



