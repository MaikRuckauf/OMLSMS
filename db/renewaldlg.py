import sys, re, datetime
from constants import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import ui
from formviewdlg import FormViewPartialLoadDlg
from sendrenewaldlg import StartRenewalDlg, SendRenewalDlg

sys.path.append(OMLWEB_PATH)
from omlweb.models import Dentist, Renewal, Test, Lot
from django.db.models import Max
import djprint
from result import ResultDlg


NUM_HISTORY_COLUMNS = 10

    
class RenewalDlg(FormViewPartialLoadDlg, ui.Ui_renewalDlg):

    def __init__(self, parent=None):
        super(RenewalDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("OMLSMS Renewal")

        self.editWidgets = [self.renewalFeeSpinBox, self.datePaidLineEdit,
        self.amountPaidSpinBox, self.checkNumLineEdit, self.lateFeeSpinBox,
        self.commentTextEdit, self.waivePushButton]
        
        self.menuWidgets = [self.findPushButton, self.seekFirstPushButton,
        self.seekNextPushButton, self.seekPreviousPushButton, self.seekLastPushButton,
        self.startPushButton, self.sendPushButton, self.payPushButton,
        self.billPushButton, self.labelPushButton, self.reportPushButton,
        self.savePushButton, self.cancelPushButton, self.dateInactivePushButton]
        
        self.editFinalizeWidgets = [self.savePushButton, self.cancelPushButton]

        self.findValues = ["id", "lot", "renewal_date"]
        self.findSizes = {
        'field_widths': [150, 150, 150],
        'window_height': 400,
        'window_width': 500,
        'zfill': [RENEWAL_ID_WIDTH, None, None],
        }
        self.allRecords = Renewal.objects.all()

        self.current_month = datetime.date.today().month
        self.current_year = datetime.date.today().year
        self.orderedByRecordNumber = False # We sort by date then record num

        self.historyTableWidget.setColumnCount(NUM_HISTORY_COLUMNS)
        labels = ["renewal", "date", "lot", "fee", "late", "total", "paid", "sent", "back", "last"]
        widths = [       70,    53,    48,    47,     47,       47,     47,     35,     35,    53]
        self.historyTableWidget.setHorizontalHeaderLabels(labels)
        self.historyTableWidget.verticalHeader().hide()
        self.historyTableWidget.setSelectionBehavior(QTableView.SelectRows)
        for column, width in enumerate(widths):
            self.historyTableWidget.setColumnWidth(column, width)
        self.disableEditing()

    def loadPartialRecords(self):
        start_date, stop_date = self.getDateRange()
        self.records = Renewal.objects.filter(renewal_date__gte=start_date)
        self.records = self.records.filter(renewal_date__lt=stop_date)
        self.records = self.records.order_by("renewal_date", "id")

    def getRecordDate(self, id):
        try:
            record = Renewal.objects.get(id=id)
            return record.renewal_date
        except:
            return datetime.date.today()
        
    def getLatestID(self, partial_id):
        #unfortunately, leading zeros of the id are lost in database translation
        #we still need to use this information so dentist 2 doesn't become 20
        max_id = partial_id
        min_id = partial_id
        for i in xrange(0,RENEWAL_ID_WIDTH - len(partial_id)):
            max_id += '9'
            min_id += '0'
        records = Renewal.objects.filter(id__range=(int(min_id), int(max_id)))
        records = records.filter(id__startswith=int(partial_id)).order_by("-renewal_date")
        if records:
            return records[0].id
        else:
            return None
        
    def loadForm(self, record):
        try:
            dentist = Dentist.objects.get(id=RenewalToDentistID(record.id))
            self.setWindowTitle("SMS Renewal - " + dentist.getFullName())
        except:
            self.setWindowTitle("SMS Renewal - " + "( Error retrieving dentist )")
            dentist = None
        self.idLineEdit.setText(
            str(record.id).zfill(RENEWAL_ID_WIDTH) if record.id else ""
        )
        self.lotNameLineEdit.setText(record.lot)
        self.renewalDateLineEdit.setText(RecordDateToText(record.renewal_date))
        self.numTestsLineEdit.setText(str(record.num_tests))
        self.renewalFeeSpinBox.setValue(record.renewal_fee)
        self.lateFeeSpinBox.setValue(record.late_fee if record.late_fee else 0)
        self.datePaidLineEdit.setText(RecordDateToText(record.payment_date))
        self.amountPaidSpinBox.setValue(record.payment_amount if record.payment_amount else 0)
        self.checkNumLineEdit.setText(record.check_num)
        self.commentTextEdit.setText(record.comment)
        self.dateInactiveLineEdit.setText(RecordDateToText(record.inactive_date))
        #if not self.historyIsLoaded():
        self.loadHistory(record)

    def saveRecord(self, record, id=None):
        val = super(RenewalDlg, self).saveRecord(record)
        self.loadHistory(record)
        return val
    
    def verifyFormData(self):
        if self.idLineEdit.text() != "" and \
                not re.match("^\d{%s}$" % RENEWAL_ID_WIDTH, self.idLineEdit.text()):
            return self.idLineEdit, "Renewal ID has improper format."
        try:
            renewal_date = FormDateToRecord(self.renewalDateLineEdit.text())
            assert renewal_date.year > 1979
        except:
            return self.renewalDateLineEdit, "Renewal date is invalid."
        try:
            if self.datePaidLineEdit.text():
                payment_date = FormDateToRecord(self.datePaidLineEdit.text())
                assert payment_date.year > 1979
        except:
            return self.datePaidLineEdit, "Payment date is invalid."
        try:
            if self.amountPaidSpinBox.value():
                assert self.datePaidLineEdit.text()
        except:
            return self.datePaidLineEdit, "Please insert date of payment (or set payment to zero)."
        try:
            if self.datePaidLineEdit.text():
                assert self.checkNumLineEdit.text()
        except:
            return self.checkNumLineEdit, "Please insert Check Number"
        try:
            if self.dateInactiveLineEdit.text():
                inactive_date = FormDateToRecord(self.dateInactiveLineEdit.text())
                assert inactive_date >= renewal_date
        except:
            return self.dateInactiveLineEdit, "Inactive date is invalid."
        return None, None
    
    def saveForm(self, record, id=None):
        if self.idLineEdit.text():
            assert record.id == int(self.idLineEdit.text())
        else:
            assert record.id == None and self.inserting
        record.lot = self.lotNameLineEdit.text()
        record.renewal_date = FormDateToRecord(self.renewalDateLineEdit.text())
        record.num_tests = int(self.numTestsLineEdit.text())
        record.renewal_fee = self.renewalFeeSpinBox.value()
        record.late_fee = self.lateFeeSpinBox.value()
        record.payment_date = FormDateToRecord(self.datePaidLineEdit.text())
        record.payment_amount = self.amountPaidSpinBox.value()
        if not record.payment_date and record.payment_amount == 0:
            record.payment_amount = None
        record.check_num = self.checkNumLineEdit.text()
        record.comment = self.commentTextEdit.toPlainText()
        record.inactive_date = FormDateToRecord(self.dateInactiveLineEdit.text())

    def prepareNewRecord(self):
        # records are created only through Send Renewals function
        return None
    
    def getTargetInsertId(self, record):
        # records are created only through Send Renewals function
        return None

    def makeBookmark(self):
        if re.match("^\d{%s}$" % RENEWAL_ID_WIDTH, self.idLineEdit.text()):
            return {
            'dentist': self.idLineEdit.text()[0:DENTIST_ID_WIDTH],
            'sterilizer': self.idLineEdit.text()[0:STERILIZER_ID_WIDTH],
            'renewal': self.idLineEdit.text(),
            'lot': self.idLineEdit.text()[STERILIZER_ID_WIDTH:]
            }
        return {}

    def goToBookmark(self, bookmark):
        if 'renewal' in bookmark and \
        bookmark['renewal'][0:STERILIZER_ID_WIDTH] == bookmark['sterilizer'] and \
        bookmark['renewal'][0:DENTIST_ID_WIDTH] == bookmark['dentist']:
            self.findRecord(int(bookmark['renewal']))
        elif 'sterilizer' in bookmark and \
        bookmark['sterilizer'][0:DENTIST_ID_WIDTH] == bookmark['dentist']:
            id = self.getLatestID((bookmark['sterilizer']))
            if id:
                self.findRecord(id)
            else:
                self.reportNotFound('Renewal', 'Sterilizer', bookmark['sterilizer'])
        elif 'dentist' in bookmark:
            id = self.getLatestID((bookmark['dentist']))
            if id:
                self.findRecord(id)
            else:
                self.reportNotFound('Renewal', 'Dentist', bookmark['dentist'])

    def historyIsLoaded(self):
        try:
            row = self.historyTableWidget.currentRow()
            self.historyTableWidget.setCurrentCell(row, 0)
            if int(self.historyTableWidget.currentItem().text()) == \
                int(self.idLineEdit.text()):
                return True
        except:
            pass
        return False

    def loadHistory(self, record):
        # fill table with column titles:
        #["renewed", "lot", "fee", "late", "total", "paid", "sent", "back", "last"]
        renewals = Renewal.objects.filter(sterilizer=record.sterilizer)
        renewals = renewals.order_by("-renewal_date")
        tests = Test.objects.filter(renewal__sterilizer__exact=record.sterilizer)
        self.historyTableWidget.setRowCount(len(renewals))
        for row, renewal in enumerate(renewals):
            if renewal.id == int(self.idLineEdit.text()):
                self.historyTableWidget.setCurrentCell(row, 0)
            text = range(0, NUM_HISTORY_COLUMNS)
            text[0] = str(renewal.id).zfill( RENEWAL_ID_WIDTH) 
            text[1] = RecordDateToText(renewal.renewal_date, shorten=True)
            text[2] = renewal.lot
            text[3] = NumToCurrency(renewal.renewal_fee)
            text[4] = NumToCurrency(renewal.late_fee)
            text[5] = NumToCurrency(
                           renewal.renewal_fee if renewal.renewal_fee else 0 + \
                           renewal.late_fee if renewal.late_fee else 0
                       )
            text[6] = NumToCurrency(renewal.payment_amount)
            text[7] = str(renewal.num_tests)
            max_test_num = 0
            test_date = None
            for test in tests:
                if test.renewal_id == renewal.id and test.test_num > max_test_num:
                    max_test_num = test.test_num
                    test_date = test.start_date
            if test_date:
                text[8] = str(max_test_num)
                text[9] = RecordDateToText(test_date, shorten=True)
            else:
                text[8] = ""
                text[9] = ""
            for column in range(0, len(text)):
                item = QTableWidgetItem(text[column] if text[column] else "")
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.historyTableWidget.setItem(row, column, item)

    def updateAmountDue(self):
        self.amountDueSpinBox.setValue(
            self.renewalFeeSpinBox.value() + self.lateFeeSpinBox.value()
        )
    
    @pyqtSignature("")
    def on_dateInactivePushButton_clicked(self):
        msgBox = QMessageBox()
        id = self.idLineEdit.text()
        type = "Renewal"
        disableMsg = "Disabling this renewal will disable all remaining " + \
            "tests.  Proceed?"
        enableMsg = "Enabling this lot will enable all remaining " + \
            "tests.  Proceed?"
        self.toggleActive(id, type, disableMsg, enableMsg)

    @pyqtSignature("QTableWidgetItem *")
    def on_historyTableWidget_itemClicked(self, item):
        if not self.editing:
            row = self.historyTableWidget.currentRow()
            self.historyTableWidget.setCurrentCell(row, 0)
            id = int(self.historyTableWidget.currentItem().text())
            self.historyTableWidget.setCurrentCell(row, 1)
            date = FormDateToRecord(self.historyTableWidget.currentItem().text(),
                shortened=True)
            self.findDatedRecord(id, date)

    @pyqtSignature("")
    def on_payPushButton_clicked(self):
        if not self.datePaidLineEdit.text():
            date = datetime.date.today().strftime(DATETIME_FORMAT)
            self.datePaidLineEdit.setText(date)
        if not self.amountPaidSpinBox.value():
            self.amountPaidSpinBox.setValue(self.amountDueSpinBox.value())
        self.on_modifyPushButton_clicked()
        self.checkNumLineEdit.setFocus()

    @pyqtSignature("")
    def on_waivePushButton_clicked(self):
        self.lateFeeSpinBox.setValue(0)

    @pyqtSignature("")
    def on_startPushButton_clicked(self):
        startDlg = StartRenewalDlg(self)
        if not startDlg.error_initializing:
            startDlg.exec_()

    @pyqtSignature("")
    def on_sendPushButton_clicked(self):
        sendDlg = SendRenewalDlg(self)
        sendDlg.exec_()

    @pyqtSignature("const QString&")
    def on_renewalFeeSpinBox_valueChanged(self, newText):
        self.updateAmountDue()

    @pyqtSignature("const QString&")
    def on_lateFeeSpinBox_valueChanged(self, newText):
        self.updateAmountDue()

    @pyqtSignature("")
    def on_labelPushButton_clicked(self):

        renewal = self.getCurrentRecord()
        id = RenewalToLotID(renewal.id)
        lot = Lot.objects.get(id=id)
        sterilizer = renewal.sterilizer
        dentist = sterilizer.dentist
        
        self.printHTML(djprint.getRenewalLabelsForSterilizers([sterilizer], [dentist], lot), spawn=False, useLabelPrinter=True)
    
    @pyqtSignature("")
    def on_billPushButton_clicked(self):
        id = self.idLineEdit.text()[0:STERILIZER_ID_WIDTH]
        self.printHTML(djprint.getBillForSterilizer(id))

    @pyqtSignature("")
    def on_reportPushButton_clicked(self):
        id = self.idLineEdit.text()
        dlg = ResultDlg(False, RenewalToSterilizerID(id), self)
        dlg.exec_()