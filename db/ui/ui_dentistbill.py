# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\dentistbill.ui'
#
# Created: Wed Jul 30 16:44:54 2014
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

class Ui_dentistBillDlg(object):
    def setupUi(self, dentistBillDlg):
        dentistBillDlg.setObjectName(_fromUtf8("dentistBillDlg"))
        dentistBillDlg.resize(402, 364)
        self.listWidget = QtGui.QListWidget(dentistBillDlg)
        self.listWidget.setGeometry(QtCore.QRect(51, 128, 256, 192))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.printPushButton = QtGui.QPushButton(dentistBillDlg)
        self.printPushButton.setGeometry(QtCore.QRect(52, 96, 77, 25))
        self.printPushButton.setObjectName(_fromUtf8("printPushButton"))
        self.cancelPushButton = QtGui.QPushButton(dentistBillDlg)
        self.cancelPushButton.setGeometry(QtCore.QRect(135, 96, 77, 25))
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.widget = QtGui.QWidget(dentistBillDlg)
        self.widget.setGeometry(QtCore.QRect(51, 62, 217, 27))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton = QtGui.QPushButton(self.widget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.overdueDaysSpinBox = QtGui.QSpinBox(self.widget)
        self.overdueDaysSpinBox.setMaximum(360)
        self.overdueDaysSpinBox.setSingleStep(30)
        self.overdueDaysSpinBox.setProperty("value", 30)
        self.overdueDaysSpinBox.setObjectName(_fromUtf8("overdueDaysSpinBox"))
        self.horizontalLayout_2.addWidget(self.overdueDaysSpinBox)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)

        self.retranslateUi(dentistBillDlg)
        QtCore.QMetaObject.connectSlotsByName(dentistBillDlg)

    def retranslateUi(self, dentistBillDlg):
        dentistBillDlg.setWindowTitle(_translate("dentistBillDlg", "Dialog", None))
        self.printPushButton.setText(_translate("dentistBillDlg", "&Print", None))
        self.cancelPushButton.setText(_translate("dentistBillDlg", "&Cancel", None))
        self.pushButton.setText(_translate("dentistBillDlg", "Add &Overdue", None))
        self.label.setText(_translate("dentistBillDlg", "by at least", None))
        self.label_2.setText(_translate("dentistBillDlg", "days", None))

