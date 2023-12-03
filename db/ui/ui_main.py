# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main.ui'
#
# Created: Sun Aug 24 17:14:10 2014
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

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.resize(580, 45)
        mainWindow.setMinimumSize(QtCore.QSize(580, 45))
        mainWindow.setMaximumSize(QtCore.QSize(580, 45))
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 562, 25))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.dentistsPushButton = QtGui.QPushButton(self.layoutWidget)
        self.dentistsPushButton.setObjectName(_fromUtf8("dentistsPushButton"))
        self.horizontalLayout.addWidget(self.dentistsPushButton)
        self.sterilizersPushButton = QtGui.QPushButton(self.layoutWidget)
        self.sterilizersPushButton.setObjectName(_fromUtf8("sterilizersPushButton"))
        self.horizontalLayout.addWidget(self.sterilizersPushButton)
        self.lotsPushButton = QtGui.QPushButton(self.layoutWidget)
        self.lotsPushButton.setObjectName(_fromUtf8("lotsPushButton"))
        self.horizontalLayout.addWidget(self.lotsPushButton)
        self.renewalsPushButton = QtGui.QPushButton(self.layoutWidget)
        self.renewalsPushButton.setObjectName(_fromUtf8("renewalsPushButton"))
        self.horizontalLayout.addWidget(self.renewalsPushButton)
        self.testsPushButton = QtGui.QPushButton(self.layoutWidget)
        self.testsPushButton.setObjectName(_fromUtf8("testsPushButton"))
        self.horizontalLayout.addWidget(self.testsPushButton)
        self.reportsPushButton = QtGui.QPushButton(self.layoutWidget)
        self.reportsPushButton.setObjectName(_fromUtf8("reportsPushButton"))
        self.horizontalLayout.addWidget(self.reportsPushButton)
        self.userComboBox = QtGui.QComboBox(self.layoutWidget)
        self.userComboBox.setMaximumSize(QtCore.QSize(60, 16777215))
        self.userComboBox.setObjectName(_fromUtf8("userComboBox"))
        self.horizontalLayout.addWidget(self.userComboBox)
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow", None))
        self.dentistsPushButton.setText(_translate("mainWindow", "&Dentists", None))
        self.sterilizersPushButton.setText(_translate("mainWindow", "&Sterilizers", None))
        self.lotsPushButton.setText(_translate("mainWindow", "&Lots", None))
        self.renewalsPushButton.setText(_translate("mainWindow", "&Renewals", None))
        self.testsPushButton.setText(_translate("mainWindow", "&Tests", None))
        self.reportsPushButton.setText(_translate("mainWindow", "Re&ports", None))

