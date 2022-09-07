import sys, datetime, locale

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

import ui
from constants import *
from formviewdlg import MainDlg

sys.path.append(OMLWEB_PATH)
from omlweb.models import Lot, Renewal, Sterilizer, Dentist, Test
from django.db.models import F
import djprint
from printlabeldlg import PrintLabelDlg
from finddlg import FindDlg


# also used by SendRenewal
def getDentistNames(itemList, isRenewalList=True):
    try:
        dentist_lookup = {}
        dentists = Dentist.objects.all()
        for dentist in dentists:
            dentist_lookup[dentist.id] = dentist
    except:
        return None

    list = []
    for item in itemList:
        try:
            if isRenewalList:
                dentist = dentist_lookup[RenewalToDentistID(item.id)]
            else:
                dentist = dentist_lookup[SterilizerToDentistID(item.id)]
            if dentist.practice_name:
                list.append(dentist.practice_name)
            else:
                list.append("%s, %s" % (dentist.lname, dentist.fname))
        except:
            list.append("(Error retrieving dentist)")
    return list

    
class ReportDlg(MainDlg, ui.Ui_reportDlg):

    def __init__(self, parent=None):
        super(ReportDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("OMLSMS Reports")
        
        self.editing = False
        self.dlg = None

    def dlgPos(self, pushButton):
        if pushButton:
            p = QPoint(self.rect().right(), pushButton.pos().y())
        else:
            p = QPoint(self.rect().right(), self.rect().top())
        return self.pos() + p + QPoint(20, 30)
    
    def hide(self):
        if self.dlg:
            self.dlg.close()
        super(ReportDlg, self).hide()
        
    def show(self, bookmark):
        super(ReportDlg, self).show()

    @pyqtSignature("")
    def on_testCountPushButton_clicked(self):
        if self.dlg:
            self.dlg.close()
        self.dlg = TestCountDlg(self.dlgPos(self.testCountPushButton), self)
        self.dlg.show()

    @pyqtSignature("")
    def on_activityReportPushButton_clicked(self):
        if self.dlg:
            self.dlg.close()
        self.dlg = ActivityReportDlg(self.dlgPos(self.activityReportPushButton), self)
        self.dlg.show()
        
    @pyqtSignature("")
    def on_anomalyReportPushButton_clicked(self):
        if self.dlg:
            self.dlg.close()
        self.dlg = AnomalyReportDlg(self.dlgPos(self.anomalyReportPushButton), self)
        self.dlg.show()
    
    @pyqtSignature("")
    def on_overdueAccountsPushButton_clicked(self):
        if self.dlg:
            self.dlg.close()
        self.dlg = OverdueReportDlg(self.dlgPos(self.overdueAccountsPushButton), self)
        self.dlg.show()

    @pyqtSignature("")
    def on_dailyPaymentReportPushButton_clicked(self):
        if self.dlg:
            self.dlg.close()
        self.dlg = PaymentReportDlg(self.dlgPos(self.dailyPaymentReportPushButton), self)
        self.dlg.show()

    @pyqtSignature("")
    def on_quarterlyPaymentSummaryPushButton_clicked(self):
        if self.dlg:
            self.dlg.close()
        self.dlg = PaymentSummaryDlg(self.dlgPos(None), self)
        self.dlg.show()

    @pyqtSignature("")
    def on_yearlyCompliancePushButton_clicked(self):
        if self.dlg:
            self.dlg.close()
        self.dlg = YearlyComplianceDlg(self.dlgPos(self.yearlyCompliancePushButton), self)
        self.dlg.show()

    @pyqtSignature("")
    def on_lotRecallPushButton_clicked(self):
        if self.dlg:
            self.dlg.close()
        self.dlg = LotRecallDlg(self.dlgPos(self.lotRecallPushButton), self)
        self.dlg.show()

class TestCountDlg(QDialog, ui.Ui_testCountDlg):
    def __init__(self, pos, parent=None):
        super(TestCountDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Daily Test Counts")
        self.move(pos)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(datetime.date.today() - datetime.timedelta(days=DAYS_FOR_TEST))

        start = datetime.date.today() - datetime.timedelta(MAX_DAYS_FOR_TEST_ENTRY)
        stop = datetime.date.today() - datetime.timedelta(DAYS_FOR_TEST + 1)
        self.needResults = Test.objects.filter(start_date__range=(start, stop)).filter(result_date__isnull=True)
        self.setButtonCount(self.overduePushButton, len(self.needResults))

    def setButtonCount(self, button, count):
        button.setText(str(count))
        button.setEnabled(count)

    @pyqtSignature("QDate")
    def on_dateEdit_dateChanged(self, q_date):
        date = q_date.toPyDate()
        count = Test.objects.filter(start_date=date).count()
        self.setButtonCount(self.inPushButton, count)
        count = Test.objects.filter(result_date=date).count()
        self.setButtonCount(self.outPushButton, count)
        count = Test.objects.filter(result_date=date).filter(result='+').count()
        self.setButtonCount(self.positivesPushButton, count)
        count = Test.objects.filter(start_date=date).filter(result_date__isnull=False).count()
        self.setButtonCount(self.resultsPushButton, count)
        count = Test.objects.filter(start_date=date).filter(result_date__isnull=True).count()
        self.setButtonCount(self.noResultsPushButton, count)

    @pyqtSignature("")
    def on_prevPushButton_clicked(self):
        date = self.dateEdit.date().toPyDate() - datetime.timedelta(days=1)
        self.dateEdit.setDate(date)

    @pyqtSignature("")
    def on_nextPushButton_clicked(self):
        date = self.dateEdit.date().toPyDate() + datetime.timedelta(days=1)
        self.dateEdit.setDate(date)
        
    @pyqtSignature("")
    def on_todayPushButton_clicked(self):
        self.dateEdit.setDate(datetime.date.today())
        
    @pyqtSignature("")
    def on_inPushButton_clicked(self):
        date = self.dateEdit.date().toPyDate()
        title = "Tests logged in on %s" % RecordDateToText(date)
        tests = Test.objects.filter(start_date=date)
        self.parent().viewText(djprint.testCountReport(title, tests))

    @pyqtSignature("")
    def on_outPushButton_clicked(self):
        date = self.dateEdit.date().toPyDate()
        title = "Tests logged out on %s" % RecordDateToText(date)
        tests = Test.objects.filter(result_date=date)
        self.parent().viewText(djprint.testCountReport(title, tests))

    @pyqtSignature("")
    def on_positivesPushButton_clicked(self):
        date = self.dateEdit.date().toPyDate()
        title = "Positives logged out on %s" % RecordDateToText(date)
        tests = Test.objects.filter(result_date=date).filter(result='+')
        self.parent().viewText(djprint.testCountReport(title, tests))

    @pyqtSignature("")
    def on_resultsPushButton_clicked(self):
        date = self.dateEdit.date().toPyDate()
        title = "Tests logged in on %s that have results" % RecordDateToText(date)
        tests = Test.objects.filter(start_date=date).filter(result_date__isnull=False)
        self.parent().viewText(djprint.testCountReport(title, tests))

    @pyqtSignature("")
    def on_noResultsPushButton_clicked(self):
        date = self.dateEdit.date().toPyDate()
        title = "Tests logged in on %s that do not have results" % RecordDateToText(date)
        tests = Test.objects.filter(start_date=date).filter(result_date__isnull=True)
        self.parent().viewText(djprint.testCountReport(title, tests))

    @pyqtSignature("")
    def on_overduePushButton_clicked(self):
        tests = self.needResults
        title = "Tests that require results at this time"
        self.parent().viewText(djprint.testCountReport(title, tests))

    @pyqtSignature("")
    def on_closePushButton_clicked(self):
        self.close()

class ActivityReportDlg(QDialog, ui.Ui_activityReportDlg):
    def __init__(self, pos, parent=None):
        super(ActivityReportDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Activity Report")
        self.move(pos)
        self.printReportPushButton.setDisabled(True)
        self.statusLabel.setText("")

    def getReport(self):
        # report sterilizers that have missed more than 2 weeks in a row
        today = datetime.date.today()
        first_of_week = today - datetime.timedelta(days = today.weekday())
        stop_date = first_of_week - datetime.timedelta(days = 1)
        start_date = first_of_week - datetime.timedelta(days = 7 * 8)
        tests = Test.objects.filter(sample_date__range=(start_date, stop_date))
        weeks = [(start_date + datetime.timedelta(days = 7 * x), 
                  start_date + datetime.timedelta(days = (7 * x) + 6))
                 for x in range(0,8)]
        test_record = [{} for x in range(0,8)]
        for test in tests:
            for i, dates in enumerate(weeks):
                if (test.sample_date >= dates[0] and test.sample_date <= dates[1]):
                    test_record[i][RenewalToSterilizerID(test.renewal_id)] = True
        sterilizers = Sterilizer.objects.filter(inactive_date__isnull=True)
        sterilizers = sterilizers.filter(dentist__inactive_date__isnull=True)
        reportList = []
        activity = {}
        for sterilizer in sterilizers:
            count = 0
            week_flagged = None
            last_week = -1
            act = []
            for i, dict in enumerate(test_record):
                if sterilizer.id in dict or sterilizer.enroll_date > weeks[i][0]:
                    count = 0
                    last_week = i
                    if sterilizer.id in dict:
                        act.append('x')
                    else:
                        act.append(' ')
                else:
                    count += 1
                    act.append('-')
                    if count > 2:
                        week_flagged = i
            if week_flagged:
                reportList.append((-week_flagged, last_week, sterilizer))
            activity[sterilizer.id] = act
        reportList.sort()
        list = [x[2] for x in reportList] # accounts needing action tend to be on top
        records = [activity[x.id] for x in list]
        names = getDentistNames(list, False)
        return (djprint.inactivityReport(list, names, weeks, records))

    @pyqtSignature("")
    def on_viewReportPushButton_clicked(self):
        self.statusLabel.setText("Working...")
        QCoreApplication.instance().processEvents()
        self.parent().viewText(self.getReport())
        self.statusLabel.setText("")
        QCoreApplication.instance().processEvents()

    @pyqtSignature("")
    def on_printReportPushButton_clicked(self):
        self.parent().printText(self.getReport())

    @pyqtSignature("")
    def on_exitPushButton_clicked(self):
        self.close()


class AnomalyReportDlg(QDialog, ui.Ui_anomalyReportDlg):
    def __init__(self, pos, parent=None):
        super(AnomalyReportDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Anomaly Report")
        self.move(pos)
        self.printReportPushButton.setDisabled(True)
        self.statusLabel.setText("")

    def excludeUnpaid(self, sterilizers):
        dentist_ids = [SterilizerToDentistID(sterilizer.id) for sterilizer in sterilizers]

        #recent unpaid renewals for those dentists
        date = datetime.date.today() - datetime.timedelta(days=MAX_DAYS_FOR_COLLECTIONS)
        renewals = Renewal.objects.filter(sterilizer__dentist__id__in=dentist_ids)
        renewals = renewals.filter(renewal_date__gte=date)
        renewals = renewals.filter(inactive_date__isnull=True)
        renewals = renewals.exclude(payment_amount__gte=F('renewal_fee')+F('late_fee'))

        # exclude sterilizers for unpaid accounts
        exclude = {}
        date = datetime.date.today() - datetime.timedelta(days=DAYS_UNTIL_OVERDUE)
        for renewal in renewals:
            if renewal.renewal_date <= date:
                exclude[RenewalToDentistID(renewal.id)] = True
        return [sterilizer for sterilizer in sterilizers if SterilizerToDentistID(sterilizer.id) not in exclude]
        
    def getActivateCandidates(self):
        #all supsended but active sterilizers
        sterilizers = Sterilizer.objects.filter(inactive_date__isnull=True)
        sterilizers = sterilizers.filter(dentist__inactive_date__isnull=True)
        sterilizers = sterilizers.filter(suspend=True)
        
        # returns sterilizers that are suspended but are paid
        return self.excludeUnpaid(sterilizers)

    def getRenewCandidates(self):
        #all active sterilizers not marked for renewal
        sterilizers = Sterilizer.objects.filter(inactive_date__isnull=True)
        sterilizers = sterilizers.filter(dentist__inactive_date__isnull=True)
        sterilizers = sterilizers.filter(renew=False)

        # exclude those not paid in full
        sterilizers = self.excludeUnpaid(sterilizers)
        
        sterilizer_ids = [sterilizer.id for sterilizer in sterilizers]
        renewals = Renewal.objects.filter(sterilizer__id__in=sterilizer_ids)
        renewals = renewals.filter(inactive_date__isnull=True)
        latest_renewal = {}
        for renewal in renewals:
            sterilizer_id = RenewalToSterilizerID(renewal.id)
            if not (sterilizer_id in latest_renewal) or latest_renewal[sterilizer_id].id < renewal.id:
                latest_renewal[sterilizer_id] = renewal
        latest_renewals = [renewal for key, renewal in latest_renewal.iteritems()]
        tests = Test.objects.filter(renewal_id__in=latest_renewals)
        latest_test = {}
        for renewal in latest_renewals:
            latest_test[renewal.id] = 0
        for test in tests:
            latest_test[test.renewal_id] = max(latest_test[test.renewal_id], test.test_num)
        dict = {}
        for sterilizer in sterilizers:
            dict[sterilizer.id] = sterilizer
        candidates = []
        for renewal in latest_renewals:
            if latest_test[renewal.id] >= dict[RenewalToSterilizerID(renewal.id)].renew_test:
                candidates.append(dict[RenewalToSterilizerID(renewal.id)])
        return candidates

    def getReport(self):
        activateCandidates = self.getActivateCandidates()
        a_names = getDentistNames(activateCandidates, False)
        renewCandidates = self.getRenewCandidates()
        r_names = getDentistNames(renewCandidates, False)
        return (djprint.getAnomalyReport(activateCandidates, a_names, renewCandidates, r_names))
        
    @pyqtSignature("")
    def on_viewReportPushButton_clicked(self):
        self.statusLabel.setText("Working...")
        QCoreApplication.instance().processEvents()
        self.parent().viewText(self.getReport())
        self.statusLabel.setText("")
        QCoreApplication.instance().processEvents()

    @pyqtSignature("")
    def on_printReportPushButton_clicked(self):
        self.parent().printText(self.getReport())

    @pyqtSignature("")
    def on_exitPushButton_clicked(self):
        self.close()


class OverdueReportDlg(QDialog, ui.Ui_overdueReportDlg):
    
    def __init__(self, pos, parent=None):
        super(OverdueReportDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Outstanding Balances")
        self.daysOverdueSpinBox.setValue(90)
        self.renewalOnlyCheckBox.setChecked(True)
        self.move(pos)
        self.printReportPushButton.setDisabled(True)
        
    def getOverdueAccounts(self):
        days = datetime.timedelta(days = self.daysOverdueSpinBox.value())
        latest_date = datetime.date.today() - days
        earliest_date = datetime.date.today() - datetime.timedelta(days = MAX_DAYS_FOR_COLLECTIONS)
        
        list = Renewal.objects.exclude(payment_amount__gte=F('renewal_fee')+F('late_fee'))
        list = list.exclude(renewal_fee=0)
        list = list.filter(renewal_date__lt=latest_date)
        list = list.filter(renewal_date__gt=earliest_date)
        list = list.filter(inactive_date__isnull=True)
        list = list.filter(sterilizer__inactive_date__isnull=True)
        list = list.filter(sterilizer__dentist__inactive_date__isnull=True)
        list = list.order_by("renewal_date")
        return list

    def getAccountsToRenew(self):
        # code duplicated in sendrenewal
        sterilizers = Sterilizer.objects.filter(renew=True)
        sterilizers = sterilizers.filter(inactive_date__isnull=True)
        sterilizers = sterilizers.filter(suspend=False)
        sterilizers = sterilizers.filter(dentist__inactive_date__isnull=True)
        renewals = Renewal.objects.filter(sterilizer__in=sterilizers)
        latest_renewal = {}
        for renewal in renewals:
            sterilizer_id = RenewalToSterilizerID(renewal.id)
            if not (sterilizer_id in latest_renewal) or latest_renewal[sterilizer_id].id < renewal.id:
                latest_renewal[sterilizer_id] = renewal
        latest_renewals = [renewal for key, renewal in latest_renewal.iteritems()]
        return latest_renewals

    def mergeMatches(self, overdue, renewals):
        mergeList = []
        d = {}
        f = {}
        for renewal in renewals:
            dentist_id = RenewalToDentistID(renewal.id)
            if dentist_id not in d:
                d[dentist_id] = [renewal]
            else:
                d[dentist_id].append(renewal)
        for renewal in overdue:
            dentist_id = RenewalToDentistID(renewal.id)
            if dentist_id in f and renewal not in f[dentist_id]:
                f[dentist_id].append(renewal)
            elif dentist_id in d:
                f[dentist_id] = d[dentist_id]
                if renewal not in f[dentist_id]:
                    f[dentist_id].append(renewal)
        for key, list in sorted(f.iteritems()):
            mergeList.append(None) # indicates a blank line
            for renewal in list:
                mergeList.append(renewal)
        if len(mergeList):
            mergeList.append(None) # indicates a blank line
        return mergeList

    def getReport(self):
        overdueList = self.getOverdueAccounts()
        if self.renewalOnlyCheckBox.isChecked():
            tempList = self.getAccountsToRenew()
            renewalList = self.mergeMatches(overdueList, tempList)
        else:
            renewalList = overdueList
        dentistNameList = getDentistNames(renewalList)
        return(djprint.printOverdueAccountList(renewalList, dentistNameList))
        
    @pyqtSignature("")
    def on_viewReportPushButton_clicked(self):
        self.parent().viewText(self.getReport())

    @pyqtSignature("")
    def on_printReportPushButton_clicked(self):
        self.parent().printText(self.getReport())

    @pyqtSignature("")
    def on_exitPushButton_clicked(self):
        self.close()


class PaymentReportDlg(QDialog, ui.Ui_paymentReportDlg):
    
    def __init__(self, pos, parent=None):
        super(PaymentReportDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Payment Report")
        self.move(pos)

        self.dateEdit.setDate(datetime.date.today())
        self.dateEdit.setCalendarPopup(True)

    def getPayments(self, date):
        list = Renewal.objects.filter(payment_date=date)
        return list

    def getReport(self):
        renewalList = self.getPayments(self.dateEdit.date().toPyDate)
        renewalList = renewalList.order_by("payment_amount")
        dentistNameList = getDentistNames(renewalList)
        return(djprint.printDailyPaymentReport(renewalList, dentistNameList))

    @pyqtSignature("")
    def on_viewReportPushButton_clicked(self):
        self.parent().viewText(self.getReport())

    @pyqtSignature("")
    def on_printReportPushButton_clicked(self):
        self.parent().printText(self.getReport())

    @pyqtSignature("")
    def on_exitPushButton_clicked(self):
        self.close()


class PaymentSummaryDlg(QDialog, ui.Ui_paymentSummaryDlg):
    
    def __init__(self, pos, parent=None):
        super(PaymentSummaryDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Accounts Summary")
        self.move(pos)

        self.selectMethodRadioButtons = [self.yearRadioButton, self.monthRadioButton,
        self.freeformRadioButton]
        
        self.yearSelectWidgets = [self.yearLineEdit, self.prevYearPushButton,
        self.nextYearPushButton]
        
        self.monthSelectWidgets = [self.monthLineEdit, self.prevMonthPushButton,
        self.nextMonthPushButton]
        
        self.freeformSelectWidgets = [self.beginDateEdit, self.endDateEdit]
        
        self.summaryWidgets = [self.renewalFeesPushButton, self.renewalFeePaymentsPushButton,
        self.lateFeesPushButton, self.lateFeePaymentsPushButton, self.unassignedPaymentsPushButton]
        
        self.currencyWidgets = [self.renewalFeesLabel, self.renewalFeePaymentsLabel,
        self.lateFeesLabel, self.lateFeePaymentsLabel, self.unassignedPaymentsLabel,
        self.balanceLabel, self.paidNoChargeLabel,
        self.paidLabel1, self.paidLabel2, self.paidLabel3, self.paidLabel4, self.paidLabel5,
        self.unpaidLabel1, self.unpaidLabel2, self.unpaidLabel3, self.unpaidLabel4,
        self.unpaidLabel5, self.paymentTotalLabel, self.outstandingBalanceTotalLabel]
        
        self.countWidgets = [self.testsCompletedPushButton, self.renewalsIssuedPushButton,
        self.partialPaymentsPushButton, self.paidNoChargePushButton,
        self.paidPushButton1, self.paidPushButton2, self.paidPushButton3,
        self.paidPushButton4, self.paidPushButton5, self.unpaidPushButton1,
        self.unpaidPushButton2, self.unpaidPushButton3, self.unpaidPushButton4,
        self.unpaidPushButton5, self.totalPaidPushButton, self.totalUnpaidPushButton]
        
        self.paidLabels = [self.paidLabel1, self.paidLabel2, self.paidLabel3, self.paidLabel4, self.paidLabel5]
        
        self.unpaidLabels = [self.unpaidLabel1, self.unpaidLabel2, self.unpaidLabel3, self.unpaidLabel4,
        self.unpaidLabel5]
        
        self.paidButtons = [self.paidPushButton1, self.paidPushButton2, self.paidPushButton3,
        self.paidPushButton4, self.paidPushButton5]
        
        self.unpaidButtons = [self.unpaidPushButton1, self.unpaidPushButton2, 
        self.unpaidPushButton3, self.unpaidPushButton4, self.unpaidPushButton5]

        self.data = None
        self.blankForm()
        self.beginDateEdit.setCalendarPopup(True)
        self.endDateEdit.setCalendarPopup(True)
        today = datetime.date.today()
        self.yearLineEdit.setText(str(today.year))
        self.monthLineEdit.setText(str(today.month))
        self.monthRadioButton.setChecked(True)

    def updateDates(self):
        month = int(self.monthLineEdit.text())
        year = int(self.yearLineEdit.text())
        if self.monthRadioButton.isChecked():
            month += 1
            if month == 13:
                month = 1
                year += 1
            first = datetime.date(year, month, 1)
            end = first - datetime.timedelta(days = 1)
            begin = datetime.date(end.year, end.month, 1)
            self.endDateEdit.setDate(end)
            self.beginDateEdit.setDate(begin)
        elif self.yearRadioButton.isChecked():
            year += 1
            first = datetime.date(year, 1, 1)
            end = first - datetime.timedelta(days = 1)
            begin = datetime.date(end.year, 1, 1)
            self.endDateEdit.setDate(end)
            self.beginDateEdit.setDate(begin)
        self.data = None
        self.blankForm()
        
    def blankForm(self):
        for widget in self.summaryWidgets:
            widget.setDisabled(True)
        
        for widget in self.currencyWidgets:
            widget.setText("$0.00")
            widget.setDisabled(True)
        
        for widget in self.countWidgets:
            widget.setText("0")
            widget.setDisabled(True)

    @pyqtSignature("")
    def on_prevMonthPushButton_clicked(self):
        month = int(self.monthLineEdit.text())
        year = int(self.yearLineEdit.text())
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        self.monthLineEdit.setText(str(month))
        self.yearLineEdit.setText(str(year))

    @pyqtSignature("")
    def on_nextMonthPushButton_clicked(self):
        month = int(self.monthLineEdit.text())
        year = int(self.yearLineEdit.text())
        month += 1
        if month == 13:
            month = 1
            year += 1
        self.monthLineEdit.setText(str(month))
        self.yearLineEdit.setText(str(year))

    @pyqtSignature("")
    def on_prevYearPushButton_clicked(self):
        year = int(self.yearLineEdit.text())
        year -= 1
        self.yearLineEdit.setText(str(year))

    @pyqtSignature("")
    def on_nextYearPushButton_clicked(self):
        year = int(self.yearLineEdit.text())
        year += 1
        self.yearLineEdit.setText(str(year))

    @pyqtSignature("bool")
    def on_yearRadioButton_toggled(self, checked):
        if checked:
            self.disablePeriodSelection()
            for widget in self.yearSelectWidgets:
                widget.setEnabled(True)
        self.updateDates()
    
    @pyqtSignature("bool")
    def on_monthRadioButton_toggled(self, checked):
        if checked:
            self.disablePeriodSelection()
            for widget in self.yearSelectWidgets:
                widget.setEnabled(True)
            for widget in self.monthSelectWidgets:
                widget.setEnabled(True)
        self.updateDates()
    
    @pyqtSignature("bool")
    def on_freeformRadioButton_toggled(self, checked):
        if checked:
            self.disablePeriodSelection()
            for widget in self.freeformSelectWidgets:
                widget.setEnabled(True)

    @pyqtSignature("const QString&")
    def on_yearLineEdit_textChanged(self):
        if self.yearRadioButton.isChecked() or self.monthRadioButton.isChecked():
            self.updateDates()

    @pyqtSignature("const QString&")
    def on_monthLineEdit_textChanged(self):
        if self.monthRadioButton.isChecked():
            self.updateDates()

    def disablePeriodSelection(self):
        for widget in self.yearSelectWidgets + self.monthSelectWidgets + self.freeformSelectWidgets:
            widget.setDisabled(True)

    def countTests(self, startDate, stopDate):
        tests = Test.objects.filter(start_date__range=(startDate, stopDate))
        return tests.count()

    def getRenewals(self, startDate, stopDate):
        renewals = Renewal.objects.filter(renewal_date__range=(startDate, stopDate))
        return renewals

    def getData(self):
        start = self.beginDateEdit.date().toPyDate()
        stop = self.endDateEdit.date().toPyDate()
        renewals = self.getRenewals(start, stop)
        
        intervals = [30,60,90,120]
        last_interval = len(intervals)
        total_charged = 0
        total_received = 0
        total_late_fees = 0
        total_late_fees_received = 0
        total_pending = 0
        total_balance = 0
        total_uncharged = 0
        partial_payments = 0
        paid = [0,0,0,0,0]
        unpaid = [0,0,0,0,0]
        balances = [0,0,0,0,0]
        unpaid_balances = [0,0,0,0,0]
        if not renewals:
            QMessageBox.warning(self, "Error", "No activity found for specified time period.")
            return None
        for renewal in renewals:
            charge = ZeroNone(renewal.renewal_fee)
            late = ZeroNone(renewal.late_fee)
            payment = ZeroNone(renewal.payment_amount)
            i = 0
            total_charged += charge
            total_received += min(charge, payment)
            total_late_fees += late
            total_late_fees_received += max(0, min(late, payment - charge))
            balance = payment - (charge + late)
            total_balance += balance
            total_pending += max(0, balance)
            if balance < 0:
                if renewal.payment_amount:
                    partial_payments += 1
                days = (datetime.date.today() - renewal.renewal_date).days
            elif not renewal.payment_date:
                days = 0
            else:
                days = (renewal.payment_date - renewal.renewal_date).days
            while i < last_interval and days >= intervals[i]:
                i += 1
            if renewal.renewal_fee == 0:
                total_uncharged += 1
            elif balance < 0:
                unpaid[i] += 1
                unpaid_balances[i] += balance
            else:
                paid[i] += 1
                balances[i] += payment
        
        values = {
        'start_date': start,
        'end_date': stop,
        'total_tests': self.countTests(start, stop),
        'total_charged': -total_charged,
        'total_received': total_received,
        'total_late_fees': -total_late_fees,
        'total_late_fee_payments': total_late_fees_received,
        'total_balance': total_balance,
        'total_renewals': len(renewals),
        'total_uncharged': total_uncharged,
        'paid': paid,
        'num_paid': sum(paid) + total_uncharged,
        'balance': balances,
        'total_payments': sum(balances),
        'unpaid': unpaid,
        'num_unpaid': sum(unpaid),
        'unpaid_balance': unpaid_balances,
        'total_unpaid': sum(unpaid_balances),
        'total_payments_pending': total_pending,
        'payments_pending': [],
        'partial_payments': partial_payments,
        }
        return values

    def fillForm(self):
        if not self.data:
            return
        
        self.renewalFeesLabel.setText(locale.currency(float(self.data['total_charged']), grouping=True))
        self.renewalFeePaymentsLabel.setText(locale.currency(float(self.data['total_received']), grouping=True))
        self.lateFeesLabel.setText(locale.currency(float(self.data['total_late_fees']), grouping=True))
        self.lateFeePaymentsLabel.setText(locale.currency(float(self.data['total_late_fee_payments']), grouping=True))
        self.unassignedPaymentsLabel.setText(locale.currency(float(self.data['total_payments_pending']), grouping=True))
        self.balanceLabel.setText(locale.currency(float(self.data['total_balance']), grouping=True))
        
        self.renewalFeesPushButton.setEnabled(self.data['total_charged'])
        self.renewalFeePaymentsPushButton.setEnabled(self.data['total_received'])
        self.lateFeesPushButton.setEnabled(self.data['total_late_fees'])
        self.lateFeePaymentsPushButton.setEnabled(self.data['total_late_fee_payments'])
        self.unassignedPaymentsPushButton.setEnabled(self.data['total_payments_pending'])

        self.testsCompletedPushButton.setText(str(self.data['total_tests']))
        self.renewalsIssuedPushButton.setText(str(self.data['total_renewals']))
        self.partialPaymentsPushButton.setText(str(self.data['partial_payments']))
        self.paidNoChargePushButton.setText(str(self.data['total_uncharged']))
        self.totalPaidPushButton.setText(str(self.data['num_paid']))
        self.totalUnpaidPushButton.setText(str(self.data['num_unpaid']))
        
        self.paymentTotalLabel.setText(locale.currency(float(self.data['total_payments']), grouping=True))
        self.outstandingBalanceTotalLabel.setText(locale.currency(float(self.data['total_unpaid']), grouping=True))

        for widget, value in zip(self.paidButtons, self.data['paid']):
            widget.setText(str(value))
        
        for widget, value in zip(self.paidLabels, self.data['balance']):
            widget.setText(locale.currency(float(value), grouping=True))

        for widget, value in zip(self.unpaidButtons, self.data['unpaid']):
            widget.setText(str(value))

        for widget, value in zip(self.unpaidLabels, self.data['unpaid_balance']):
            widget.setText(locale.currency(float(value), grouping=True))
        
        for widget in self.currencyWidgets:
            widget.setEnabled(True)
        
        for widget in self.countWidgets:
            if widget.text() != '0':
                widget.setEnabled(True)
    
    def getReport(self):
        if not self.data:
            self.data = self.getData()
            self.fillForm()
        if self.data:
            return(djprint.printQuarterlyPaymentSummary(self.data))

    def previewReport(self):
        if not self.data:
            self.data = self.getData()
        self.fillForm()

    def showRenewals(self, title, filter):
        start = self.beginDateEdit.date().toPyDate()
        stop = self.endDateEdit.date().toPyDate()
        renewals = filter(start, stop)
        names = getDentistNames(renewals)
        self.parent().viewText(djprint.viewRenewals(renewals, names, title, start, stop))

    def getRenewalFees(self, startDate, stopDate):
        renewals = Renewal.objects.filter(renewal_date__range=(startDate, stopDate))
        renewals = renewals.filter(renewal_fee__gt=0)
        return renewals

    @pyqtSignature("")
    def on_renewalFeesPushButton_clicked(self):
        title = "Renewals with Fees"
        filter = self.getRenewalFees
        self.showRenewals(title, filter)

    def getRenewalFeePayments(self, startDate, stopDate):
        renewals = Renewal.objects.filter(renewal_date__range=(startDate, stopDate))
        renewals = renewals.filter(payment_amount__gt=0)
        return renewals

    @pyqtSignature("")
    def on_renewalFeePaymentsPushButton_clicked(self):
        title = "Payments"
        filter = self.getRenewalFeePayments
        self.showRenewals(title, filter)

    def getLateFees(self, startDate, stopDate):
        renewals = Renewal.objects.filter(renewal_date__range=(startDate, stopDate))
        renewals = renewals.filter(late_fee__gt=0)
        return renewals

    @pyqtSignature("")
    def on_lateFeesPushButton_clicked(self):
        title = "Renewals with Late Fees"
        filter = self.getLateFees
        self.showRenewals(title, filter)

    def getLateFeePayments(self, startDate, stopDate):
        renewals = Renewal.objects.filter(renewal_date__range=(startDate, stopDate))
        renewals = renewals.filter(late_fee__gt=0)
        renewals = renewals.filter(payment_amount__gt=F('renewal_fee'))
        return renewals

    @pyqtSignature("")
    def on_lateFeePaymentsPushButton_clicked(self):
        title = "Renewals with Late Fee Payments"
        filter = self.getLateFeePayments
        self.showRenewals(title, filter)

    def getUnassignedPayments(self, startDate, stopDate):
        renewals = Renewal.objects.filter(renewal_date__range=(startDate, stopDate))
        renewals = renewals.filter(payment_amount__gt=F('renewal_fee')+F('late_fee'))
        return renewals
    
    @pyqtSignature("")
    def on_unassignedPaymentsPushButton_clicked(self):
        title = "Renewals with Unassigned Payments"
        filter = self.getUnassignedPayments
        self.showRenewals(title, filter)
        
    @pyqtSignature("")
    def on_testsCompletedPushButton_clicked(self):
        start = self.beginDateEdit.date().toPyDate()
        stop = self.endDateEdit.date().toPyDate()
        title = "Tests Completed"
        tests = Test.objects.filter(result_date__range=(start, stop))
        self.parent().viewText(djprint.viewTests(tests, title, start, stop))

    @pyqtSignature("")
    def on_renewalsIssuedPushButton_clicked(self):
        title = "Renewals Issued during Period"
        filter = self.getRenewals
        self.showRenewals(title, filter)

    def getPartialPayments(self, startDate, stopDate):
        renewals = Renewal.objects.filter(renewal_date__range=(startDate, stopDate))
        renewals = renewals.filter(payment_amount__lt=F('renewal_fee')+F('late_fee'))
        renewals = renewals.filter(payment_amount__gt=0)
        return renewals
        
    @pyqtSignature("")
    def on_partialPaymentsPushButton_clicked(self):
        title = "Partial Payments"
        filter = self.getPartialPayments
        self.showRenewals(title, filter)

    def getPaidNoCharge(self, startDate, stopDate):
        renewals = Renewal.objects.filter(renewal_date__range=(startDate, stopDate))
        renewals = renewals.filter(renewal_fee=0)
        return renewals
        
    @pyqtSignature("")
    def on_paidNoChargePushButton_clicked(self):
        title = "Renewals with No Charges"
        filter = self.getPaidNoCharge
        self.showRenewals(title, filter)

    def showPaidRenewals(self, title, range):
        intervals = [0,30,60,90,120]
        min = intervals[range-1]
        max = None
        if range < 5:
            max = intervals[range] - 1
        startDate = self.beginDateEdit.date().toPyDate()
        stopDate = self.endDateEdit.date().toPyDate()
        renewals = Renewal.objects.filter(renewal_date__range=(startDate, stopDate))
        renewals = renewals.filter(payment_date__gte=F('renewal_date')+datetime.timedelta(days=min))
        if max:
            renewals = renewals.filter(payment_date__lte=F('renewal_date')+datetime.timedelta(days=max))
        renewals = renewals.filter(payment_amount__gte=F('renewal_fee')+F('late_fee'))
        names = getDentistNames(renewals)
        self.parent().viewText(djprint.viewRenewals(renewals, names, title, startDate, stopDate))

    @pyqtSignature("")
    def on_paidPushButton1_clicked(self):
        title = "Paid 0-29 days."
        self.showPaidRenewals(title, 1)

    @pyqtSignature("")
    def on_paidPushButton2_clicked(self):
        title = "Paid 30-59 days."
        self.showPaidRenewals(title, 2)

    @pyqtSignature("")
    def on_paidPushButton3_clicked(self):
        title = "Paid 60-89 days."
        self.showPaidRenewals(title, 3)

    @pyqtSignature("")
    def on_paidPushButton4_clicked(self):
        title = "Paid 90-119 days."
        self.showPaidRenewals(title, 4)

    @pyqtSignature("")
    def on_paidPushButton5_clicked(self):
        title = "Paid 120+ days."
        self.showPaidRenewals(title, 5)

    def getTotalPaid(self, startDate, stopDate):
        renewals = Renewal.objects.filter(renewal_date__range=(startDate, stopDate))
        renewals = renewals.filter(payment_amount__gte=F('renewal_fee')+F('late_fee'))
        return renewals

    @pyqtSignature("")
    def on_totalPaidPushButton_clicked(self):
        title = "All Fully Paid Renewals."
        filter = self.getTotalPaid
        self.showRenewals(title, filter)

    def showUnpaidRenewals(self, title, range):
        intervals = [0,30,60,90,120]
        min = datetime.date.today() - datetime.timedelta(days = intervals[range-1])
        max = None
        if range < 5:
            max = datetime.date.today() - datetime.timedelta(days = intervals[range] - 1)
        startDate = self.beginDateEdit.date().toPyDate()
        stopDate = self.endDateEdit.date().toPyDate()
        renewals = Renewal.objects.filter(renewal_date__range=(startDate, stopDate))
        renewals = renewals.filter(renewal_date__lte=min)
        if max:
            renewals = renewals.filter(renewal_date__gte=max)
        renewals = renewals.exclude(payment_amount__gte=F('renewal_fee')+F('late_fee'))
        renewals = renewals.exclude(renewal_fee=0)
        names = getDentistNames(renewals)
        self.parent().viewText(djprint.viewRenewals(renewals, names, title, startDate, stopDate))

    @pyqtSignature("")
    def on_unpaidPushButton1_clicked(self):
        title = "Unpaid 0-29 days."
        self.showUnpaidRenewals(title, 1)

    @pyqtSignature("")
    def on_unpaidPushButton2_clicked(self):
        title = "Unpaid 30-59 days."
        self.showUnpaidRenewals(title, 2)

    @pyqtSignature("")
    def on_unpaidPushButton3_clicked(self):
        title = "Unpaid 60-89 days."
        self.showUnpaidRenewals(title, 3)

    @pyqtSignature("")
    def on_unpaidPushButton4_clicked(self):
        title = "Unpaid 90-119 days."
        self.showUnpaidRenewals(title, 4)

    @pyqtSignature("")
    def on_unpaidPushButton5_clicked(self):
        title = "Unpaid 120+ days."
        self.showUnpaidRenewals(title, 5)

    def getTotalUnpaid(self, startDate, stopDate):
        renewals = Renewal.objects.filter(renewal_date__range=(startDate, stopDate))
        renewals = renewals.exclude(payment_amount__gte=F('renewal_fee')+F('late_fee'))
        renewals = renewals.exclude(renewal_fee=0)
        return renewals

    @pyqtSignature("")
    def on_totalUnpaidPushButton_clicked(self):
        title = "All Unpaid Renewals."
        filter = self.getTotalUnpaid
        self.showRenewals(title, filter)

    @pyqtSignature("")
    def on_viewReportPushButton_clicked(self):
        self.parent().viewText(self.getReport())

    @pyqtSignature("")
    def on_previewReportPushButton_clicked(self):
        self.previewReport()

    @pyqtSignature("")
    def on_exitPushButton_clicked(self):
        self.close()


class YearlyComplianceDlg(QDialog, ui.Ui_yearlyComplianceDlg):
    
    def __init__(self, pos, parent):
        super(YearlyComplianceDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Yearly Compliance")
        self.move(pos)

        self.endDateEdit.setDate(datetime.date(datetime.date.today().year, 1, 15))
        self.beginDateEdit.setDate(datetime.date(datetime.date.today().year - 1, 1, 15))
        
        self.firstDentistSpinBox.setValue(1)
        self.lastDentistSpinBox.setValue(200)
        
        self.beginDateEdit.setCalendarPopup(True)
        self.endDateEdit.setCalendarPopup(True)
        self.statusLabel.setText("Choose reports to generate.")
        self.printing = False

    def getData(self):
        sterilizers = Sterilizer.objects.filter(inactive_date__isnull=True)
        sterilizers = sterilizers.filter(dentist__inactive_date__isnull=True)
        sterilizers = sterilizers.order_by("id")
        
        dentists = Dentist.objects.filter(inactive_date__isnull=True)
        dentists = dentists.filter(id__gte=self.firstDentistSpinBox.value())
        dentists = dentists.filter(id__lte=self.lastDentistSpinBox.value())
        dentists = dentists.order_by("id")
        
        lookup = {}
        for dentist in dentists:
            lookup[dentist.id] = []
        for sterilizer in sterilizers:
            dentist_id = SterilizerToDentistID(sterilizer.id)
            if dentist_id in lookup:
                lookup[dentist_id].append(sterilizer)
                
        return (dentists, lookup)

    @pyqtSignature("")
    def on_printLettersPushButton_clicked(self):
        (dentists, sterilizerDict) = self.getData()
        year = self.beginDateEdit.date().year()
        user = self.parent().parent().director
        self.printing = True
        for dentist in dentists:
            self.statusLabel.setText("Queuing reports for office #%s" % dentist.id)
            QCoreApplication.instance().processEvents()
            if not self.printing:
                self.statusLabel.setText("Queuing reports halted.")
                break
            for sterilizer in sterilizerDict[dentist.id]:
                start = str(sterilizer.id) + '000'
                stop = str(sterilizer.id) + '999'
                tests = Test.objects.filter(renewal__range=(start,stop))
                tests = tests.filter(sample_date__lte=self.endDateEdit.date().toPyDate())
                tests = tests.filter(sample_date__gte=self.beginDateEdit.date().toPyDate())
                numTests = tests.count()
                compliance = (numTests >= COMPLIANT_TESTS_PER_YEAR)
                self.parent().printHTML(djprint.printYearlyComplianceLetter(
                    dentist, sterilizer, compliance, year, numTests, user))
        self.printing = False
        self.statusLabel.setText("Queuing reports completed.")

    @pyqtSignature("")
    def on_printLabelsPushButton_clicked(self):
        (dentists, sterilizerDict) = self.getData()
        labelDlg = PrintLabelDlg(self.parent(), dentists)
        labelDlg.exec_()
        #labelDlg.on_printDentistsPushButton_clicked()

    @pyqtSignature("")
    def on_exitPushButton_clicked(self):
        if not self.printing:
            self.close()
        else:
            self.printing = False


class LotRecallDlg(QDialog, ui.Ui_lotRecallDlg):
    
    def __init__(self, pos, parent=None):
        super(LotRecallDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Lot Recall")
        self.move(pos)

        self.lotList = Lot.objects.all()
        self.lotList = self.lotList.order_by('-id')
        if len(self.lotList) == 0:
            QMessageBox.warning(self, "No Lots", "No valid lots found for renewal.")
            self.error_initializing = True
        else:
            for number, lot in enumerate(self.lotList):
                self.lotComboBox.insertItem(number, str(lot.id))
            self.lotComboBox.setCurrentIndex(0)
        self.printReportPushButton.setDisabled(True)

    def getRenewals(self, lot):
        list = Renewal.objects.filter(lot=lot.name)
        return list

    def getReport(self):
        lot = self.lotList[self.lotComboBox.currentIndex()]
        renewalList = self.getRenewals(lot)
        #if renewalList:
        dentistNameList = getDentistNames(renewalList)
        return(djprint.printLotRecall(renewalList, dentistNameList))
        #else:
        #    return ""

    @pyqtSignature("")
    def on_viewReportPushButton_clicked(self):
        self.parent().viewText(self.getReport())

    @pyqtSignature("")
    def on_printReportPushButton_clicked(self):
        self.parent().printText(self.getReport())

    @pyqtSignature("")
    def on_exitPushButton_clicked(self):
        self.close()