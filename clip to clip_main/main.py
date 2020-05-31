import gui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
from systemhandle import SystemHandle
from info import Data

class Main():
    def __init__(self): 
        app = QtWidgets.QApplication(sys.argv)

        # first username add window
        login = gui.Login()

        if login.exec_() == QtWidgets.QDialog.Accepted:
            username = login.textName.text().strip()

            # initializing the data
            data = Data(username, '')

            # main window
            window = gui.Window(data)
            window.show()
            
            # listening to the keyboard and socket thread
            try:
                s = SystemHandle(data)
                s.start()
            except ConnectionRefusedError:
                QMessageBox.critical(window, 'Warning', 'Server is not available', QMessageBox.Ok, QMessageBox.Ok)
                window.close()
                exit()
                
            sys.exit(app.exec_())

if __name__ == "__main__":
    Main()