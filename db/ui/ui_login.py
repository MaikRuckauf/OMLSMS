# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\login.ui'
#
# Created: Sun Aug 24 16:58:49 2014
#      by: PyQt4 UI code generator 4.11
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_loginDlg(object):
    def setupUi(self, loginDlg):
        loginDlg.setObjectName(_fromUtf8("loginDlg"))
        loginDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        loginDlg.setEnabled(True)
        loginDlg.resize(356, 235)
        loginDlg.setMinimumSize(QtCore.QSize(356, 235))
        loginDlg.setMaximumSize(QtCore.QSize(356, 235))
        self.verticalLayout = QVBoxLayout(loginDlg)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QLabel(loginDlg)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.line_2 = QFrame(loginDlg)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.label_4 = QLabel(loginDlg)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.line_4 = QFrame(loginDlg)
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.verticalLayout.addWidget(self.line_4)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QLabel(loginDlg)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.loginLineEdit = QLineEdit(loginDlg)
        self.loginLineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.loginLineEdit.setMaxLength(12)
        self.loginLineEdit.setObjectName(_fromUtf8("loginLineEdit"))
        self.gridLayout.addWidget(self.loginLineEdit, 0, 1, 1, 1)
        self.label_2 = QLabel(loginDlg)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.passwordLineEdit = QLineEdit(loginDlg)
        self.passwordLineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.passwordLineEdit.setMaxLength(12)
        self.passwordLineEdit.setObjectName(_fromUtf8("passwordLineEdit"))
        self.gridLayout.addWidget(self.passwordLineEdit, 1, 1, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout)
        self.line = QFrame(loginDlg)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout_3.addWidget(self.line)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.loginPushButton = QPushButton(loginDlg)
        self.loginPushButton.setObjectName(_fromUtf8("loginPushButton"))
        self.horizontalLayout.addWidget(self.loginPushButton)
        self.exitPushButton = QPushButton(loginDlg)
        self.exitPushButton.setObjectName(_fromUtf8("exitPushButton"))
        self.horizontalLayout.addWidget(self.exitPushButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line_3 = QFrame(loginDlg)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout.addWidget(self.line_3)
        self.statusLabel = QLabel(loginDlg)
        self.statusLabel.setEnabled(True)
        self.statusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.verticalLayout.addWidget(self.statusLabel)

        self.retranslateUi(loginDlg)
        QtCore.QMetaObject.connectSlotsByName(loginDlg)

    def retranslateUi(self, loginDlg):
        loginDlg.setWindowTitle(_translate("loginDlg", "Dialog", None))
        self.label_3.setText(_translate("loginDlg", "Oral Mircobiology Lab Database", None))
        self.label_4.setText(_translate("loginDlg", "Please Enter Login", None))
        self.label.setText(_translate("loginDlg", "Login", None))
        self.label_2.setText(_translate("loginDlg", "Password", None))
        self.loginPushButton.setText(_translate("loginDlg", "&Login", None))
        self.exitPushButton.setText(_translate("loginDlg", "E&xit", None))
        self.statusLabel.setText(_translate("loginDlg", "(statusLabel)", None))

