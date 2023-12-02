# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\printlabel.ui'
#
# Created: Fri Sep 26 15:16:08 2014
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

class Ui_printLabelDlg(object):
    def setupUi(self, printLabelDlg):
        printLabelDlg.setObjectName(_fromUtf8("printLabelDlg"))
        printLabelDlg.resize(339, 460)
        self.widget = QtGui.QWidget(printLabelDlg)
        self.widget.setGeometry(QtCore.QRect(11, 11, 310, 432))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.addDentistPushButton = QtGui.QPushButton(self.widget)
        self.addDentistPushButton.setObjectName(_fromUtf8("addDentistPushButton"))
        self.verticalLayout_3.addWidget(self.addDentistPushButton)
        self.addSterilizerPushButton = QtGui.QPushButton(self.widget)
        self.addSterilizerPushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.addSterilizerPushButton.setObjectName(_fromUtf8("addSterilizerPushButton"))
        self.verticalLayout_3.addWidget(self.addSterilizerPushButton)
        self.addByDentistPushButton = QtGui.QPushButton(self.widget)
        self.addByDentistPushButton.setObjectName(_fromUtf8("addByDentistPushButton"))
        self.verticalLayout_3.addWidget(self.addByDentistPushButton)
        self.addOfficePushButton = QtGui.QPushButton(self.widget)
        self.addOfficePushButton.setObjectName(_fromUtf8("addOfficePushButton"))
        self.verticalLayout_3.addWidget(self.addOfficePushButton)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.treeWidget = QtGui.QTreeWidget(self.widget)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout_4.addWidget(self.treeWidget)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.rowSpinBox = QtGui.QSpinBox(self.widget)
        self.rowSpinBox.setMinimum(1)
        self.rowSpinBox.setMaximum(10)
        self.rowSpinBox.setObjectName(_fromUtf8("rowSpinBox"))
        self.verticalLayout_2.addWidget(self.rowSpinBox)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.columnSpinBox = QtGui.QSpinBox(self.widget)
        self.columnSpinBox.setMinimum(1)
        self.columnSpinBox.setMaximum(3)
        self.columnSpinBox.setObjectName(_fromUtf8("columnSpinBox"))
        self.verticalLayout.addWidget(self.columnSpinBox)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.printDentistsPushButton = QtGui.QPushButton(self.widget)
        self.printDentistsPushButton.setObjectName(_fromUtf8("printDentistsPushButton"))
        self.horizontalLayout_2.addWidget(self.printDentistsPushButton)
        self.printSterilizersPushButton = QtGui.QPushButton(self.widget)
        self.printSterilizersPushButton.setObjectName(_fromUtf8("printSterilizersPushButton"))
        self.horizontalLayout_2.addWidget(self.printSterilizersPushButton)
        self.cancelPushButton = QtGui.QPushButton(self.widget)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout_2.addWidget(self.cancelPushButton)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.retranslateUi(printLabelDlg)
        QtCore.QMetaObject.connectSlotsByName(printLabelDlg)

    def retranslateUi(self, printLabelDlg):
        printLabelDlg.setWindowTitle(_translate("printLabelDlg", "Sterilizer Labels", None))
        self.addDentistPushButton.setText(_translate("printLabelDlg", "Add &Dentist", None))
        self.addSterilizerPushButton.setText(_translate("printLabelDlg", "Add &Sterilizer", None))
        self.addByDentistPushButton.setText(_translate("printLabelDlg", "Add Sterilizers &by Dentist", None))
        self.addOfficePushButton.setText(_translate("printLabelDlg", "Add Dental Office (Sterilizers and Dentist)", None))
        self.label.setText(_translate("printLabelDlg", "Start Printing at Label:", None))
        self.label_2.setText(_translate("printLabelDlg", "Row", None))
        self.label_3.setText(_translate("printLabelDlg", "Column", None))
        self.printDentistsPushButton.setText(_translate("printLabelDlg", "Print &Dentists", None))
        self.printSterilizersPushButton.setText(_translate("printLabelDlg", "Print &Sterilizers", None))
        self.cancelPushButton.setText(_translate("printLabelDlg", "&Cancel", None))

