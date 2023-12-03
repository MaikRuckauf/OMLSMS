import re
from datetime import date
from constants import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *

import ui
from formviewdlg import MainDlg

import sys
sys.path.append(OMLWEB_PATH)
# sys.path is for the following import,  which can't be done here without
# violating django initialization: from omlweb.models import Dentist
from django.conf import settings

class LoginDlg(MainDlg, ui.Ui_loginDlg):

    def __init__(self, userName=None, parent=None):
        super(LoginDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("OML Database (Login Required)")
        self.loginPushButton.setFocusPolicy(Qt.NoFocus)
        self.exitPushButton.setFocusPolicy(Qt.NoFocus)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.statusLabel.setText("")
        if userName:
            self.loginLineEdit.setText(userName)

    def exec_(self):
        self.passwordLineEdit.setText('test') # todo: change to ''
        self.loginLineEdit.selectAll()
        self.updateUi()
        return super(LoginDlg, self).exec_()

    def on_loginLineEdit_textEdited(self):
        self.updateUi()

    def on_loginLineEdit_returnPressed(self):
        self.passwordLineEdit.setFocus()

    def on_passwordLineEdit_textEdited(self):
        self.updateUi()

    def on_passwordLineEdit_returnPressed(self):
        self.passwordLineEdit.clearFocus()
        if self.loginPushButton.isEnabled:
            self.attemptLogin()

    def updateUi(self):
        enable = False
        if self.loginLineEdit.text() and self.passwordLineEdit.text():
            enable = True
        self.loginPushButton.setEnabled(enable)

    def on_loginPushButton_clicked(self):
        self.attemptLogin()

    def attemptLogin(self):
        self.statusLabel.setText("Connecting to database...")
        QCoreApplication.instance().processEvents()
        try:
            assert settings.configured
            settings.DATABASES['default']['USER'] = self.loginLineEdit.text()
            settings.DATABASES['default']['PASSWORD'] = "sinJ4juMper#123" #self.passwordLineEdit.text()

            # this import must be done here to avoid django error
            from updatedatabase import updateDatabase
            updateDatabase()
            self.statusLabel.setText("Performing database maintenance...")
            QCoreApplication.instance().processEvents()
        except Exception as e:
            self.statusLabel.setText("Error connecting to database.")
            QCoreApplication.instance().processEvents()
        else:
            self.done(True)

    def on_exitPushButton_clicked(self):
        self.done(False)
