import sys, os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

( Ui_LoginDialog, QDialog ) = uic.loadUiType( os.path.join(os.path.dirname( __file__ ), 'LoginDialog.ui' ))

class LoginDialog(QtGui.QDialog):
    
    

    def __init__(self, username):
        QtGui.QWidget.__init__(self)

        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)
        
        self.ui.usernameLineEdit.setText(username)
        self.isOK = False
        
    def loginOK(self):
        
        self.username = self.ui.usernameLineEdit.text()
        self.password = self.ui.passwordLineEdit.text()
        
        if len(self.username) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Login Dialog - Error")
            warningMessage.setText("No usernames supplied!")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        if len(self.password) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Login Dialog - Error")
            warningMessage.setText("No password supplied!")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        self.isOK = True
        self.accept()
        
    def loginCancel(self):
        self.isOK = False
        self.reject()
        
    def getLoginCredentials(self):
        return self.username,self.password
