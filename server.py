import socket
import threading
import os

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

def main():
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

if __name__ == "__main__":
    main()



































# import pypyodbc

# SQLServer = "localhost"
# Database = "phonebook"

# connection = pypyodbc.connect('Driver={SQL Server};'
#                               'Server=' + SQLServer + ';'
#                               'Database=' + Database + ';')

# cursor = connection.cursor()
