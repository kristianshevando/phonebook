import sys

sys.path.append("../phonebook/modes/")
from adminmode import AdminModeWindow

from PyQt5.QtSql import *  
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
 QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout 


class SignInWindow(QWidget):
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
            self.widget = QWidget()
            self.adminModeWindowObject = AdminModeWindow()
            self.adminModeWindowObject.__init__(self.widget)
            self.adminModeWindowObject.initialize('../phonebook/datafile', 'QSQLITE')
            self.widget.show()
        else:
            QMessageBox.critical(None, "Invalid", "Invalid username or password. Click cancel to exit.", QMessageBox.Cancel)
    
    def connectToDatabase(self, filename, server):
        database = QSqlDatabase.addDatabase(server)
        database.setDatabaseName(filename)
        if not database.open():
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
            self.connectToDatabase(filename, server)
            self.createDatabase()
        else:
            self.connectToDatabase(filename, server)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    signInWindowObject = SignInWindow()
    signInWindowObject.initialize('../phonebook/accounts', 'QSQLITE')
    signInWindowObject.show()
    sys.exit(app.exec_())
