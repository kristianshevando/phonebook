import sys
sys.path.append("../phonebook/signs/")

#from signup import SignUpWindow
import signin

from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QApplication

# class Phonebook:
#     def startApplication(self):
#         self.widget = QWidget()
#         signInWindowObject = SignInWindow()
#         signInWindowObject.__init__(self.widget)
#         signInWindowObject.initialize('../phonebook/accounts', 'QSQLITE')
#         self.widget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    signInWindowObject = signin.SignInWindow()
    sys.exit(app.exec_())