# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\result.ui'
#
# Created: Mon Oct 13 13:30:19 2014
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

class Ui_resultDlg(object):
    def setupUi(self, resultDlg):
        resultDlg.setObjectName(_fromUtf8("resultDlg"))
        resultDlg.resize(226, 166)
        self.widget = QtGui.QWidget(resultDlg)
        self.widget.setGeometry(QtCore.QRect(11, 11, 202, 144))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.defaultPeriodRadioButton = QtGui.QRadioButton(self.widget)
        self.defaultPeriodRadioButton.setObjectName(_fromUtf8("defaultPeriodRadioButton"))
        self.verticalLayout_2.addWidget(self.defaultPeriodRadioButton)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.specificPeriodRadioButton = QtGui.QRadioButton(self.widget)
        self.specificPeriodRadioButton.setObjectName(_fromUtf8("specificPeriodRadioButton"))
        self.verticalLayout.addWidget(self.specificPeriodRadioButton)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.startDateEdit = QtGui.QDateEdit(self.widget)
        self.startDateEdit.setObjectName(_fromUtf8("startDateEdit"))
        self.horizontalLayout_2.addWidget(self.startDateEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.endDateEdit = QtGui.QDateEdit(self.widget)
        self.endDateEdit.setObjectName(_fromUtf8("endDateEdit"))
        self.horizontalLayout.addWidget(self.endDateEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.printPushButton = QtGui.QPushButton(self.widget)
        self.printPushButton.setObjectName(_fromUtf8("printPushButton"))
        self.horizontalLayout_3.addWidget(self.printPushButton)
        self.cancelPushButton = QtGui.QPushButton(self.widget)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout_3.addWidget(self.cancelPushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.retranslateUi(resultDlg)
        QtCore.QMetaObject.connectSlotsByName(resultDlg)

    def retranslateUi(self, resultDlg):
        resultDlg.setWindowTitle(_translate("resultDlg", "Dialog", None))
        self.label.setText(_translate("resultDlg", "Test Results Report for", None))
        self.defaultPeriodRadioButton.setText(_translate("resultDlg", "default time period", None))
        self.specificPeriodRadioButton.setText(_translate("resultDlg", "specified time period", None))
        self.label_3.setText(_translate("resultDlg", "beginning:", None))
        self.label_2.setText(_translate("resultDlg", "and ending:", None))
        self.printPushButton.setText(_translate("resultDlg", "&Print", None))
        self.cancelPushButton.setText(_translate("resultDlg", "E&xit", None))

