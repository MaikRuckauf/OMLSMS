# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\startrenewal.ui'
#
# Created: Thu Nov 20 12:18:23 2014
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

class Ui_startRenewalDlg(object):
    def setupUi(self, startRenewalDlg):
        startRenewalDlg.setObjectName(_fromUtf8("startRenewalDlg"))
        startRenewalDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        startRenewalDlg.resize(377, 489)
        self.layoutWidget = QtGui.QWidget(startRenewalDlg)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 17, 353, 461))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setContentsMargins(-1, 6, -1, 12)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(13, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.numberNeedingRenewalLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.numberNeedingRenewalLineEdit.setEnabled(False)
        self.numberNeedingRenewalLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.numberNeedingRenewalLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numberNeedingRenewalLineEdit.setObjectName(_fromUtf8("numberNeedingRenewalLineEdit"))
        self.horizontalLayout_2.addWidget(self.numberNeedingRenewalLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setContentsMargins(6, -1, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lotComboBox = QtGui.QComboBox(self.layoutWidget)
        self.lotComboBox.setObjectName(_fromUtf8("lotComboBox"))
        self.horizontalLayout.addWidget(self.lotComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtGui.QTableWidget(self.layoutWidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 300))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_7.addWidget(self.label_2)
        self.renewalsSelectedLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.renewalsSelectedLineEdit.setEnabled(True)
        self.renewalsSelectedLineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.renewalsSelectedLineEdit.setObjectName(_fromUtf8("renewalsSelectedLineEdit"))
        self.horizontalLayout_7.addWidget(self.renewalsSelectedLineEdit)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_7.addWidget(self.label_4)
        self.stripsRequiredLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.stripsRequiredLineEdit.setEnabled(True)
        self.stripsRequiredLineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.stripsRequiredLineEdit.setObjectName(_fromUtf8("stripsRequiredLineEdit"))
        self.horizontalLayout_7.addWidget(self.stripsRequiredLineEdit)
        spacerItem3 = QtGui.QSpacerItem(28, 18, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem4 = QtGui.QSpacerItem(28, 18, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.sendPushButton = QtGui.QPushButton(self.layoutWidget)
        self.sendPushButton.setAutoDefault(False)
        self.sendPushButton.setObjectName(_fromUtf8("sendPushButton"))
        self.horizontalLayout_3.addWidget(self.sendPushButton)
        self.cancelPushButton = QtGui.QPushButton(self.layoutWidget)
        self.cancelPushButton.setAutoDefault(False)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout_3.addWidget(self.cancelPushButton)
        spacerItem5 = QtGui.QSpacerItem(28, 18, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.statusLabel = QtGui.QLabel(self.layoutWidget)
        self.statusLabel.setMinimumSize(QtCore.QSize(200, 0))
        self.statusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.horizontalLayout_6.addWidget(self.statusLabel)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.retranslateUi(startRenewalDlg)
        QtCore.QMetaObject.connectSlotsByName(startRenewalDlg)

    def retranslateUi(self, startRenewalDlg):
        startRenewalDlg.setWindowTitle(_translate("startRenewalDlg", "Dialog", None))
        self.label_3.setText(_translate("startRenewalDlg", "Sterilizers needing renewal:", None))
        self.label.setText(_translate("startRenewalDlg", "Renew using Lot:", None))
        self.label_2.setText(_translate("startRenewalDlg", "Total Renewals", None))
        self.label_4.setText(_translate("startRenewalDlg", "Total Strips", None))
        self.sendPushButton.setText(_translate("startRenewalDlg", "&Send", None))
        self.cancelPushButton.setText(_translate("startRenewalDlg", "&Close", None))
        self.statusLabel.setText(_translate("startRenewalDlg", "Status", None))

