#!/usr/bin/python

# Created by Euan A. Thoms <euan@potensol.com>
#
# Copyright Under the Simplified BSD  License


import sys
sys.path.append("/usr/share/netdrive-connector")
from PyQt4 import QtCore, QtGui
from ui_LoginDialog import Ui_LoginDialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


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
            warningMessage.setText("No username supplied!")
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