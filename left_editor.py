from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import data
from data import Package
import editor
import os

# Left half of editor GUI
class LeftLayout(QVBoxLayout):
    def __init__(self, package : Package):
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
        self.data_table = DataTable(self.package)
        self.setWidget(self.data_table)

# Table widget for variable names, types, and values
class DataTable(QTableWidget):
    def __init__(self, package):
        super().__init__()

        self.package = package

        self.selected_row = -1

        #Makes vertical headers invisible, sets size policy, and initializes columns and 1 row
        self.verticalHeader().setVisible(False)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setColumnCount(3)
        self.setRowCount(0)

        self.cellClicked.connect(self.cell_clicked)
        self.cellDoubleClicked.connect(self.cell_double_clicked)

        # Sets up headers for columns
        h_name, h_type, h_val = QTableWidgetItem("Name"), QTableWidgetItem("Type"), QTableWidgetItem("Value")
        self.setHorizontalHeaderItem(0,h_name)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setHorizontalHeaderItem(1,h_type)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.setHorizontalHeaderItem(2,h_val)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        # Populates data_table with values from Package
        if len(self.package.data.keys()) == 0:
            self.add_row()
        else:
            for key in self.package.data:
                i = self.add_row()
                val = self.package.data[key]
                typeof = type(val).__name__
                self.cellWidget(i,1).set_type_from_string(typeof)
                self.item(i,0).setText(key)
                if typeof != "list":
                    self.item(i,2).setText(str(val))
                else:
                    widget = DataTableListWidget(key,val)
                    widget.window.w_list.itemChanged.connect(self.itemChanged.emit)
                    self.setItem(i,2,widget)
                    self.item(i,2).setText("...")
                
    # Converts data to a dictionary
    def to_dict(self):
        for i in range(self.rowCount()):
            key = self.item(i,0).text()
            if key == "":
                key = "value_" + str(i+1)
                self.item(i,0).setText(key)
        d = {}
        for i in range(self.rowCount()):
            key = self.item(i,0).text()
            data_type = self.cellWidget(i,1).get_type()
            if data_type != list:
                val = self.item(i,2).text()
                if val == "":
                    new_val = str(data_type.__call__())
                else:
                    new_val = data.parse_data_type(data_type, val)
                self.item(i,2).setText(str(new_val))
            else:
                if type(self.item(i,2)) != DataTableListWidget:
                    self.setItem(i,2, DataTableListWidget(key,[]))
                new_val = self.item(i,2).window.to_list()
                self.item(i,2).setText("...")
            
            d[key] = new_val
            
            
        return d
    
    # Selects the cell clicked by user
    def cell_clicked(self, row, _):
        self.selected_row = row
    
    def cell_double_clicked(self, row, col):
        self.selected_row = row
        if col == 2:
            if self.cellWidget(row,1).currentIndex() == 4:
                self.item(row,2).window.show()

    # Adds row of data
    def add_row(self):
        self.blockSignals(True)
        i = self.rowCount()
        self.insertRow(i)
        self.setCellWidget(i, 1, TypeBox(self,i))
        self.setItem(i,0, QTableWidgetItem())
        self.blockSignals(False)
        self.setItem(i,2, QTableWidgetItem())
        return i

    # Removes row by index selected
    def delete_row(self):
        if self.selected_row > -1:
            count = self.rowCount()
            self.setRowCount(count-1)
            self.itemChanged.emit(self.item(self.selected_row,0))
            self.removeRow(self.selected_row)
        self.selected_row -= 1

