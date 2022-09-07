# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\yearlycompliance.ui'
#
# Created: Mon Sep 22 13:35:39 2014
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

class Ui_yearlyComplianceDlg(object):
    def setupUi(self, yearlyComplianceDlg):
        yearlyComplianceDlg.setObjectName(_fromUtf8("yearlyComplianceDlg"))
        yearlyComplianceDlg.resize(269, 274)
        self.widget = QtGui.QWidget(yearlyComplianceDlg)
        self.widget.setGeometry(QtCore.QRect(13, 14, 247, 247))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 10)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.beginDateEdit = QtGui.QDateEdit(self.widget)
        self.beginDateEdit.setObjectName(_fromUtf8("beginDateEdit"))
        self.horizontalLayout_3.addWidget(self.beginDateEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.endDateEdit = QtGui.QDateEdit(self.widget)
        self.endDateEdit.setObjectName(_fromUtf8("endDateEdit"))
        self.horizontalLayout.addWidget(self.endDateEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 10, -1, 10)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.label_6 = QtGui.QLabel(self.widget)
        self.label_6.setMinimumSize(QtCore.QSize(30, 0))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_5.addWidget(self.label_6)
        self.firstDentistSpinBox = QtGui.QSpinBox(self.widget)
        self.firstDentistSpinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.firstDentistSpinBox.setMaximum(99999)
        self.firstDentistSpinBox.setSingleStep(100)
        self.firstDentistSpinBox.setObjectName(_fromUtf8("firstDentistSpinBox"))
        self.horizontalLayout_5.addWidget(self.firstDentistSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setMinimumSize(QtCore.QSize(30, 0))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_4.addWidget(self.label_5)
        self.lastDentistSpinBox = QtGui.QSpinBox(self.widget)
        self.lastDentistSpinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.lastDentistSpinBox.setMaximum(99999)
        self.lastDentistSpinBox.setSingleStep(100)
        self.lastDentistSpinBox.setObjectName(_fromUtf8("lastDentistSpinBox"))
        self.horizontalLayout_4.addWidget(self.lastDentistSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.printLettersPushButton = QtGui.QPushButton(self.widget)
        self.printLettersPushButton.setObjectName(_fromUtf8("printLettersPushButton"))
        self.horizontalLayout_2.addWidget(self.printLettersPushButton)
        self.printLabelsPushButton = QtGui.QPushButton(self.widget)
        self.printLabelsPushButton.setObjectName(_fromUtf8("printLabelsPushButton"))
        self.horizontalLayout_2.addWidget(self.printLabelsPushButton)
        self.exitPushButton = QtGui.QPushButton(self.widget)
        self.exitPushButton.setObjectName(_fromUtf8("exitPushButton"))
        self.horizontalLayout_2.addWidget(self.exitPushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.statusLabel = QtGui.QLabel(self.widget)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.horizontalLayout_6.addWidget(self.statusLabel)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.retranslateUi(yearlyComplianceDlg)
        QtCore.QMetaObject.connectSlotsByName(yearlyComplianceDlg)

    def retranslateUi(self, yearlyComplianceDlg):
        yearlyComplianceDlg.setWindowTitle(_translate("yearlyComplianceDlg", "Dialog", None))
        self.label.setText(_translate("yearlyComplianceDlg", "Yearly compliance for period", None))
        self.label_2.setText(_translate("yearlyComplianceDlg", "beginning:", None))
        self.label_3.setText(_translate("yearlyComplianceDlg", "and ending:", None))
        self.label_4.setText(_translate("yearlyComplianceDlg", "for dentistal office records numbered", None))
        self.label_6.setText(_translate("yearlyComplianceDlg", "from:", None))
        self.label_5.setText(_translate("yearlyComplianceDlg", "to:", None))
        self.printLettersPushButton.setText(_translate("yearlyComplianceDlg", "&Print Letters", None))
        self.printLabelsPushButton.setText(_translate("yearlyComplianceDlg", "Print &Labels", None))
        self.exitPushButton.setText(_translate("yearlyComplianceDlg", "E&xit", None))
        self.statusLabel.setText(_translate("yearlyComplianceDlg", "(Status)", None))

