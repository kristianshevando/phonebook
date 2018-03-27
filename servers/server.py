import socket
import threading
import os

from PyQt5.QtSql import *
from PyQt5.QtCore import Qt
from PyQt5 import QtNetwork
from PyQt5.QtWidgets import (QDialog, QApplication, QVBoxLayout, QPushButton,
                             QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout, QTextEdit)

class FileServerWindow(QDialog):
    def __init__(self, parent = None):
        super(FileServerWindow, self).__init__(parent)

        self.ipAddressLabel = QLabel('IP address')
        self.ipAddressLineEdit = QLineEdit()
        self.portLabel = QLabel('Port')
        self.portLineEdit = QLineEdit()

        self.informationTextEdit = QTextEdit()

        self.connectToServerButton = QPushButton('Connect')
        self.connectToServerButton.setEnabled(False)
        self.ipAddressLineEdit.textChanged[str].connect(lambda: self.connectToServerButton.setEnabled(self.ipAddressLineEdit.text() != "" 
                                                                                    and self.portLineEdit.text() != ""))
        self.portLineEdit.textChanged[str].connect(lambda: self.signInButton.setEnabled(self.ipAddressLineEdit.text() != "" 
                                                                                    and self.portLineEdit.text() != ""))

        #self.connectToServerButton.clicked.connect(self.connectToServer)

        self.exitButton = QPushButton('Exit')
        self.exitButton.clicked.connect(self.close)

        grid = QGridLayout()
        grid.addWidget(self.ipAddressLabel, 0, 0)
        grid.addWidget(self.ipAddressLineEdit, 0, 1)
        grid.addWidget(self.portLabel, 1, 0)
        grid.addWidget(self.portLineEdit, 1, 1)

        hBox = QHBoxLayout()
        hBox.addWidget(self.connectToServerButton)
        hBox.addWidget(self.exitButton)

        vBox = QVBoxLayout()
        vBox.addLayout(grid)
        vBox.addWidget(self.informationTextEdit)
        vBox.addLayout(hBox)

        self.setLayout(vBox)



def retreiveFile(server, sock):
    filename = sock.recv(1024).decode()
    if os.path.isfile(filename):
        sock.send(("EXISTS " + str(os.path.getsize(filename))).encode())
        userResponse = sock.recv(1024).decode()
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as infile:
                bytesToSend = infile.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = infile.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERROR".encode())

    sock.close()

def main(host, port):
    host = "127.0.0.1"
    port = 5000

    s = socket.socket()
    s.bind((host, port))

    s.listen(5)

    print("Server Started")

    while(True):
        c, addr = s.accept()
        print("client connected ip " + str(addr))
        t = threading.Thread(target=retreiveFile, args=("retreiveThread", c))
        t.start()
    
    s.close()



class DatabaseServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port


    def executeQuery(receivedQuery):
        queryObject = QSqlQuery()
        queryObject.exec_(receivedQuery)

#TODO: manage with queries handling, finish this class, 
#на сервере хранится база данных, идет запрос от клиента, передается в функцию, в функции этот запрос выполняется, 


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    server = FileServerWindow()
    sys.exit(server.exec_())



































# import pypyodbc

# SQLServer = "localhost"
# Database = "phonebook"

# connection = pypyodbc.connect('Driver={SQL Server};'
#                               'Server=' + SQLServer + ';'
#                               'Database=' + Database + ';')

# cursor = connection.cursor()
