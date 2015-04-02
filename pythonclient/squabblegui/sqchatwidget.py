from PyQt4 import QtCore, QtGui

class SqChatWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(SqChatWidget, self).__init__(parent)

        self.sendBtn = QtGui.QPushButton('Send', self)
        self.sendBtn.resize(self.sendBtn.sizeHint())

        self.settingsBtn = QtGui.QPushButton('Settings', self)
        self.settingsBtn.resize(self.settingsBtn.sizeHint())

        # Put the button in an hbox with a spacer
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.settingsBtn)
        hbox.addStretch(1)
        hbox.addWidget(self.sendBtn)

        self.log = QtGui.QTextEdit(self)
        self.log.setReadOnly(True)
        
        self.message = QtGui.QTextEdit(self)
        # Don't allow initial messages
        self.disableMessageInput()

        chatVbox = QtGui.QVBoxLayout()
        chatVbox.addWidget(self.log)
        chatVbox.addWidget(self.message)
        chatVbox.addLayout(hbox)
        #chatVbox.addLayout(mainVbox)

        self.setLayout(chatVbox)

    def clearLog(self):
        self.log.clear()
        
    def clearMessage(self):
        self.message.clear()

        
    def getMessage(self):
        return str(self.message.toPlainText())

        
    def addLogMessage(self, user, message):
        text = "<b>"+user + " ></b> " + message
        self.log.append(text)
        self.log.append("")

    def logError(self, message):
        self.addLogNotification(message, "red")

    def logNote(self, message):
        self.addLogNotification(message, "blue")

    def logCommand(self, message):
        self.addLogNotification(message, "green")

    def addLogNotification(self, notice, color="black"):
        text = "<span style='color:" + color + "'>" + notice + "</span>"
        self.log.append(text)
        self.log.append("")
        

    def disableMessageInput(self):
        self.message.setReadOnly(True)

        
    def enableMessageInput(self):
        self.message.setReadOnly(False)