class ListEditor(QWidget):
    def __init__(self, name, list):
        super().__init__()
        self.name = name
        self.list = list

        self.setWindowTitle(name + " (List)")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.selected_item = -1

        self.setFont(editor.FONT)

        # List of loaded images
        self.w_list = QTableWidget()

        self.w_list.verticalHeader().setVisible(True)
        self.w_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.w_list.setColumnCount(2)
        self.w_list.setRowCount(0)

        self.w_list.cellDoubleClicked.connect(self.cell_double_clicked)
        self.w_list.cellClicked.connect(self.cell_clicked)

        h_type, h_val = QTableWidgetItem("Type"), QTableWidgetItem("Value")
        self.w_list.setHorizontalHeaderItem(0,h_type)
        self.w_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.w_list.setHorizontalHeaderItem(1,h_val)
        self.w_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)

        for val in list:
            i = self.add_row()
            typeof = type(val).__name__
            self.w_list.cellWidget(i,0).set_type_from_string(typeof)
            if typeof != "list":
                self.w_list.item(i,1).setText(str(val))
            else:
                widget = DataTableListWidget(str(i),val)
                widget.window.w_list.itemChanged.connect(self.w_list.itemChanged.emit)
                self.w_list.setItem(i,1,widget)
                self.w_list.item(i,1).setText("...")

        layout = QVBoxLayout()
        layout.addWidget(self.w_list)

        button_container = QHBoxLayout()
        add = QPushButton("Add")
        add.clicked.connect(self.add_row)
        add.setToolTip("Adds new list item")
        delete = QPushButton("Delete")
        delete.clicked.connect(self.delete_row)
        delete.setToolTip("Deletes selected list item")

        button_container.addWidget(add)
        button_container.addWidget(delete)
        r_spacer = QSpacerItem(60, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # add spacer to move buttons to left side
        button_container.addItem(r_spacer)
        layout.addLayout(button_container)
        self.setLayout(layout)

    def to_list(self):
        res = []
        for i in range(self.w_list.rowCount()):
            data_type = self.w_list.cellWidget(i,0).get_type()
            if data_type != list:
                val = self.w_list.item(i,1).text()
                if val == "":
                    new_val = str(data_type.__call__())
                else:
                    new_val = data.parse_data_type(data_type, val)
                self.w_list.item(i,1).setText(str(new_val))
            else:
                if type(self.w_list.item(i,1)) != DataTableListWidget:
                    self.w_list.setItem(i,1, DataTableListWidget(str(i),[]))
                new_val = self.w_list.item(i,1).window.to_list()
                self.w_list.item(i,1).setText("...")
            res.append(new_val)
        return res
    
    def cell_clicked(self, row, _):
        self.selected_row = row
    
    def cell_double_clicked(self, row, col):
        self.selected_row = row
        if col == 1:
            if self.w_list.cellWidget(row,0).currentIndex() == 4:
                self.w_list.item(row,1).window.show()

    def add_row(self):
        self.w_list.blockSignals(True)
        i = self.w_list.rowCount()
        self.w_list.insertRow(i)
        self.w_list.setCellWidget(i, 0, TypeBox(self.w_list,i, 0))
        self.w_list.setItem(i,1, QTableWidgetItem())
        self.w_list.blockSignals(False)
        return i
    
    def delete_row(self):
        if self.selected_row > -1:
            count = self.w_list.rowCount()
            self.w_list.setRowCount(count-1)
            self.w_list.itemChanged.emit(self.item(self.selected_row,0))
            self.w_list.removeRow(self.selected_row)
        self.selected_row -= 1

        # Subwindow container for lists in data table
class DataTableListWidget(QTableWidgetItem):
    def __init__(self, name, list):
        super().__init__()
        self.window = ListEditor(name, list)
        self.window.setStyleSheet(editor.STYLE)
        self.window.setFont(editor.FONT)

# Dropdown for Type field of data_table  
class TypeBox(QComboBox):
    def __init__(self, table : DataTable, row : int, is_table : bool = True):
        super().__init__()
        self.is_table = is_table
        self.list = ("Int", "Float", "String", "Bool", "List")
        self.addItems(self.list)
        self.table : DataTable = table
        self.row = row
        self.currentIndexChanged.connect(self.type_change)

    # When the box is changed, edit the value
    def type_change(self, val):
        t = self.get_type()
        item = self.table.item(self.row, 1+int(self.is_table))
        if t != list:
            val = data.parse_data_type(t, item.text())
            item.setText(str(val))
        else:
            if self.is_table:
                name = self.table.item(self.row, 0).text()
            else:
                name = str(self.row)
            self.table.setItem(self.row, 1+int(self.is_table),DataTableListWidget(name,[]))
        

    # Converts integer to typename
    def get_type(self):
        v = self.currentIndex()
        if v == 1:
            return float
        elif v == 2:
            return str
        elif v == 3:
            return bool
        elif v == 4:
            return list
        else:
            return int
        
    def set_type_from_string(self, type_string):
        if type_string == "str":
            self.setCurrentIndex(2)
        self.setCurrentText(str.capitalize(type_string))

        