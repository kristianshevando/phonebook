import sys

from PyQt5.QtSql import *  
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
 QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout 


class SignUp(QWidget):
    def __init__(self, parent = None):
        super(SignUp, self).__init__(parent)

        self.labelUsername = QLabel("Username")
        self.editUsername = QLineEdit()
        self.editUsername.setPlaceholderText("Create username")

        self.labelPassword = QLabel("Password")
        self.editPassword = QLineEdit()
        self.editPassword.setPlaceholderText("Create password")
        self.editPassword.setEchoMode(QLineEdit.Password)

        self.labelConfirmPassword = QLabel("Confirm password")
        self.editConfirmPassword = QLineEdit()
        self.editConfirmPassword.setPlaceholderText("Confirm password")
        self.editConfirmPassword.setEchoMode(QLineEdit.Password)

        grid = QGridLayout()
        grid.addWidget(self.labelUsername, 0, 0)
        grid.addWidget(self.editUsername, 0, 1)
        grid.addWidget(self.labelPassword, 1, 0)
        grid.addWidget(self.editPassword, 1, 1)
        grid.addWidget(self.labelConfirmPassword, 2, 0)
        grid.addWidget(self.editConfirmPassword, 2, 1)    

        self.signUpButton = QPushButton("Sign up")
        self.signUpButton.setEnabled(False)
        self.editUsername.textChanged[str].connect(lambda: self.signUpButton.setEnabled(self.editUsername.text() != "" 
        and self.editPassword.text() != "" and self.editConfirmPassword.text() != ""))
        self.editPassword.textChanged[str].connect(lambda: self.signUpButton.setEnabled(self.editUsername.text() != "" 
        and self.editPassword.text() != "" and self.editConfirmPassword.text() != ""))
        self.editConfirmPassword.textChanged[str].connect(lambda: self.signUpButton.setEnabled(self.editUsername.text() != "" 
        and self.editPassword.text() != "" and self.editConfirmPassword.text() != ""))
        self.signUpButton.clicked.connect(self.signUp)

        self.exitButton = QPushButton("Exit")
        self.exitButton.clicked.connect(self.close)

        hBox = QHBoxLayout()
        hBox.addWidget(self.signUpButton)
        hBox.addWidget(self.exitButton)

        vBox = QVBoxLayout()
        vBox.addLayout(grid)
        vBox.addLayout(hBox)
        vBox.setAlignment(Qt.AlignTop)

        self.setWindowTitle("Sign in")
        self.resize(330, 150)
        self.setLayout(vBox)

    def signUp(self):
        username = self.editUsername.text()
        password = self.editPassword.text()
        confirmPassword = self.editConfirmPassword.text()

        query = QSqlQuery()

        if password == confirmPassword:
            query.exec_("insert into accounts values('{0}', '{1}')".format(username, password))
        else:
            QMessageBox.critical(None, "Error", "Passwords are not equal.\n Try again. Click cancel to exit.", QMessageBox.Cancel)
        #    self.close()
        # if query.isValid():
        #     QMessageBox.critical(None, "Cannot open database",
        #             "Unable to establish a database connection.\n"
        #             "This example needs SQLite support. Please read the Qt SQL "
        #             "driver documentation for information how to build it.\n\n"
        #             "Click Cancel to exit.", QMessageBox.Cancel)
        # else:
        #     pass

    def enableButton(self):
        if len(self.editUsername.text()) > 0 and len(self.editPassword.text()) > 0:
            self.logInButton.setEnabled(True)
        else:
            self.logInButton.setEnabled(False)

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
    administrator = SignUp()
    administrator.init('accounts', 'QSQLITE')
    administrator.show()
    sys.exit(app.exec_())
