import sys, os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

( Ui_RootPasswordDialog, QDialog ) = uic.loadUiType( os.path.join(os.path.dirname( __file__ ), 'RootPasswordDialog.ui' ))

class RootPasswordDialog(QtGui.QDialog):


    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.ui = Ui_RootPasswordDialog()
        self.ui.setupUi(self)
        
        self.isOK = False
        
    def loginOK(self):
        
        self.password = self.ui.passwordLineEdit.text()
        
        if len(self.password) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Data Entry Error")
            warningMessage.setText("No password supplied!")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        self.isOK = True
        self.accept()
        
    def loginCancel(self):
        self.isOK = False
        self.reject()
        
    def getRootPassword(self):
        return self.password
