# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\report.ui'
#
# Created: Sat Nov 01 15:34:25 2014
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

class Ui_reportDlg(object):
    def setupUi(self, reportDlg):
        reportDlg.setObjectName(_fromUtf8("reportDlg"))
        reportDlg.resize(142, 252)
        self.widget = QtGui.QWidget(reportDlg)
        self.widget.setGeometry(QtCore.QRect(10, 13, 120, 229))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.dailyPaymentReportPushButton = QtGui.QPushButton(self.widget)
        self.dailyPaymentReportPushButton.setObjectName(_fromUtf8("dailyPaymentReportPushButton"))
        self.verticalLayout_3.addWidget(self.dailyPaymentReportPushButton)
        self.testCountPushButton = QtGui.QPushButton(self.widget)
        self.testCountPushButton.setObjectName(_fromUtf8("testCountPushButton"))
        self.verticalLayout_3.addWidget(self.testCountPushButton)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.overdueAccountsPushButton = QtGui.QPushButton(self.widget)
        self.overdueAccountsPushButton.setObjectName(_fromUtf8("overdueAccountsPushButton"))
        self.verticalLayout_2.addWidget(self.overdueAccountsPushButton)
        self.activityReportPushButton = QtGui.QPushButton(self.widget)
        self.activityReportPushButton.setObjectName(_fromUtf8("activityReportPushButton"))
        self.verticalLayout_2.addWidget(self.activityReportPushButton)
        self.anomalyReportPushButton = QtGui.QPushButton(self.widget)
        self.anomalyReportPushButton.setObjectName(_fromUtf8("anomalyReportPushButton"))
        self.verticalLayout_2.addWidget(self.anomalyReportPushButton)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.quarterlyPaymentSummaryPushButton = QtGui.QPushButton(self.widget)
        self.quarterlyPaymentSummaryPushButton.setObjectName(_fromUtf8("quarterlyPaymentSummaryPushButton"))
        self.verticalLayout.addWidget(self.quarterlyPaymentSummaryPushButton)
        self.yearlyCompliancePushButton = QtGui.QPushButton(self.widget)
        self.yearlyCompliancePushButton.setObjectName(_fromUtf8("yearlyCompliancePushButton"))
        self.verticalLayout.addWidget(self.yearlyCompliancePushButton)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.lotRecallPushButton = QtGui.QPushButton(self.widget)
        self.lotRecallPushButton.setObjectName(_fromUtf8("lotRecallPushButton"))
        self.verticalLayout_4.addWidget(self.lotRecallPushButton)

        self.retranslateUi(reportDlg)
        QtCore.QMetaObject.connectSlotsByName(reportDlg)

    def retranslateUi(self, reportDlg):
        reportDlg.setWindowTitle(_translate("reportDlg", "Dialog", None))
        self.dailyPaymentReportPushButton.setText(_translate("reportDlg", "Daily &Payment", None))
        self.testCountPushButton.setText(_translate("reportDlg", "Daily &Test Count", None))
        self.overdueAccountsPushButton.setText(_translate("reportDlg", "Outstanding &Balances", None))
        self.activityReportPushButton.setText(_translate("reportDlg", "Activity Report", None))
        self.anomalyReportPushButton.setText(_translate("reportDlg", "&Anomaly Report", None))
        self.quarterlyPaymentSummaryPushButton.setText(_translate("reportDlg", "Accounts &Summary", None))
        self.yearlyCompliancePushButton.setText(_translate("reportDlg", "Yearly &Compliance", None))
        self.lotRecallPushButton.setText(_translate("reportDlg", "Lot &Recall", None))

