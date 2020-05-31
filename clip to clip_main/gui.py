from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QVBoxLayout, QLabel, qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui
import time
import os

class Login(QtWidgets.QDialog):
    '''
    class to handle the username and save it
    '''
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.textName = QLineEdit(self)
        self.textName.move(100, 25)
        self.textName.resize(280,40)
        label = QLabel('User Name :', self)
        label.move(20,30)

        self.buttonLogin = QPushButton('Save', self)
        self.buttonLogin.move(150,70)
        self.buttonLogin.resize(100,50)
        self.buttonLogin.setEnabled(False)
        self.textName.textChanged[str].connect(lambda: self.buttonLogin.setEnabled(self.textName.text() != ""))
        self.buttonLogin.clicked.connect(self.handleUser)

        self.setWindowTitle("Enter User Name ")
        self.setGeometry(800,400,400,130)
        layout = QVBoxLayout(self)


    def handleUser(self):
        userName = self.textName.text()
        if userName == '':
            QMessageBox.warning(self, 'Warning', 'Username cannot be empty', QMessageBox.Ok, QMessageBox.Ok)
        else:
            if len(userName) <= 20:
                self.accept()
            else:
                QMessageBox.warning(self, 'Warning', 'Username must be less than 20 character', QMessageBox.Ok, QMessageBox.Ok)

class HandleFile(QtWidgets.QDialog):
    def __init__(self, data, parent=None):
        super(HandleFile, self).__init__(parent)
        self.data = data
        
        file_location = QLabel("*your data will be saved at path = C:/clip-to-clip/", self)
        file_location.move(20,0)
        file_location.resize(290,40)

        self.fileName = QLineEdit(self)
        self.fileName.move(110, 35)
        self.fileName.resize(260,40)
        label = QLabel('Filename :', self)
        label.move(20,38)

        self.buttonAdd = QPushButton('Save', self)
        self.buttonAdd.move(155,80)
        self.buttonAdd.resize(100,40)
        self.buttonAdd.clicked.connect(self.addFile)

        self.setWindowTitle("File ")
        self.setGeometry(800,400,400,150)
        layout = QVBoxLayout(self)

    def addFile(self):
        self.data.filename = self.fileName.text()
        if self.data.filename == '':
            QMessageBox.warning(self, 'Warning', 'File name is not defined', QMessageBox.Ok, QMessageBox.Ok)
        else:
            if '.txt' not in self.data.filename:
                self.data.filename += '.txt'
            if os.path.exists(self.data.path):
                if self.data.filename in os.listdir(self.data.path):
                    QMessageBox.question(self, 'Warning', 'File already exists!!', QMessageBox.Ok, QMessageBox.Ok)
                else:
                    QMessageBox.information(self, 'Success', 'File will be created', QMessageBox.Ok, QMessageBox.Ok)
            else:
                os.mkdir(self.data.path)
                QMessageBox.information(self, 'Success', 'File will be created', QMessageBox.Ok, QMessageBox.Ok)

class Window(QtWidgets.QMainWindow):
    '''
    Main window where we need to define who we want to send the data and save it
    '''
    def __init__(self, data):
        super().__init__()
        self.title = 'Clip to Clip'
        self.left = 800
        self.top = 400
        self.width = 400
        self.height = 135
        self.data = data
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # mainMenu = self.menuBar()
        # fileMenu = mainMenu.addMenu('Group')
        # editMenu = mainMenu.addMenu('Personal')
        
        #Open on menubar
        addAct = QAction('&Add file', self)
        # addAct.setShortcut('Ctrl+A')
        addAct.setStatusTip('Add File')
        addAct.triggered.connect(self.handleFile)

        #Exit on menubar
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit applicatiion')
        exitAct.triggered.connect(qApp.quit)
        
        # addAct.triggered.connect(self.openFile)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(addAct)
        fileMenu.addAction(exitAct)

        label1 = QLabel('User Name :      '+self.data.username, self)
        label1.move(5,30)
        label1.resize(300,17)

        label2 = QLabel('To :', self)
        label2.move(50,55)
    
        # Create textbox
        self.main_textbox = QLineEdit(self)
        self.main_textbox.move(100, 55)
        self.main_textbox.resize(220,30)
        self.main_textbox.returnPressed.connect(self.on_click)
        
        # Create a button in the window
        self.button = QPushButton('Save', self)
        self.button.move(150,95)
        
        self.button.setEnabled(False)
        self.main_textbox.textChanged[str].connect(lambda: self.button.setEnabled(self.main_textbox.text() != ""))

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
    
    @pyqtSlot()
    def on_click(self):
        to_person = self.main_textbox.text()
        if to_person == '':
            QMessageBox.warning(self, 'Warning', "Person name cannot be empty", QMessageBox.Ok, QMessageBox.Ok)
        else:
            if len(to_person) <= 20:
                self.data.to_person = to_person
                QMessageBox.information(self, 'Saved', 'Name saved: ' + self.data.to_person, QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self, 'Warning', 'Person name must be less than 20 character', QMessageBox.Ok, QMessageBox.Ok)

    # @pyqtSlot()
    # def user_on_click(self):
    #     self.initUI()
    #     self.main_textbox.setText("")

    def handleFile(self):
        self.dialogs = list()
        dialog = HandleFile(self.data)
        self.dialogs.append(dialog)
        dialog.show()
