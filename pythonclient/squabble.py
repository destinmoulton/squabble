#!/usr/bin/python

import sys
import json
import time
import squabblecrypt
import squabblegui
from PyQt4 import QtGui
from PyQt4.QtNetwork import *
from PyQt4.QtCore import *

class Squabble(QtGui.QMainWindow):

    def __init__(self):
        super(Squabble, self).__init__()

        # Set the initial time
        self.setMessageLastRecd()

        # The list of received messages
        self.receivedMessages = []

        # Setup the interval timer for getting messages
        self.checkMessagesTimer = QTimer()
        self.checkMessagesTimer.timeout.connect(self.getMessages)
        self.checkMessagesTimer.setInterval(2000)
        
        self.initUI()

        
    def initUI(self):

        self.stackedWidget = QtGui.QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.settingsWidget = squabblegui.SqSettingsWidget(self)
        self.chatWidget = squabblegui.SqChatWidget(self)
        
        self.stackedWidget.addWidget(self.settingsWidget)
        self.stackedWidget.addWidget(self.chatWidget)
        self.stackedWidget.setCurrentWidget(self.settingsWidget)

        self.settingsWidget.continueBtn.clicked.connect(self.validateUserPass)
                    
        self.chatWidget.settingsBtn.clicked.connect(self.showSettings)
        self.chatWidget.sendBtn.clicked.connect(self.sendMessage)
        
        self.setGeometry(300,300,350, 450)
        self.setWindowTitle('Squabble Chat')
        self.settingsWidget.setInitialFocus()
        self.show()


    def setupNetwork(self):
        self.tcpClient = QTcpSocket()
        host, port = self.settingsWidget.getHostAndPort()

        self.chatWidget.logNote("Hi " + self.username + "!")
        self.chatWidget.logCommand("Connecting to " + host + " on port " + str(port) + "...")
        
        self.tcpClient.connectToHost(host, port)

        # Handle the connected event
        self.tcpClient.connected.connect(self.serverConnected)

        # Handle the disconnected event
        self.tcpClient.disconnected.connect(self.serverLost)

        self.tcpClient.error.connect(self.serverError)

        
    def serverConnected(self):
        self.chatWidget.logNote("Connection successful!")

        self.chatWidget.enableMessageInput()

        # Start checking the server for messages
        self.checkMessagesTimer.start()

    def serverLost(self):
        self.chatWidget.logError("Lost connection to server...")

        # Don't let the user type while disconnected
        self.chatWidget.disableMessageInput()

        # Stop querying the server for new messages
        self.checkMessagesTimer.stop()

    def serverError(self, error):
        self.chatWidget.logError(self.tcpClient.errorString())

    def validateUserPass(self):
        usernameTmp = self.settingsWidget.getName()

        if usernameTmp is not "":
            self.username = usernameTmp
            self.passphrase = self.settingsWidget.getPassphrase()

            # Bring the chat widget to the foreground
            self.stackedWidget.setCurrentWidget(self.chatWidget)

            self.setupNetwork()


    def showSettings(self):
        dialogResponse = QtGui.QMessageBox.question(self, 'Disconnect?',
                                           "Are you sure you want to end this chat session?", QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if dialogResponse == QtGui.QMessageBox.Yes:
        
            self.chatWidget.clearLog()
        
            self.stackedWidget.setCurrentWidget(self.settingsWidget)

            
    def sendMessage(self, state):
        message = self.chatWidget.getMessage()
        
        jsonData = {
            'message': message,
            'timestamp': int(time.time())
        }
        
        self.chatWidget.addLogMessage('me', message)
        self.tcpToServer('broadcast', jsonData)
        self.chatWidget.clearMessage()

        
    def getMessages(self):
        
        jsonData = {'time_last_checked':self.messageLastRecd}
        self.tcpToServer('acquire', jsonData)
        newMessages = str(self.tcpClient.readAll())

        try:
            jsonMessages = json.loads(newMessages)
            if len(jsonMessages) >= 1:
                if isinstance(jsonMessages[0], dict):
                    if 'user' in jsonMessages[0]:
                        self.setMessageLastRecd()
                        for message in jsonMessages:
                            if message['_id'] not in self.receivedMessages:
                                self.receivedMessages.append(message['_id'])
                                self.chatWidget.addLogMessage(message['user'], message['message'])

        except(ValueError,KeyError,TypeError):
            print("JSON format error")
            

            
    def setMessageLastRecd(self):
        timestamp = int(time.time())
        self.messageLastRecd = timestamp

        
    def tcpToServer(self, command, dataDict):
        jsonData = {'command':command, 'user':self.username}
        jsonData.update(dataDict)
        jsonString = json.dumps(jsonData)
        self.tcpClient.write(QString(jsonString).toLatin1())

        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Really Quit?',
                                           "Are you sure you want to quit?", QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():

    app = QtGui.QApplication(sys.argv)
    sq = Squabble()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
