#!/usr/bin/python

# Created by Euan A. Thoms <euan@potensol.com>
#
# Copyright Under the Simplified BSD  License

import sys
sys.path.append("/usr/share/netdrive-connector")
from PyQt4 import QtCore, QtGui
import subprocess
from ui_NetdriveConnectorWidget import Ui_NetdriveConnectorWidget
from LoginDialog import LoginDialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class NetdriveConnector(QtGui.QWidget):
    
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.ui = Ui_NetdriveConnectorWidget()
        self.ui.setupUi(self)
        
        #shellCommand = str("whoami")
        #self.username = str (subprocess.check_output(shellCommand,shell=True)).splitlines()[0]
        
        self.getHomeFolder()

        self.loadConnectionsTable()
        
    def loadConnectionsTable(self):
        
        self.ui.connectionsListWidget.clear()
        
        shellCommand = str("cat /etc/fstab | grep ' davfs '")
        if subprocess.call(shellCommand,shell=True) == 0:
            davfsConnections = str (subprocess.check_output(shellCommand,shell=True)).splitlines()
        else:
            davfsConnections = None
        
        shellCommand = str("cat /etc/fstab | grep ' fuse.sshfs '")
        if subprocess.call(shellCommand,shell=True) == 0:
            sftpConnections = str (subprocess.check_output(shellCommand,shell=True)).splitlines()
        else:
            sftpConnections = None
            
        if davfsConnections != None:
            self.ui.connectionsListWidget.addItems(davfsConnections)
        if sftpConnections != None:
            self.ui.connectionsListWidget.addItems(sftpConnections)
        
        for i in range(self.ui.connectionsListWidget.count()):
            listItem = self.ui.connectionsListWidget.item(i)
            mountpoint =  listItem.text().split(' ')[1]
            shellCommand = str("mount | grep ' " + mountpoint + " '")
            if subprocess.call(shellCommand,shell=True) == 0:
                listItem.setBackgroundColor(QtGui.QColor(100,200,100,80))
            else:
                listItem.setBackgroundColor(QtGui.QColor(250,120,10,80))
                
    def clearSftpFields(self):
        self.ui.sftpUsernameLineEdit.clear()
        self.ui.sftpHostnameLineEdit.clear()
        self.ui.sftpPortSpinBox.setValue(22)
        self.ui.sftpPathLineEdit.clear()
        self.ui.sftpMountpointLineEdit.clear()
        self.ui.sftpPasswordlessCheckBox.setChecked(True)
        self.ui.sftpPasswordLineEdit.clear()
        self.ui.sftpAutoMountCheckBox.setCheckable(True)
        self.ui.sftpAutoMountCheckBox.setChecked(False)
        
        
    def clearWebdavFields(self):
        self.ui.webdavServerUrlLineEdit.clear()
        self.ui.webdavUriLineEdit.clear()
        self.ui.webdavMountpointLineEdit.clear()
        self.ui.httpRadioButton.setChecked(True)
        self.ui.webdavProtocolLbl.setText("http://")
        self.ui.webdavPortSpinBox.setValue(80)
        self.ui.webdavUsernameLineEdit.clear()
        self.ui.webdavPasswordLineEdit.clear()
        self.ui.webdavAutoMountCheckBox.setCheckable(True)
        self.ui.webdavAutoMountCheckBox.setChecked(False)
        
    def sftpPasswordlessCheckBoxClicked(self):
        
        if self.ui.sftpPasswordlessCheckBox.isChecked():
            self.ui.sftpAutoMountCheckBox.setCheckable(True)
        else:
            self.ui.sftpAutoMountCheckBox.setChecked(False)
            self.ui.sftpAutoMountCheckBox.setCheckable(False)
            
    def webdavSavePasswordCheckBoxClicked(self):
        
        if self.ui.webdavSavePasswordCheckBox.isChecked():
            self.ui.webdavAutoMountCheckBox.setCheckable(True)
        else:
            self.ui.webdavAutoMountCheckBox.setChecked(False)
            self.ui.webdavAutoMountCheckBox.setCheckable(False)
            
        
    
    def connectBtnClicked(self):
        
        if len(self.ui.connectionsListWidget.selectedItems()) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("No connection selected. Please select a filesystem to connect.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        toConnect = self.ui.connectionsListWidget.selectedItems()[0].text()
        filesystem = toConnect.split(' ')[0]
        mountpoint =  toConnect.split(' ')[1]
        fsType = toConnect.split(' ')[2]
        
        shellCommand = str("mount | grep ' " + mountpoint + " '")
        if subprocess.call(shellCommand,shell=True) == 0:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("The selected filesystem is already mounted.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        shellCommand = str("cat '" + self.homeFolder + "/.davfs2/secrets' | grep '^" + filesystem +" '")
        if fsType == "davfs" and subprocess.call(shellCommand,shell=True) != 0:
            isPasswordSaved = False
            loginDialog = LoginDialog("")
            loginDialog.exec_()
            if not loginDialog.isOK:
                return False
            else:
                username,password = loginDialog.getLoginCredentials()
                shellCommand = str("echo '" + filesystem + " " + username + " " + password + "' >> '" + self.homeFolder + "/.davfs2/secrets'")
                if subprocess.call(shellCommand,shell=True) != 0:
                    warningMessage = QtGui.QMessageBox(self)
                    warningMessage.setWindowTitle("Netdrive Connector - Error")
                    warningMessage.setText("ERROR: Failed to add username/password to secrets file.")
                    warningMessage.setIcon(QtGui.QMessageBox.Warning)
                    warningMessage.show()
        else:
            isPasswordSaved = True
            
        shellCommand = str("mount " + mountpoint)
        if subprocess.call(shellCommand,shell=True) != 0:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("Failed to connect filesystem: " + filesystem)
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
        else:
            successMessage = QtGui.QMessageBox(self)
            successMessage.setWindowTitle("Netdrive Connector - Success")
            successMessage.setText("Successfully connected the remote filesystem: " + filesystem )
            successMessage.setIcon(QtGui.QMessageBox.Information)
            successMessage.show()
            
        if not isPasswordSaved:
            #TODO: check for GNU/LInux or *BSD and use specific sed in-place command
            shellCommand =  str('sed -i "\|^' + filesystem + ' .*|d" "' + self.homeFolder + '/.davfs2/secrets"')
            if subprocess.call(shellCommand,shell=True) != 0:
                warningMessage = QtGui.QMessageBox(self)
                warningMessage.setWindowTitle("Netdrive Connector - Error")
                warningMessage.setText("ERROR: Failed to remove username/password from secrets file.")
                warningMessage.setIcon(QtGui.QMessageBox.Warning)
                warningMessage.show()
                
        self.loadConnectionsTable()
            
    def disconnectBtnClicked(self):
        
        if len(self.ui.connectionsListWidget.selectedItems()) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("No connection selected. Please select a filesystem to disconnect.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        toDisconnect = self.ui.connectionsListWidget.selectedItems()[0].text()
        mountpoint =  toDisconnect.split(' ')[1]
        
        shellCommand = str("mount | grep ' " + mountpoint + " '")
        if subprocess.call(shellCommand,shell=True) != 0:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("The selected filesystem is not currently mounted.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        shellCommand = str("umount " + mountpoint)
        if subprocess.call(shellCommand,shell=True) != 0:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("Failed to disconnect mount point: " + mountpoint + " . Try to save and close all open files, exit the folder and try again." )
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
        else:
            successMessage = QtGui.QMessageBox(self)
            successMessage.setWindowTitle("Netdrive Connector - Success")
            successMessage.setText("Successfully disconnected the remote filesystem mounted at: " + mountpoint)
            successMessage.setIcon(QtGui.QMessageBox.Information)
            successMessage.show()
            
        self.loadConnectionsTable()
            
    def removeBtnClicked(self):
        
        connection = self.ui.connectionsListWidget.selectedItems()[0].text()
        filesystem = connection.split(' ')[0]
        mountpoint =  connection.split(' ')[1]
        fsType = connection.split(' ')[2]
        
        shellCommand = str("mount | grep ' " + mountpoint + " '")
        if subprocess.call(shellCommand,shell=True) == 0:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("The selected filesystem is currently mounted. Disconnect before trying to remove the connection.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
        
        reply = QtGui.QMessageBox.question(self, 'Netdrive Connector',"Are you sure that you want to remove this connection?", \
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.No:
            return False
        
        if fsType == "davfs":
            removeCmd = "remove-webdav-connector"
        elif fsType == "fuse.sshfs":
            removeCmd = "remove-sftp-connector"
        
        shellCommand = str("kdesu " + removeCmd + " " + filesystem + " "  + mountpoint)
        if subprocess.call(shellCommand,shell=True) != 0:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("Failed to remove the connection to : " + filesystem )
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
        
        mountpointNoSlashes = str(mountpoint).replace("/","_")
        
        shellCommand = str("rm " + self.homeFolder + "/.config/autostart/netdrive_connector" + mountpointNoSlashes + ".desktop" )
        if subprocess.call(shellCommand,shell=True) != 0:
            print "WARNING: problem whilst removing autostart file."
        
        shellCommand = str("rm " + self.homeFolder + "/.kde/shutdown/netdrive_connector" + mountpointNoSlashes + ".sh" )
        if subprocess.call(shellCommand,shell=True) != 0:
            print "WARNING: problem whilst removing auto-shutdown file."
        
        self.loadConnectionsTable()
            
    def makeShortcutBtnClicked(self):
        pass
    
    def addSftpBtnClicked(self):
        
        sftpUsername= self.ui.sftpUsernameLineEdit.text()
        sftpHostname= self.ui.sftpHostnameLineEdit.text()
        sftpPort = str(self.ui.sftpPortSpinBox.value())
        sftpMountpoint = self.ui.sftpMountpointLineEdit.text()
        sftpPath = self.ui.sftpPathLineEdit.text()
        sftpPassword = self.ui.sftpPasswordLineEdit.text()
        
        if len(str(sftpUsername).replace(" ","")) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("No valid username. Please enter a valid username.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        if len(str(sftpHostname).replace(" ","")) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("No valid hostname. Please enter a valid hostname.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        if len(str(sftpPath).replace(" ","")) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("No valid path. Please enter a valid path.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        if len(str(sftpMountpoint).replace(" ","")) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("No mount point (folder) selected. Please select a folder to use as a mount point.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        if self.ui.sftpPasswordlessCheckBox.isChecked() and len(str(sftpPassword).replace(" ","")) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("No SFTP password supplied. Please enter the password for the user on the server.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        shellCommand = str("kdesu add-sftp-connector '" + sftpUsername + "@" + sftpHostname + ":" + sftpPort + "/" + sftpPath + "' '" + sftpMountpoint + "'")
        if self.ui.sftpPasswordlessCheckBox.isChecked():
            shellCommand = str(shellCommand + " key " + sftpPassword) 
        if subprocess.call(shellCommand,shell=True) != 0:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("Failed to add the connection. ")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
        else:
            if self.ui.sftpAutoMountCheckBox.isChecked():
                self.addAutoMount(sftpMountpoint)
            self.clearSftpFields()
            self.loadConnectionsTable()
    
    def addWebdavBtnClicked(self):
        
        webdavProtocol = self.ui.webdavProtocolLbl.text()
        webdavURL = self.ui.webdavServerUrlLineEdit.text()
        webdavPort = str(self.ui.webdavPortSpinBox.value())
        webdavMountpoint = self.ui.webdavMountpointLineEdit.text()
        webdavURI = self.ui.webdavUriLineEdit.text()
        webdavUsername = self.ui.webdavUsernameLineEdit.text()
        webdavPassword = self.ui.webdavPasswordLineEdit.text()
        
        
            
        if len(str(webdavURL).replace(" ","")) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("No valid server URL. Please enter a valid server URL.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        if len(str(webdavURI).replace(" ","")) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("No valid WebDAV URI. Please enter a valid WebDAV URI.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        if len(str(webdavMountpoint).replace(" ","")) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("No mount point (folder) selected. Please select a folder to use as a mount point.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        if self.ui.webdavSavePasswordCheckBox.isChecked() and len(str(webdavUsername).replace(" ","")) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("No valid WebDAV username supplied. Please enter a valid WebDAV username.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        if self.ui.webdavSavePasswordCheckBox.isChecked() and len(str(webdavPassword).replace(" ","")) < 1:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("No WebDAV password supplied. Please enter the WebDAV password.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False
            
        shellCommand = str("kdesu add-webdav-connector '"+ webdavProtocol + webdavURL + ":" + webdavPort + "/" + webdavURI + "' '" + webdavMountpoint + "'")
        if self.ui.webdavSavePasswordCheckBox.isChecked():
            shellCommand = str(shellCommand + " " + webdavUsername + " " + webdavPassword) 
        if subprocess.call(shellCommand,shell=True) != 0:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("Failed to add the connection. ")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
        else:
            if self.ui.webdavAutoMountCheckBox.isChecked():
                self.addAutoMount(webdavMountpoint)
            self.clearWebdavFields()
            self.loadConnectionsTable()

    def sftpMountpointBtnClicked(self):
        
        mountpoint = QtGui.QFileDialog.getExistingDirectory(self, 'Select mount point',self.homeFolder)
        
        if mountpoint == self.homeFolder:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Warning")
            warningMessage.setText("WARNING: The selected folder is your home folder. Mounting a remote filesystem to your home folder is not recommended.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            
        if self.isMountpointOwnedByCurrentUser(mountpoint):
            self.ui.sftpMountpointLineEdit.setText(mountpoint)
        else:
            errorMessage = QtGui.QErrorMessage(self)
            errorMessage.setWindowTitle("Netdrive Connector - Error")
            errorMessage.showMessage("ERROR: you are not the owner of the selected folder. Please change ownership of the folder or select a different mount point.")
    
    def webdavMountpointBtnClicked(self):
        
        mountpoint = QtGui.QFileDialog.getExistingDirectory(self, 'Select mount point',self.homeFolder)
        
        if mountpoint == self.homeFolder:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Warning")
            warningMessage.setText("WARNING: The selected folder is your home folder. Mounting a remote filesystem to your home folder is not recommended.")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            
        if self.isMountpointOwnedByCurrentUser(mountpoint):
            self.ui.webdavMountpointLineEdit.setText(mountpoint)
        else:
            errorMessage = QtGui.QErrorMessage(self)
            errorMessage.setWindowTitle("Netdrive Connector - Error")
            errorMessage.showMessage("ERROR: you are not the owner of the selected folder. Please change ownership of the folder or select a different mount point.")
    
    def httpRadioBtnClicked(self):
        
        self.ui.webdavProtocolLbl.setText("http://")
        
        if self.ui.webdavPortSpinBox.value() == 443:
            self.ui.webdavPortSpinBox.setValue(80)
    
    def httpsRadioBtnClicked(self):
        
        self.ui.webdavProtocolLbl.setText("https://")
        
        if self.ui.webdavPortSpinBox.value() == 80:
            self.ui.webdavPortSpinBox.setValue(443)
            
    def getHomeFolder(self):
        
        self.homeFolder = str (subprocess.check_output("echo $HOME",shell=True)).splitlines()[0]
            
    def isMountpointOwnedByCurrentUser(self, mountpoint):
        
        currentUser = str (subprocess.check_output("whoami",shell=True)).splitlines()[0]
        
        shellCommand = str ("ls -ld " + mountpoint + " | awk '{print $3}'")
        
        folderOwner = str (subprocess.check_output(shellCommand,shell=True)).splitlines()[0]
        
        if folderOwner != currentUser:
            return False
        else:
            return True
            
    def addAutoMount(self, mountpoint):
        
        mountpointNoSlashes = str(mountpoint).replace("/","_")
        
        fileContents =\
"""
[Desktop Entry]
Name=Netdrive AutoMounter
Hidden=false
StartupNotify=false
Terminal=false
TerminalOptions=
Type=Application
X-DBUS-ServiceName=
X-DBUS-StartupType=unique
X-KDE-SubstituteUID=false
X-KDE-Username=
"""
        fileContents = str(fileContents + "Exec=mount " + mountpoint)
        shellCommand = str("if [ ! -d " + self.homeFolder + "/.config/autostart ]; then mkdir " + self.homeFolder + "/.config/autostart ; fi ; echo '" + fileContents + "' > " + self.homeFolder + "/.config/autostart/netdrive_connector" + mountpointNoSlashes + ".desktop" )
        if subprocess.call(shellCommand,shell=True) != 0:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("An error occured whilst creating the autostart file in " + self.homeFolder + "/.config/autostart .")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False

        fileContents=\
"""
#!/bin/bash

"""
        fileContents = str(fileContents + "umount " + mountpoint)
        shellCommand = str("if [ ! -d " + self.homeFolder + "/.kde/shutdown ]; then mkdir " + self.homeFolder + "/.kde/shutdown ; fi ; echo '" + fileContents + "' > " + self.homeFolder + "/.kde/shutdown/netdrive_connector" + mountpointNoSlashes + ".sh; chmod +x " + self.homeFolder + "/.kde/shutdown/netdrive_connector" + mountpointNoSlashes + ".sh" )
        if subprocess.call(shellCommand,shell=True) != 0:
            warningMessage = QtGui.QMessageBox(self)
            warningMessage.setWindowTitle("Netdrive Connector - Error")
            warningMessage.setText("An error occured whilst creating the auto-shutdown file in " + self.homeFolder + "/.kde/shutdown .")
            warningMessage.setIcon(QtGui.QMessageBox.Warning)
            warningMessage.show()
            return False

def main():
    app = QtGui.QApplication(sys.argv)
    netdriveConnector = NetdriveConnector()
    layout = QtGui.QGridLayout()
    layout.addWidget(netdriveConnector)
    netdriveConnectorDialog = QtGui.QDialog()        
    netdriveConnectorDialog.setLayout(layout)
    netdriveConnectorDialog.setWindowTitle("Netdrive Connector")
    netdriveConnectorDialog.resize(700,600)
    netdriveConnectorDialog.setWindowIcon(QtGui.QIcon('/usr/share/icons/netdrive-connector.png'))
    netdriveConnectorDialog.exec_()
    sys.exit()

if __name__ == '__main__':
    main()
