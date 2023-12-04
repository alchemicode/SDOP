from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import data
from data import Package
import os
from left_editor import *
from right_editor import *

FONT : QFont
STYLE : str

# Main Application container
class SDOPWindow(QMainWindow):
    def __init__(self, style):
        super().__init__()
        self.setWindowTitle("Silly Data Object Packager")
        self.setFixedWidth(1400)
        self.setFixedHeight(800)

        self.setStyleSheet(style)

        _id = QFontDatabase.addApplicationFont("res/FiraMono.ttf")
        font_families = QFontDatabase.applicationFontFamilies(_id)
        global FONT 
        FONT = QFont(font_families[0], 12)
        global STYLE
        STYLE = style
        
        self.editor = Editor()
        bar = self.menuBar()
        file = bar.addMenu("File")

        # Toolbar Menu
        # New Package button
        new = QAction("New",self)
        new.setShortcut("Ctrl+N")
        new.setStatusTip("Creates a new package tab")
        new.triggered.connect(self.editor.empty_tab)
        file.addAction(new)

        # Open Package button
        open = QAction("Open", self)
        open.setShortcut("Ctrl+O")
        open.setStatusTip("Opens a package tab")
        open.triggered.connect(self.editor.open_tab)
        file.addAction(open)

        # Save Package button
        save = QAction("Save",self)
        save.setShortcut("Ctrl+S")
        save.setStatusTip("Saves the current package tab")
        save.triggered.connect(self.editor.save_tab)
        file.addAction(save)

        # Save As Button
        save_as = QAction("Save As",self)
        save_as.setShortcut("Ctrl+Shift+S")
        save_as.setStatusTip("Saves the current package tab into a new file")
        save_as.triggered.connect(self.editor.save_tab_as)
        file.addAction(save_as)

        file.addAction("Quit")
        
        edit = bar.addMenu("Edit")
        # edit.addAction("Copy")
        # edit.addAction("Cut")
        # edit.addAction("Paste")

        layout = QVBoxLayout()

        # Adds logo and tab widget
        logo_pix = QPixmap()
        logo_display = QLabel()
        logo_display.setProperty("class", "image")
        logo_pix.loadFromData(data.LOGO_IMAGE)
        logo_display.resize(128,64)
        logo_display.setFixedHeight(64)
        logo_display.setPixmap(logo_pix.scaledToHeight(64))
        
        layout.addWidget(logo_display)

        central_widget = QWidget()
        
        layout.addWidget(self.editor)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        # Sets status bar in bottom left
        self.setStatusBar(QStatusBar(self))

    # Check for unsaved files before closing application
    def closeEvent(self, event):
        for i in range(self.editor.tab_widget.count()):
            w = self.editor.tab_widget.widget(i)
            if w.saved == False:
                box = QMessageBox
                ret = box.question(None, "", f"Save {w.package.name} before closing?", box.Yes | box.No | box.Cancel)
                if ret == box.No:
                    continue
                elif ret == box.Cancel:
                    event.ignore()
                    return
                else:
                    self.editor.tab_widget.setCurrentIndex(i)
                    self.editor.save_tab()
        event.accept()

