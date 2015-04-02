from PyQt4 import QtCore, QtGui

class SqSettingsWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(SqSettingsWidget, self).__init__(parent)

        self.usernameInput = QtGui.QLineEdit()

        self.passphraseInput = QtGui.QLineEdit()

        self.hostInput = QtGui.QLineEdit("localhost")

        self.portInput = QtGui.QLineEdit("7777")

        self.continueBtn = QtGui.QPushButton('Continue', self)
        self.continueBtn.resize(self.continueBtn.sizeHint())
        
        formLayout = QtGui.QFormLayout()
        formLayout.addRow("Name", self.usernameInput)
        formLayout.addRow("Decryption Phrase", self.passphraseInput)
        formLayout.addRow("Host", self.hostInput)
        formLayout.addRow("Port", self.portInput)
        formLayout.addRow("", self.continueBtn)

        middleVbox = QtGui.QVBoxLayout()
        middleVbox.addStretch(1)
        middleVbox.addLayout(formLayout)
        middleVbox.addStretch(1)

        self.setLayout(middleVbox)

    def getHostAndPort(self):
        return str(self.hostInput.text()), int(self.portInput.text())

    def getName(self):
        return str(self.usernameInput.text())

    def getPassphrase(self):
        return str(self.passphraseInput.text())

    def setInitialFocus(self):
       self.usernameInput.setFocus()
