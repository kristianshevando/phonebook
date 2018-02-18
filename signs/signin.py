import sys

sys.path.append("../phonebook/modes/")
from adminmode import AdminMode

from PyQt5.QtSql import *  
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
 QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout 


class SignIn(QWidget):
    def __init__(self, parent = None):
        super(SignIn, self).__init__(parent)

        self.labelUsername = QLabel("Username")
        self.editUsername = QLineEdit()
        self.editUsername.setPlaceholderText("Username")

        self.labelPassword = QLabel("Password")
        self.editPassword = QLineEdit()
        self.editPassword.setPlaceholderText("Password")
        self.editPassword.setEchoMode(QLineEdit.Password)

        grid = QGridLayout()
        grid.addWidget(self.labelUsername, 0, 0)
        grid.addWidget(self.editUsername, 0, 1)
        grid.addWidget(self.labelPassword, 1, 0)
        grid.addWidget(self.editPassword, 1, 1)

        self.logInButton = QPushButton("Enter")
        self.logInButton.setEnabled(False)
        self.editUsername.textChanged[str].connect(lambda: self.logInButton.setEnabled(self.editUsername.text() != "" 
                                                                                    and self.editPassword.text() != ""))
        self.editPassword.textChanged[str].connect(lambda: self.logInButton.setEnabled(self.editUsername.text() != "" 
                                                                                    and self.editPassword.text() != ""))
        self.logInButton.clicked.connect(self.logIn)

        self.exitButton = QPushButton("Exit")
        self.exitButton.clicked.connect(self.close)

        hBox = QHBoxLayout()
        hBox.addWidget(self.logInButton)
        hBox.addWidget(self.exitButton)

        vBox = QVBoxLayout()
        vBox.addLayout(grid)
        vBox.addLayout(hBox)
        vBox.setAlignment(Qt.AlignTop)

        self.setWindowTitle("Sign in")
        self.resize(330, 150)
        self.setLayout(vBox)

    def logIn(self):
        username = self.editUsername.text()
        password = self.editPassword.text()

        query = QSqlQuery()
        query.exec_("select * from accounts where username = '{0}' and password = '{1}'".format(username, password))
        query.next()

        if query.isValid():
            self.close()
            self.widget = QWidget()
            self.admin = AdminMode()
            self.admin.__init__(self.widget)
            self.admin.init('../phonebook/datafile', 'QSQLITE')
            self.widget.show()
        else:
            QMessageBox.critical(None, "Invalid", "Invalid username or password. Click cancel to exit.", QMessageBox.Cancel)
    
    def db_connect(self, filename, server):
        db = QSqlDatabase.addDatabase(server)
        db.setDatabaseName(filename)
        if not db.open():
            QMessageBox.critical(None, "Cannot open database",
                    "Unable to establish a database connection.\n"
                    "This example needs SQLite support. Please read the Qt SQL "
                    "driver documentation for information how to build it.\n\n"
                    "Click Cancel to exit.", QMessageBox.Cancel)
            return False
        return True

    def db_create(self):
        query = QSqlQuery()
        query.exec_("create table accounts(username varchar(20), password varchar(20))")

    def init(self, filename, server):
        import os
        if not os.path.exists(filename):
            self.db_connect(filename, server)
            self.db_create()
        else:
            self.db_connect(filename, server)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    signIn = SignIn()
    signIn.init('../phonebook/accounts', 'QSQLITE')
    signIn.show()
    sys.exit(app.exec_())
