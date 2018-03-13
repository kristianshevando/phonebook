import socket

def main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.connect((host, port))

    filename = input("Enter filename: ")
    if filename != 'q':
        s.send(filename.encode())
        data = s.recv(1024).decode()
        if data[:6] == 'EXISTS':
            filesize = int(data[6:])
            message = input("File exisits, " + str(filesize) + " bytes download(y/n)?")

            if message == "Y" or message == "y":
                s.send('OK'.encode())
                outfile = open('new_' + filename, 'wb')
                data = s.recv(1024).decode()
                totalRecv = len(data)
                outfile.write(data.encode())
                while totalRecv < filesize:
                    data = s.recv(1024).decode()
                    totalRecv += len(data)
                    outfile.write(data)
                    print("{0:.2f}".format((totalRecv/float(filesize)) * 100) + "% Done")
                print("Download complete!")
        else:
            print("File doesn't exist!")
    s.close()

if __name__ == "__main__":
    main()