# Editor Window
class Editor(QWidget):
    def __init__(self):
        super().__init__()
        # Sets up tabs
        self.tab_widget : QTabWidget = QTabWidget()
        self.tab_widget.tabCloseRequested.connect(self.tab_widget.removeTab)
        self.tab_widget.setTabsClosable(True)

        self.setFont(FONT)

        # Adds tab to layout
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
    def empty_tab(self):
        np = Package("","",{},[])
        np.add_default()
        n = EditorTab(np, False, self.tab_widget)
        self.tab_widget.addTab(n, "New Package")
        self.tab_widget.setCurrentWidget(n)

    # Creates a tab based off a Package Object
    def add_tab(self, tab):
        if tab.package.filepath != "":
            self.tab_widget.addTab(tab, ".../" + tab.package.get_filename())
        else:
            self.tab_widget.addTab(tab, "New Package")

    # Collects editor data and makes it into a Package object
    def save_tab(self):
        tab_i = self.tab_widget.currentIndex()
        tab = self.tab_widget.currentWidget()
        if not tab.saved:
            tab.set_package_data()
            if tab.package.name == "":
                self.error.show()
            else:
                if tab.package.filepath == "":
                    self.save_tab_as()
                else:
                    with open(tab.package.filepath, 'wb') as f:
                        f.write(tab.package.convert_data_to_bytes())
                        for i in tab.package.images:
                            f.write(i[1])
                        self.tab_widget.setTabText(tab_i, ".../" + tab.package.get_filename())
                        tab.saved = True

    # Opens save dialog and gets filepath to save file too
    def save_tab_as(self):
        name, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Silly Data Object Package (*.sdop)")
        tab_i = self.tab_widget.currentIndex()
        tab = self.tab_widget.currentWidget()
        if name == "":
            return
        with open(name, 'wb') as f:
            f.write(tab.package.convert_data_to_bytes())
            for i in tab.package.images:
                f.write(i[1])
            tab.package.filepath = name
            self.tab_widget.setTabText(tab_i, ".../" + tab.package.get_filename())
            tab.saved = True

    # Opens file dialog to open existing package
    def open_tab(self):
        name, _ = QFileDialog.getOpenFileName(self, "Open Package", "", "Silly Data Object Package (*.sdop)")
        ext = name.split(".")
        if name == "":
            return
        if len(ext) != 2 or ext[1].lower() != "sdop":
            self.error.setText("Unpackaging Error\n\nInvalid File Extension")
            self.error.show()
            return
        with open(name, 'rb') as f:
            whole = f.read()
            parts = whole.split(data.PNG_SIGNATURE)
            p = data.read_package(parts[0])
            p.filepath = name            
            for i in range(1,len(parts)):
                title = p.images[i-1]
                p.images[i-1] = (title, bytearray(data.PNG_SIGNATURE + parts[i]))
            self.add_tab(EditorTab(p,True,self.tab_widget))


# Tab Widget
class EditorTab(QWidget):
    def __init__(self, package : Package, saved, tabWidget : QTabWidget):
        super().__init__()
        self.package : Package = package
        self.saved : bool = saved
        self.tabWidget = tabWidget
        # Left side holds Name, Description, Data table, New and Delete buttons
        self.left_side = LeftLayout(package)
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.left_side)

        self.setFont(FONT)
        
        # Add spacer between the two layouts to make nicer :)
        c_spacer = QSpacerItem(50, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.layout.addItem(c_spacer)

        # Right side holds image + placeholder, blank scrolldown menu, new and delete buttons
        self.right_side = RightLayout(package)
        self.layout.addLayout(self.right_side)
        self.setLayout(self.layout)

        # Sets up save asterisk signals (* at the beginning of tab names)
        self.left_side.name_line.textChanged.connect(self.check_file_changed)
        self.left_side.desc_box.textChanged.connect(self.check_file_changed)
        self.left_side.data_box.data_table.itemChanged.connect(self.check_file_changed)
        self.right_side.data_changed_signal.connect(self.check_file_changed)
    
    # Checks if the UI boxes match with the Package object data
    def check_for_changes(self):
        return self.left_side.name_line.text() != self.package.name \
            or self.left_side.desc_box.toPlainText() != self.package.desc \
            or self.left_side.data_box.data_table.to_dict() != self.package.data \
            or self.right_side.to_list() != self.package.images

    # Changed tab name and sets tab.saved depending on check_for_changes
    def check_file_changed(self):
        i = self.tabWidget.indexOf(self)
        if self.check_for_changes():
            if self.package.filepath != "":
                self.tabWidget.setTabText(i,".../" + self.package.get_filename() + "*")
            else:
                self.tabWidget.setTabText(i, "*New Package")
            self.saved = False
        else:
            if self.package.filepath != "":
                self.tabWidget.setTabText(i, ".../" + self.package.get_filename())
                self.saved = True

    # Loads all the GUI elements' data into Package object
    def set_package_data(self):
        self.package.name = self.left_side.name_line.text()
        self.package.desc = self.left_side.desc_box.toPlainText()
        self.package.data = self.left_side.data_box.data_table.to_dict()
        self.package.images = self.right_side.to_list()
                