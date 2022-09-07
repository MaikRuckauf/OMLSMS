# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\lotrecall.ui'
#
# Created: Tue Aug 19 20:17:10 2014
#      by: PyQt4 UI code generator 4.11
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_lotRecallDlg(object):
    def setupUi(self, lotRecallDlg):
        lotRecallDlg.setObjectName(_fromUtf8("lotRecallDlg"))
        lotRecallDlg.resize(266, 79)
        self.widget = QtGui.QWidget(lotRecallDlg)
        self.widget.setGeometry(QtCore.QRect(10, 10, 247, 57))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lotComboBox = QtGui.QComboBox(self.widget)
        self.lotComboBox.setObjectName(_fromUtf8("lotComboBox"))
        self.horizontalLayout.addWidget(self.lotComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.viewReportPushButton = QtGui.QPushButton(self.widget)
        self.viewReportPushButton.setObjectName(_fromUtf8("viewReportPushButton"))
        self.horizontalLayout_2.addWidget(self.viewReportPushButton)
        self.printReportPushButton = QtGui.QPushButton(self.widget)
        self.printReportPushButton.setObjectName(_fromUtf8("printReportPushButton"))
        self.horizontalLayout_2.addWidget(self.printReportPushButton)
        self.exitPushButton = QtGui.QPushButton(self.widget)
        self.exitPushButton.setObjectName(_fromUtf8("exitPushButton"))
        self.horizontalLayout_2.addWidget(self.exitPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(lotRecallDlg)
        QtCore.QMetaObject.connectSlotsByName(lotRecallDlg)

    def retranslateUi(self, lotRecallDlg):
        lotRecallDlg.setWindowTitle(_translate("lotRecallDlg", "Dialog", None))
        self.label.setText(_translate("lotRecallDlg", "List of renewals for lot:", None))
        self.viewReportPushButton.setText(_translate("lotRecallDlg", "&View Report", None))
        self.printReportPushButton.setText(_translate("lotRecallDlg", "&Print Report", None))
        self.exitPushButton.setText(_translate("lotRecallDlg", "E&xit", None))

