import sys

from PyQt5.QtSql import *
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, \
 QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout

class AdminModeWindow(QWidget):
    def __init__(self, parent = None):
        super(AdminModeWindow, self).__init__(parent)
        self.phonebookTable = QTableWidget(0, 8)
        self.phonebookTable.setHorizontalHeaderLabels(['ID', 'NAME', 'SURNAME', 'PHONE', 'CITY', 'STREET', 'HOUSE', 'APARTMENT'])
        self.phonebookTable.setAlternatingRowColors(True)
        self.phonebookTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.phonebookTable.setSelectionBehavior(QTableWidget.SelectRows)
        self.phonebookTable.setSelectionMode(QTableWidget.SingleSelection)

        self.idLabel = QLabel("ID")
        self.idLineEdit = QLineEdit()
        self.idLineEdit.setText("0")
        self.idLineEdit.setPlaceholderText("Unique identification number")

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
        grid.addWidget(self.idLabel, 0, 0)
        grid.addWidget(self.idLineEdit, 0, 1)
        grid.addWidget(self.nameLabel, 1, 0)
        grid.addWidget(self.nameLineEdit, 1, 1)
        grid.addWidget(self.surnameLabel, 2, 0)
        grid.addWidget(self.surnameLineEdit, 2, 1)
        grid.addWidget(self.phoneLabel, 3, 0)
        grid.addWidget(self.phoneLineEdit, 3, 1)
        grid.addWidget(self.cityLabel, 4, 0)
        grid.addWidget(self.cityLineEdit, 4, 1)
        grid.addWidget(self.streetLabel, 5, 0)
        grid.addWidget(self.streetLineEdit, 5, 1)
        grid.addWidget(self.houseLabel, 6, 0)
        grid.addWidget(self.houseLineEdit, 6, 1)
        grid.addWidget(self.apartmentLabel, 7, 0)
        grid.addWidget(self.apartmentLineEdit, 7, 1)

        self.downloadDataButton = QPushButton("Download")
        self.downloadDataButton.clicked.connect(self.downloadData)
        
        self.searchDataButton = QPushButton("Search")
        self.searchDataButton.clicked.connect(self.search)

        self.insertDataButton = QPushButton("Insert")
        self.insertDataButton.clicked.connect(self.insertData)

        self.clearTableButton = QPushButton("Clear")  
        self.clearTableButton.clicked.connect(self.phonebookTable.clearContents)

        self.removeDataButton = QPushButton("Remove")
        self.removeDataButton.clicked.connect(self.removeData)

        hBox = QHBoxLayout()
        hBox.addWidget(self.downloadDataButton)
        hBox.addWidget(self.searchDataButton)
        hBox.addWidget(self.insertDataButton)
        hBox.addWidget(self.clearTableButton)
        hBox.addWidget(self.removeDataButton)

        vBoxAsWidget = QWidget()

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
        self.resize(1230, 320)
        self.setLayout(fullBox)

    def search(self, event):
        idText        = int(self.idLineEdit.text())
        nameText      = self.nameLineEdit.text()
        surnameText   = self.surnameLineEdit.text()
        phoneText     = int(self.phoneLineEdit.text())
        cityText      = self.cityLineEdit.text()
        streetText    = self.streetLineEdit.text()
        houseText     = int(self.houseLineEdit.text())
        apartmentText = int(self.apartmentLineEdit.text())

        searchQuery = QSqlQuery()
        searchQuery.exec_("select * from phonebook where id like {0} or name like '{1}' or surname like '{2}' " 
                   "or phone like {3} or city like '{4}' or street like '{5}' or house like {6} or apartment like {7}"
                   .format(idText, nameText, surnameText, phoneText, cityText, streetText, houseText, apartmentText))

        self.showData(searchQuery)

    def showData(self, query):
        index = 0

        while query.next():
            idQueryValue        = query.value(0)
            nameQueryValue      = query.value(1)
            surnameQueryValue   = query.value(2)
            phoneQueryValue     = query.value(3)
            cityQueryValue      = query.value(4)
            streetQueryValue    = query.value(5)
            houseQueryValue     = query.value(6)
            apartmentQueryValue = query.value(7)

            self.phonebookTable.setRowCount(index + 1)
            self.phonebookTable.setItem(index, 0, QTableWidgetItem(str(idQueryValue)))
            self.phonebookTable.setItem(index, 1, QTableWidgetItem(nameQueryValue))
            self.phonebookTable.setItem(index, 2, QTableWidgetItem(surnameQueryValue))
            self.phonebookTable.setItem(index, 3, QTableWidgetItem(str(phoneQueryValue)))
            self.phonebookTable.setItem(index, 4, QTableWidgetItem(cityQueryValue))
            self.phonebookTable.setItem(index, 5, QTableWidgetItem(streetQueryValue))
            self.phonebookTable.setItem(index, 6, QTableWidgetItem(str(houseQueryValue)))
            self.phonebookTable.setItem(index, 7, QTableWidgetItem(str(apartmentQueryValue)))

            index += 1

    def downloadData(self, event):
        downloadDataQuery = QSqlQuery()
        downloadDataQuery.exec_("select * from phonebook")
        self.showData(downloadDataQuery)

    def insertData(self, event):
        idText        = int(self.idLineEdit.text())
        nameText      = self.nameLineEdit.text()
        surnameText   = self.surnameLineEdit.text()
        phoneText     = int(self.phoneLineEdit.text())
        cityText      = self.cityLineEdit.text()
        streetText    = self.streetLineEdit.text()
        houseText     = int(self.houseLineEdit.text())
        apartmentText = int(self.apartmentLineEdit.text())

        insertDataQuery = QSqlQuery()
        insertDataQuery.exec_("insert into phonebook values({0}, '{1}', '{2}', {3}, '{4}', '{5}', {6}, {7})".
                    format(idText, nameText, surnameText, phoneText, cityText, streetText, houseText, apartmentText))

    def removeData(self, event):
        selected = self.phonebookTable.currentIndex()
        if not selected.isValid() or len(self.phonebookTable.selectedItems()) < 1:
            return

        ids = self.phonebookTable.selectedItems()[0]
        query = QSqlQuery()
        query.exec_("remove from phonebook where id = {0}".format(ids.text()))

        self.phonebookTable.removeRow(selected.row())
        self.phonebookTable.setCurrentIndex(QModelIndex())

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
        createDatabaseQuery.exec_("create table phonebook(id int primary key, "
                   "name varchar(20), surname varchar(20), phone int(10), city varchar(15), "
                   "street varchar(15), house int(6), apartment int(6))")

    def initialize(self, filename, server):
        import os
        if not os.path.exists(filename):
            self.connectToDatabase(filename, server)
            self.createDatabase()
        else:
            self.connectToDatabase(filename, server)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    adminModeWindowObject = AdminModeWindow()
    adminModeWindowObject.initialize('../phonebook/datafile', 'QSQLITE')
    adminModeWindowObject.show()
    sys.exit(app.exec_())
