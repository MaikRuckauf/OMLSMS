# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\starttest.ui'
#
# Created: Sun Jul 27 17:31:59 2014
#      by: PyQt4 UI code generator 4.11
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_startTestDlg(object):
    def setupUi(self, startTestDlg):
        startTestDlg.setObjectName(_fromUtf8("startTestDlg"))
        startTestDlg.resize(283, 121)
        self.formLayout = QtGui.QFormLayout(startTestDlg)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(startTestDlg)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.testNumLineEdit = QtGui.QLineEdit(startTestDlg)
        self.testNumLineEdit.setObjectName(_fromUtf8("testNumLineEdit"))
        self.verticalLayout.addWidget(self.testNumLineEdit)
        spacerItem = QtGui.QSpacerItem(18, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.confirmPushButton = QtGui.QPushButton(startTestDlg)
        self.confirmPushButton.setObjectName(_fromUtf8("confirmPushButton"))
        self.horizontalLayout.addWidget(self.confirmPushButton)
        self.cancelPushButton = QtGui.QPushButton(startTestDlg)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout.setLayout(0, QtGui.QFormLayout.LabelRole, self.verticalLayout)

        self.retranslateUi(startTestDlg)
        QtCore.QMetaObject.connectSlotsByName(startTestDlg)

    def retranslateUi(self, startTestDlg):
        startTestDlg.setWindowTitle(_translate("startTestDlg", "Dialog", None))
        self.label.setText(_translate("startTestDlg", "Please Enter Test Identification Number for New Test:", None))
        self.confirmPushButton.setText(_translate("startTestDlg", "Confirm", None))
        self.cancelPushButton.setText(_translate("startTestDlg", "Cancel", None))

