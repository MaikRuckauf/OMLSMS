# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\sendrenewal.ui'
#
# Created: Tue Sep 02 15:07:39 2014
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

class Ui_sendRenewalDlg(object):
    def setupUi(self, sendRenewalDlg):
        sendRenewalDlg.setObjectName(_fromUtf8("sendRenewalDlg"))
        sendRenewalDlg.resize(373, 134)
        self.widget = QtGui.QWidget(sendRenewalDlg)
        self.widget.setGeometry(QtCore.QRect(11, 11, 355, 113))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.renewalIdLineEdit = QtGui.QLineEdit(self.widget)
        self.renewalIdLineEdit.setObjectName(_fromUtf8("renewalIdLineEdit"))
        self.horizontalLayout.addWidget(self.renewalIdLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.numRenewalsLineEdit = QtGui.QLineEdit(self.widget)
        self.numRenewalsLineEdit.setEnabled(False)
        self.numRenewalsLineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.numRenewalsLineEdit.setObjectName(_fromUtf8("numRenewalsLineEdit"))
        self.horizontalLayout_2.addWidget(self.numRenewalsLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.printMailingLabelsPushButton = QtGui.QPushButton(self.widget)
        self.printMailingLabelsPushButton.setObjectName(_fromUtf8("printMailingLabelsPushButton"))
        self.horizontalLayout_3.addWidget(self.printMailingLabelsPushButton)
        self.printReportsPushButton = QtGui.QPushButton(self.widget)
        self.printReportsPushButton.setObjectName(_fromUtf8("printReportsPushButton"))
        self.horizontalLayout_3.addWidget(self.printReportsPushButton)
        self.exitPushButton = QtGui.QPushButton(self.widget)
        self.exitPushButton.setObjectName(_fromUtf8("exitPushButton"))
        self.horizontalLayout_3.addWidget(self.exitPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.statusLabel = QtGui.QLabel(self.widget)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.horizontalLayout_4.addWidget(self.statusLabel)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(sendRenewalDlg)
        QtCore.QMetaObject.connectSlotsByName(sendRenewalDlg)

    def retranslateUi(self, sendRenewalDlg):
        sendRenewalDlg.setWindowTitle(_translate("sendRenewalDlg", "Dialog", None))
        self.label.setText(_translate("sendRenewalDlg", "Enter Renewal ID:", None))
        self.label_2.setText(_translate("sendRenewalDlg", "Current Number of Renewals:", None))
        self.printMailingLabelsPushButton.setText(_translate("sendRenewalDlg", "Print &Mailing Labels", None))
        self.printReportsPushButton.setText(_translate("sendRenewalDlg", "Print &Reports", None))
        self.exitPushButton.setText(_translate("sendRenewalDlg", "E&xit", None))
        self.statusLabel.setText(_translate("sendRenewalDlg", "Status Label", None))

