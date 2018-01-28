import sys

from PyQt5.QtSql import * 
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
 QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout     


class PhoneBook(QWidget):
    def __init__(self, parent = None):
        super(PhoneBook, self).__init__(parent)
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(['ID', 'NAME', 'SURNAME', 'PHONE', 'CITY', 'STREET', 'HOUSE', 'APARTMENT'])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        self.labelID = QLabel("ID")
        self.editID = QLineEdit()
        self.editID.setPlaceholderText("Unique identification number")

        self.labelName = QLabel("Name")
        self.editName = QLineEdit()
        self.editName.setPlaceholderText("Name")

        self.labelSurname = QLabel("Surname")
        self.editSurname = QLineEdit()
        self.editSurname.setPlaceholderText("Surname")

        self.labelPhone = QLabel("Phone")
        self.editPhone = QLineEdit()
        self.editPhone.setPlaceholderText("Phone number")

        self.labelCity = QLabel("City")
        self.editCity = QLineEdit()
        self.editCity.setPlaceholderText("City name")

        self.labelStreet = QLabel("Street")
        self.editStreet = QLineEdit()
        self.editStreet.setPlaceholderText("Street name")

        self.labelHouse = QLabel("House")
        self.editHouse = QLineEdit()
        self.editHouse.setPlaceholderText("House number")

        self.labelApartment = QLabel("Apartment")
        self.editApartment = QLineEdit()
        self.editApartment.setPlaceholderText("Apartment number")

        grid = QGridLayout()
        grid.addWidget(self.labelID, 0, 0)
        grid.addWidget(self.editID, 0, 1)
        grid.addWidget(self.labelName, 1, 0)
        grid.addWidget(self.editName, 1, 1)
        grid.addWidget(self.labelSurname, 2, 0)
        grid.addWidget(self.editSurname, 2, 1)
        grid.addWidget(self.labelPhone, 3, 0)
        grid.addWidget(self.editPhone, 3, 1)
        grid.addWidget(self.labelCity, 4, 0)
        grid.addWidget(self.editCity, 4, 1)
        grid.addWidget(self.labelStreet, 5, 0)
        grid.addWidget(self.editStreet, 5, 1)
        grid.addWidget(self.labelHouse, 6, 0)
        grid.addWidget(self.editHouse, 6, 1)
        grid.addWidget(self.labelApartment, 7, 0)
        grid.addWidget(self.editApartment, 7, 1)

        self.searchDataButton = QPushButton("Search")
        self.searchDataButton.clicked.connect(self.search)

        self.exitButton = QPushButton("Exit")
        self.exitButton.clicked.connect(self.close)

        hBox = QHBoxLayout()
        hBox.addWidget(self.searchDataButton)
        hBox.addWidget(self.exitButton)

        vBox = QVBoxLayout()
        vBox.addLayout(grid)
        vBox.addLayout(hBox)
        vBox.setAlignment(Qt.AlignTop)
        vBox.addWidget(self.table)

        self.setWindowTitle("Phonebook")
        self.resize(824, 320)
        self.setLayout(vBox)

    def search(self, event):
        index = 0

        idText = self.editID.text()
        nameText = self.editName.text()
        surnameText = self.editSurname.text()
        phoneText = self.editPhone.text()
        cityText = self.editCity.text()
        streetText = self.editStreet.text()
        houseText = self.editHouse.text()
        apartmentText = self.editApartment.text()

        query = QSqlQuery()
        query.exec_("select * from phonebook where id like {0} or name like '{1}' or surname like '{2}' " 
                   "or phone like {3} or city like '{4}' or street like '{5}' or house like {6} or apartment like {7}"
                   .format(idText, nameText, surnameText, phoneText, cityText, streetText, houseText, apartmentText))

        while query.next():
            ids = query.value(0)
            name = query.value(1)
            surname = query.value(2)
            phone = query.value(3)
            city = query.value(4)
            street = query.value(5)
            house = query.value(6)
            apartment = query.value(7)

            self.table.setRowCount(index + 1)
            self.table.setItem(index, 0, QTableWidgetItem(str(ids)))
            self.table.setItem(index, 1, QTableWidgetItem(name))
            self.table.setItem(index, 2, QTableWidgetItem(surname))
            self.table.setItem(index, 3, QTableWidgetItem(str(phone)))
            self.table.setItem(index, 4, QTableWidgetItem(city))
            self.table.setItem(index, 5, QTableWidgetItem(street))
            self.table.setItem(index, 6, QTableWidgetItem(str(house)))
            self.table.setItem(index, 7, QTableWidgetItem(str(apartment)))

            index += 1

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
    book = PhoneBook()
    book.db_connect('datafile', 'QSQLITE')
    book.show()
    sys.exit(app.exec_())
