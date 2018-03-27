import sys
import json

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QPushButton, \
                            QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout

with open('../phonebook/config.json') as json_file:
    config = json.load(json_file)

class SignUpWindow(QDialog):
    def __init__(self, parent = None):
        super(SignUpWindow, self).__init__(parent)

        self.usernameLabel = QLabel('Username')
        self.usernameLineEdit = QLineEdit()
        self.usernameLineEdit.setPlaceholderText('Create username')

        self.passwordLabel = QLabel('Password')
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setPlaceholderText('Create password')
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

        self.confirmPasswordLabel = QLabel('Confirm password')
        self.confirmPasswordLineEdit = QLineEdit()
        self.confirmPasswordLineEdit.setPlaceholderText('Confirm password')
        self.confirmPasswordLineEdit.setEchoMode(QLineEdit.Password)

        grid = QGridLayout()
        grid.addWidget(self.usernameLabel, 0, 0)
        grid.addWidget(self.usernameLineEdit, 0, 1)
        grid.addWidget(self.passwordLabel, 1, 0)
        grid.addWidget(self.passwordLineEdit, 1, 1)
        grid.addWidget(self.confirmPasswordLabel, 2, 0)
        grid.addWidget(self.confirmPasswordLineEdit, 2, 1)

        self.signUpButton = QPushButton('Sign up')
        self.signUpButton.setEnabled(False)
        self.usernameLineEdit.textChanged[str].connect(lambda: self.signUpButton.setEnabled(self.usernameLineEdit.text() != ""
                                            and self.passwordLineEdit.text() != "" and self.confirmPasswordLineEdit.text() != ""))
        self.passwordLineEdit.textChanged[str].connect(lambda: self.signUpButton.setEnabled(self.usernameLineEdit.text() != ""
                                            and self.passwordLineEdit.text() != "" and self.confirmPasswordLineEdit.text() != ""))
        self.confirmPasswordLineEdit.textChanged[str].connect(lambda: self.signUpButton.setEnabled(self.usernameLineEdit.text() != ""
                                            and self.passwordLineEdit.text() != "" and self.confirmPasswordLineEdit.text() != ""))
        self.signUpButton.clicked.connect(self.signUp)

        self.exitButton = QPushButton('Exit')
        self.exitButton.clicked.connect(self.close)

        hBox = QHBoxLayout()
        hBox.addWidget(self.signUpButton)
        hBox.addWidget(self.exitButton)

        vBox = QVBoxLayout()
        vBox.addLayout(grid)
        vBox.addLayout(hBox)
        vBox.setAlignment(Qt.AlignTop)

        self.setWindowTitle('Sign up')
        self.resize(330, 150)
        self.setLayout(vBox)

    def signUp(self):
        usernameText        = self.usernameLineEdit.text()
        passwordText        = self.passwordLineEdit.text()
        confirmPasswordText = self.confirmPasswordLineEdit.text()

        if passwordText == confirmPasswordText:
            signUpQuery = QSqlQuery()
            signUpQuery.exec_("insert into accounts values('{0}', '{1}')".format(usernameText, passwordText))
            QMessageBox.setText(None, 'Well done! \n Now you have an access to the system')
        else:
            QMessageBox.critical(None, 'Error', 'Passwords are not equal.\n Try again. Click cancel to exit.', QMessageBox.Cancel)

    def connectToDatabase(self, filename, server):
        database = QSqlDatabase.addDatabase(server)
        database.setDatabaseName(filename)
        if not database.open():
            QMessageBox.critical(None, 'Cannot open database',
                    'Unable to establish a database connection.\n'
                    'This example needs SQLite support. Please read the Qt SQL '
                    'driver documentation for information how to build it.\n\n'
                    'Click Cancel to exit.', QMessageBox.Cancel)
            return False
        return True

    def createDatabase(self):
        createDatabaseQuery = QSqlQuery()
        createDatabaseQuery.exec_('create table accounts(username varchar(20), password varchar(20))')

    def initialize(self, filename, server):
        import os
        if not os.path.exists(filename):
            self.connectToDatabase(filename, server)
            self.createDatabase()
        else:
            self.connectToDatabase(filename, server)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    signUpWindowObject = SignUpWindow()
    signUpWindowObject.initialize(config['ACCOUNTS_FILE_PATH'], config['SERVER'])
    signUpWindowObject.show()
    sys.exit(app.exec_())

