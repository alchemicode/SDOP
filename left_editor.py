from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import data
from data import Package
import os

# Left half of editor GUI
class LeftLayout(QVBoxLayout):
    def __init__(self, package : Package, tab):
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
        l_spacer = QSpacerItem(60, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

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

# Table widget for variable names, types, and values
class DataTable(QTableWidget):
    def __init__(self, pdata):
        super().__init__()

        self.selected_row = -1

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
                self.item(i,2).setText(str(val))
                self.cellWidget(i,1).set_type_from_string(type(val).__name__)
                self.item(i,0).setText(key)
                
    # Converts data to a dictionary
    def to_dict(self):
        for i in range(self.rowCount()):
            key = self.item(i,0).text()
            if key == "":
                old = self.selected_row
                self.selected_row = i
                self.delete_row()
                self.selected_row = old
        d = {}
        for i in range(self.rowCount()):
            key = self.item(i,0).text()
            data_type = self.cellWidget(i,1).get_type()
            val = self.item(i,2).text()
            if val == "":
                self.item(i,2).setText(str(data_type.__call__()))
            d[key] = data.parse_data_type(data_type, val)
        return d
    
    # Selects the cell clicked by user
    def cell_clicked(self, row, _):
        self.selected_row = row

    # Adds row of data
    def add_row(self):
        self.blockSignals(True)
        i = self.rowCount()
        self.insertRow(i)
        self.setCellWidget(i, 1, TypeBox(self,i))
        self.setItem(i,0, QTableWidgetItem())
        self.setItem(i,2, QTableWidgetItem())
        self.blockSignals(False)
        return i

    # Removes row by index selected
    def delete_row(self):
        if self.selected_row > -1:
            count = self.rowCount()
            self.setRowCount(count-1)
            self.itemChanged.emit(self.item(self.selected_row,0))
            self.removeRow(self.selected_row)
        self.selected_row = -1

# Dropdown for Type field of data_table        
class TypeBox(QComboBox):
    def __init__(self, table : DataTable, row : int):
        super().__init__()
        self.list = ("Int", "Float", "String", "Bool", "List")
        self.addItems(self.list)
        self.table : DataTable = table
        self.row = row
        self.currentIndexChanged.connect(self.type_change)

    # When the box is changed, edit the value
    def type_change(self):
        t = self.get_type()
        item = self.table.item(self.row, 2)
        val = data.parse_data_type(t, item.text())
        item.setText(str(val))

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