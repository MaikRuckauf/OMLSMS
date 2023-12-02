# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\testnotify.ui'
#
# Created: Sat Aug 16 21:15:20 2014
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

class Ui_testNotifyDlg(object):
    def setupUi(self, testNotifyDlg):
        testNotifyDlg.setObjectName(_fromUtf8("testNotifyDlg"))
        testNotifyDlg.resize(359, 232)
        self.widget = QtGui.QWidget(testNotifyDlg)
        self.widget.setGeometry(QtCore.QRect(10, 20, 336, 199))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.dentalOfficeLineEdit = QtGui.QLineEdit(self.widget)
        self.dentalOfficeLineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.dentalOfficeLineEdit.setObjectName(_fromUtf8("dentalOfficeLineEdit"))
        self.horizontalLayout.addWidget(self.dentalOfficeLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.dentistLineEdit = QtGui.QLineEdit(self.widget)
        self.dentistLineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.dentistLineEdit.setObjectName(_fromUtf8("dentistLineEdit"))
        self.horizontalLayout_2.addWidget(self.dentistLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.contactPersonLineEdit = QtGui.QLineEdit(self.widget)
        self.contactPersonLineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.contactPersonLineEdit.setObjectName(_fromUtf8("contactPersonLineEdit"))
        self.horizontalLayout_3.addWidget(self.contactPersonLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.phoneNumberLineEdit = QtGui.QLineEdit(self.widget)
        self.phoneNumberLineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.phoneNumberLineEdit.setObjectName(_fromUtf8("phoneNumberLineEdit"))
        self.horizontalLayout_4.addWidget(self.phoneNumberLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_5.addWidget(self.label_5)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.faxNumberLineEdit = QtGui.QLineEdit(self.widget)
        self.faxNumberLineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.faxNumberLineEdit.setObjectName(_fromUtf8("faxNumberLineEdit"))
        self.horizontalLayout_5.addWidget(self.faxNumberLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_6 = QtGui.QLabel(self.widget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_6.addWidget(self.label_6)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.emailLineEdit = QtGui.QLineEdit(self.widget)
        self.emailLineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.emailLineEdit.setObjectName(_fromUtf8("emailLineEdit"))
        self.horizontalLayout_6.addWidget(self.emailLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.printNotifiedPushButton = QtGui.QPushButton(self.widget)
        self.printNotifiedPushButton.setObjectName(_fromUtf8("printNotifiedPushButton"))
        self.horizontalLayout_7.addWidget(self.printNotifiedPushButton)
        self.printAttemptedPushButton = QtGui.QPushButton(self.widget)
        self.printAttemptedPushButton.setObjectName(_fromUtf8("printAttemptedPushButton"))
        self.horizontalLayout_7.addWidget(self.printAttemptedPushButton)
        self.exitPushButton = QtGui.QPushButton(self.widget)
        self.exitPushButton.setObjectName(_fromUtf8("exitPushButton"))
        self.horizontalLayout_7.addWidget(self.exitPushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.retranslateUi(testNotifyDlg)
        QtCore.QMetaObject.connectSlotsByName(testNotifyDlg)

    def retranslateUi(self, testNotifyDlg):
        testNotifyDlg.setWindowTitle(_translate("testNotifyDlg", "Contact Dental Office", None))
        self.label.setText(_translate("testNotifyDlg", "Dental Office:", None))
        self.label_2.setText(_translate("testNotifyDlg", "Dentist:", None))
        self.label_3.setText(_translate("testNotifyDlg", "Contact Person:", None))
        self.label_4.setText(_translate("testNotifyDlg", "Phone Number:", None))
        self.label_5.setText(_translate("testNotifyDlg", "FAX Number:", None))
        self.label_6.setText(_translate("testNotifyDlg", "E-mail:", None))
        self.printNotifiedPushButton.setText(_translate("testNotifyDlg", "Print Notified", None))
        self.printAttemptedPushButton.setText(_translate("testNotifyDlg", "Print Contact &Attempted", None))
        self.exitPushButton.setText(_translate("testNotifyDlg", "E&xit", None))

