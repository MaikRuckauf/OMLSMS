# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\overduereport.ui'
#
# Created: Sun Sep 28 20:34:03 2014
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

class Ui_overdueReportDlg(object):
    def setupUi(self, overdueReportDlg):
        overdueReportDlg.setObjectName(_fromUtf8("overdueReportDlg"))
        overdueReportDlg.resize(261, 100)
        self.widget = QtGui.QWidget(overdueReportDlg)
        self.widget.setGeometry(QtCore.QRect(11, 11, 247, 81))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.daysOverdueSpinBox = QtGui.QSpinBox(self.widget)
        self.daysOverdueSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.daysOverdueSpinBox.setMinimum(0)
        self.daysOverdueSpinBox.setMaximum(360)
        self.daysOverdueSpinBox.setSingleStep(30)
        self.daysOverdueSpinBox.setProperty("value", 0)
        self.daysOverdueSpinBox.setObjectName(_fromUtf8("daysOverdueSpinBox"))
        self.horizontalLayout.addWidget(self.daysOverdueSpinBox)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.renewalOnlyCheckBox = QtGui.QCheckBox(self.widget)
        self.renewalOnlyCheckBox.setObjectName(_fromUtf8("renewalOnlyCheckBox"))
        self.verticalLayout.addWidget(self.renewalOnlyCheckBox)
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

        self.retranslateUi(overdueReportDlg)
        QtCore.QMetaObject.connectSlotsByName(overdueReportDlg)

    def retranslateUi(self, overdueReportDlg):
        overdueReportDlg.setWindowTitle(_translate("overdueReportDlg", "Dialog", None))
        self.label.setText(_translate("overdueReportDlg", "Billed at least", None))
        self.label_2.setText(_translate("overdueReportDlg", "days ago", None))
        self.renewalOnlyCheckBox.setText(_translate("overdueReportDlg", "Only Accounts needing Renewal", None))
        self.viewReportPushButton.setText(_translate("overdueReportDlg", "&View Report", None))
        self.printReportPushButton.setText(_translate("overdueReportDlg", "&Print Report", None))
        self.exitPushButton.setText(_translate("overdueReportDlg", "E&xit", None))

