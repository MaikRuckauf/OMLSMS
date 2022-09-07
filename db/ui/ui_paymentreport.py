# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\paymentreport.ui'
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

class Ui_paymentReportDlg(object):
    def setupUi(self, paymentReportDlg):
        paymentReportDlg.setObjectName(_fromUtf8("paymentReportDlg"))
        paymentReportDlg.resize(264, 77)
        self.widget = QtGui.QWidget(paymentReportDlg)
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
        self.dateEdit = QtGui.QDateEdit(self.widget)
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.horizontalLayout.addWidget(self.dateEdit)
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

        self.retranslateUi(paymentReportDlg)
        QtCore.QMetaObject.connectSlotsByName(paymentReportDlg)

    def retranslateUi(self, paymentReportDlg):
        paymentReportDlg.setWindowTitle(_translate("paymentReportDlg", "Dialog", None))
        self.label.setText(_translate("paymentReportDlg", "Payments made on:", None))
        self.viewReportPushButton.setText(_translate("paymentReportDlg", "&View Report", None))
        self.printReportPushButton.setText(_translate("paymentReportDlg", "&Print Report", None))
        self.exitPushButton.setText(_translate("paymentReportDlg", "E&xit", None))

