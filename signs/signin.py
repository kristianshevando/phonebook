import sys
import os.path
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import servers.server
from modes.adminmode import AdminModeWindow
from signup import SignUpWindow

from PyQt5.QtSql import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QPushButton,\
                            QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout 

with open('../phonebook/config.json') as json_file:
    config = json.load(json_file)

class SignInWindow(QDialog):
    def __init__(self, parent = None):
        super(SignInWindow, self).__init__(parent)

        self.usernameLabel = QLabel("Username")
        self.usernameLineEdit = QLineEdit()
        self.usernameLineEdit.setPlaceholderText("Username")

        self.passwordLabel = QLabel("Password")
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setPlaceholderText("Password")
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        grid = QGridLayout()
        grid.addWidget(self.usernameLabel, 0, 0)
        grid.addWidget(self.usernameLineEdit, 0, 1)
        grid.addWidget(self.passwordLabel, 1, 0)
        grid.addWidget(self.passwordLineEdit, 1, 1)

        self.signInButton = QPushButton("Sign in")
        self.signInButton.setEnabled(False)
        self.usernameLineEdit.textChanged[str].connect(lambda: self.signInButton.setEnabled(self.usernameLineEdit.text() != "" 
                                                                                    and self.passwordLineEdit.text() != ""))
        self.passwordLineEdit.textChanged[str].connect(lambda: self.signInButton.setEnabled(self.usernameLineEdit.text() != "" 
                                                                                    and self.passwordLineEdit.text() != ""))
        self.signInButton.clicked.connect(self.signIn)

        self.exitButton = QPushButton("Exit")
        self.exitButton.clicked.connect(self.close)

        hBox = QHBoxLayout()
        hBox.addWidget(self.signInButton)
        hBox.addWidget(self.exitButton)

        vBox = QVBoxLayout()
        vBox.addLayout(grid)
        vBox.addLayout(hBox)
        vBox.setAlignment(Qt.AlignTop)

        self.setWindowTitle("Sign in")
        self.resize(330, 150)
        self.setLayout(vBox)

    def signIn(self):
        usernameText = self.usernameLineEdit.text()
        passwordText = self.passwordLineEdit.text()

        signInQuery = QSqlQuery()
        signInQuery.exec_("select * from accounts where username = '{0}' and password = '{1}'".format(usernameText, passwordText))
        signInQuery.next()

        if signInQuery.isValid():
            self.close()
            self.adminModeWidget = QDialog()
            self.adminModeWindowObject = AdminModeWindow()
            self.adminModeWindowObject.__init__(self.adminModeWidget)
            self.adminModeWindowObject.initialize('../phonebook/datafile', 'QSQLITE')
            self.adminModeWindowObject.show()
        else:
            QMessageBox.critical(None, "Invalid", "Invalid username or password. Click cancel to exit.", QMessageBox.Cancel)
    
    def connectToDatabase(self, filename, server):
        accountsDatabase = QSqlDatabase.addDatabase(server)
        accountsDatabase.setDatabaseName(filename)
        if not accountsDatabase.open():
            QMessageBox.critical(None, "Cannot open database",
                    "Unable to establish a database connection.\n"
                    "This example needs SQLite support. Please read the Qt SQL "
                    "driver documentation for information how to build it.\n\n"
                    "Click Cancel to exit.", QMessageBox.Cancel)
            return False
        return True

    def createDatabase(self):
        createDatabaseQuery = QSqlQuery()
        createDatabaseQuery.exec_("create table accounts(username varchar(20), password varchar(20))")

    def initialize(self, filename, server):
        import os
        if not os.path.exists(filename):
            # self.connectToDatabase(filename, server)
            # self.createDatabase()
            self.signUpWidget = QDialog()
            self.signUpWindowObject = SignUpWindow()
            self.signUpWindowObject.__init__(self.signUpWidget)
            self.signUpWindowObject.initialize(config['ACCOUNTS_FILE_PATH'], config['SERVER'])
            self.signUpWindowObject.show()
        else:
            self.connectToDatabase(filename, server)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    signInWindowObject = SignInWindow()
    signInWindowObject.initialize(config['ACCOUNTS_FILE_PATH'], config['SERVER'])
    signInWindowObject.show()
    # signInWindowObject.show()
    sys.exit(app.exec_())
