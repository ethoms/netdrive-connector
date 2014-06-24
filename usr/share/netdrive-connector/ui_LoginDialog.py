# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginDialog.ui'
#
# Created: Fri Mar 21 13:10:25 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName(_fromUtf8("LoginDialog"))
        LoginDialog.resize(411, 116)
        self.gridLayout_2 = QtGui.QGridLayout(LoginDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.usernameLbl = QtGui.QLabel(LoginDialog)
        self.usernameLbl.setObjectName(_fromUtf8("usernameLbl"))
        self.gridLayout.addWidget(self.usernameLbl, 0, 0, 1, 1)
        self.label = QtGui.QLabel(LoginDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.okBtn = QtGui.QPushButton(LoginDialog)
        self.okBtn.setObjectName(_fromUtf8("okBtn"))
        self.gridLayout.addWidget(self.okBtn, 2, 0, 1, 1)
        self.cancelBtn = QtGui.QPushButton(LoginDialog)
        self.cancelBtn.setObjectName(_fromUtf8("cancelBtn"))
        self.gridLayout.addWidget(self.cancelBtn, 2, 1, 1, 1)
        self.passwordLineEdit = QtGui.QLineEdit(LoginDialog)
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setObjectName(_fromUtf8("passwordLineEdit"))
        self.gridLayout.addWidget(self.passwordLineEdit, 1, 1, 1, 3)
        self.usernameLineEdit = QtGui.QLineEdit(LoginDialog)
        self.usernameLineEdit.setObjectName(_fromUtf8("usernameLineEdit"))
        self.gridLayout.addWidget(self.usernameLineEdit, 0, 1, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)

        self.retranslateUi(LoginDialog)
        QtCore.QObject.connect(self.okBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), LoginDialog.loginOK)
        QtCore.QObject.connect(self.cancelBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), LoginDialog.loginCancel)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)
        LoginDialog.setTabOrder(self.usernameLineEdit, self.passwordLineEdit)
        LoginDialog.setTabOrder(self.passwordLineEdit, self.okBtn)
        LoginDialog.setTabOrder(self.okBtn, self.cancelBtn)

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(QtGui.QApplication.translate("LoginDialog", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.usernameLbl.setText(QtGui.QApplication.translate("LoginDialog", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LoginDialog", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.okBtn.setText(QtGui.QApplication.translate("LoginDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelBtn.setText(QtGui.QApplication.translate("LoginDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

