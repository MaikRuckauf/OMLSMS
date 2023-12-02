# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\activityreport.ui'
#
# Created: Sun Nov 02 13:52:16 2014
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

class Ui_activityReportDlg(object):
    def setupUi(self, activityReportDlg):
        activityReportDlg.setObjectName(_fromUtf8("activityReportDlg"))
        activityReportDlg.resize(254, 68)
        self.widget = QtGui.QWidget(activityReportDlg)
        self.widget.setGeometry(QtCore.QRect(1, 11, 247, 48))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.viewReportPushButton = QtGui.QPushButton(self.widget)
        self.viewReportPushButton.setObjectName(_fromUtf8("viewReportPushButton"))
        self.horizontalLayout.addWidget(self.viewReportPushButton)
        self.printReportPushButton = QtGui.QPushButton(self.widget)
        self.printReportPushButton.setObjectName(_fromUtf8("printReportPushButton"))
        self.horizontalLayout.addWidget(self.printReportPushButton)
        self.exitPushButton = QtGui.QPushButton(self.widget)
        self.exitPushButton.setObjectName(_fromUtf8("exitPushButton"))
        self.horizontalLayout.addWidget(self.exitPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.statusLabel = QtGui.QLabel(self.widget)
        self.statusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.verticalLayout.addWidget(self.statusLabel)

        self.retranslateUi(activityReportDlg)
        QtCore.QMetaObject.connectSlotsByName(activityReportDlg)

    def retranslateUi(self, activityReportDlg):
        activityReportDlg.setWindowTitle(_translate("activityReportDlg", "Dialog", None))
        self.viewReportPushButton.setText(_translate("activityReportDlg", "&View Report", None))
        self.printReportPushButton.setText(_translate("activityReportDlg", "&Print Report", None))
        self.exitPushButton.setText(_translate("activityReportDlg", "E&xit", None))
        self.statusLabel.setText(_translate("activityReportDlg", "(Status)", None))

