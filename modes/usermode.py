import sys

from PyQt5.QtSql import * 
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
 QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout     
from PyQt5 import QtNetwork

class UserModeWindow(QWidget):
    def __init__(self, parent = None):
        super(UserModeWindow, self).__init__(parent)

        self.phonebookTable = QTableWidget(0, 7)
        self.phonebookTable.setHorizontalHeaderLabels(['NAME', 'SURNAME', 'PHONE', 'CITY', 'STREET', 'HOUSE', 'APARTMENT'])        
        self.phonebookTable.setAlternatingRowColors(True)
        self.phonebookTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.phonebookTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.phonebookTable.setSelectionMode(QTableWidget.SingleSelection)

        self.nameLabel = QLabel("Name")
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setPlaceholderText("Name")

        self.surnameLabel = QLabel("Surname")
        self.surnameLineEdit = QLineEdit()
        self.surnameLineEdit.setPlaceholderText("Surname")

        self.phoneLabel = QLabel("Phone")
        self.phoneLineEdit = QLineEdit()
        self.phoneLineEdit.setText("0")
        self.phoneLineEdit.setPlaceholderText("Phone number")

        self.cityLabel = QLabel("City")
        self.cityLineEdit = QLineEdit()
        self.cityLineEdit.setPlaceholderText("City name")

        self.streetLabel = QLabel("Street")
        self.streetLineEdit = QLineEdit()
        self.streetLineEdit.setPlaceholderText("Street name")

        self.houseLabel = QLabel("House")
        self.houseLineEdit = QLineEdit()
        self.houseLineEdit.setText("0")
        self.houseLineEdit.setPlaceholderText("House number")

        self.apartmentLabel = QLabel("Apartment")
        self.apartmentLineEdit = QLineEdit()
        self.apartmentLineEdit.setText("0")
        self.apartmentLineEdit.setPlaceholderText("Apartment number")

        grid = QGridLayout()
        grid.addWidget(self.nameLabel, 0, 0)
        grid.addWidget(self.nameLineEdit, 0, 1)
        grid.addWidget(self.surnameLabel, 1, 0)
        grid.addWidget(self.surnameLineEdit, 1, 1)
        grid.addWidget(self.phoneLabel, 2, 0)
        grid.addWidget(self.phoneLineEdit, 2, 1)
        grid.addWidget(self.cityLabel, 3, 0)
        grid.addWidget(self.cityLineEdit, 3, 1)
        grid.addWidget(self.streetLabel, 4, 0)
        grid.addWidget(self.streetLineEdit, 4, 1)
        grid.addWidget(self.houseLabel, 5, 0)
        grid.addWidget(self.houseLineEdit, 5, 1)
        grid.addWidget(self.apartmentLabel, 6, 0)
        grid.addWidget(self.apartmentLineEdit, 6, 1)

        self.searchDataButton = QPushButton("Search")
        self.searchDataButton.clicked.connect(self.search)

        self.clearTableButton = QPushButton("Clear table")  
        self.clearTableButton.clicked.connect(self.phonebookTable.clearContents)

        self.exitButton = QPushButton("Exit")
        self.exitButton.clicked.connect(self.close)

        hBox = QHBoxLayout()
        hBox.addWidget(self.searchDataButton)
        hBox.addWidget(self.clearTableButton)
        hBox.addWidget(self.exitButton)

        vBox = QVBoxLayout()
        vBox.addLayout(grid)
        vBox.addLayout(hBox)
        vBox.setAlignment(Qt.AlignTop)
        vBoxAsWidget = QWidget()
        vBoxAsWidget.setLayout(vBox)
        vBoxAsWidget.setFixedWidth(400)

        fullBox = QHBoxLayout()
        fullBox.addWidget(vBoxAsWidget)
        fullBox.addWidget(self.phonebookTable)

        self.setWindowTitle("Phonebook")
        self.resize(1130, 320)
        self.setLayout(fullBox)

    def search(self, event):
        index = 0

        nameText      = self.nameLineEdit.text()
        surnameText   = self.surnameLineEdit.text()
        phoneText     = self.phoneLineEdit.text()
        cityText      = self.cityLineEdit.text()
        streetText    = self.streetLineEdit.text()
        houseText     = self.houseLineEdit.text()
        apartmentText = self.apartmentLineEdit.text()

        searchQuery = QSqlQuery()
        searchQuery.exec_("select name, surname, phone, city, street, house, apartment from phonebook where name like '{0}' or surname like '{1}' " 
                   "or phone like {2} or city like '{3}' or street like '{4}' or house like {5} or apartment like {6}"
                   .format(nameText, surnameText, phoneText, cityText, streetText, houseText, apartmentText))

        while searchQuery.next():
            nameQueryValue      = searchQuery.value(0)
            surnameQueryValue   = searchQuery.value(1)
            phoneQueryValue     = searchQuery.value(2)
            cityQueryValue      = searchQuery.value(3)
            streetQueryValue    = searchQuery.value(4)
            houseQueryValue     = searchQuery.value(5)
            apartmentQueryValue = searchQuery.value(6)

            self.phonebookTable.setRowCount(index + 1)
            self.phonebookTable.setItem(index, 0, QTableWidgetItem(nameQueryValue))
            self.phonebookTable.setItem(index, 1, QTableWidgetItem(surnameQueryValue))
            self.phonebookTable.setItem(index, 2, QTableWidgetItem(str(phoneQueryValue)))
            self.phonebookTable.setItem(index, 3, QTableWidgetItem(cityQueryValue))
            self.phonebookTable.setItem(index, 4, QTableWidgetItem(streetQueryValue))
            self.phonebookTable.setItem(index, 5, QTableWidgetItem(str(houseQueryValue)))
            self.phonebookTable.setItem(index, 6, QTableWidgetItem(str(apartmentQueryValue)))

            index += 1

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

    # def db_create(self):
    #     query = QSqlQuery()
    #     query.exec_("create table phonebook(id int primary key, "
    #                "name varchar(20), surname varchar(20), phone int(10), city varchar(15), street varchar(15), house int(6), apartment int(6))")

    # def init(self, filename, server):
    #     import os
    #     if not os.path.exists(filename):
    #         self.db_connect(filename, server)
    #         self.db_create()
    #     else:
    #         self.db_connect(filename, server)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    userModeWindowObject = UserModeWindow()
    userModeWindowObject.connectToDatabase('datafile', 'QSQLITE')
    userModeWindowObject.show()
    sys.exit(app.exec_())
