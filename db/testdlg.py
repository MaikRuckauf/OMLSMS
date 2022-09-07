import sys, re, datetime, time
from constants import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import ui
from formviewdlg import FormViewPartialLoadDlg
from testnotifydlg import TestNotifyDlg

sys.path.append(OMLWEB_PATH)
from omlweb.models import Renewal, Test, Dentist, Lot
from django.db.models import Max
import djprint
from result import ResultDlg
from finddlg import FindDlg


NUM_HISTORY_COLUMNS = 7


class StartTestDlg(QDialog, ui.Ui_startTestDlg):
    pass
    
class TestDlg(FormViewPartialLoadDlg, ui.Ui_testDlg):

    def __init__(self, parent=None):
        super(TestDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("OMLSMS Test")

        self.editWidgets = [self.sterilizeDateEdit, self.startDateLineEdit,
        self.resultDateLineEdit, self.testResultPushButton, self.controlResultPushButton,
        self.startedByLineEdit, self.resultsByLineEdit, self.commentTextEdit,
        self.stripNumLineEdit, self.prevDayPushButton, self.nextDayPushButton]

        self.menuWidgets = [self.findPushButton, self.seekFirstPushButton,
        self.seekNextPushButton, self.seekPreviousPushButton, self.seekLastPushButton,
        self.startPushButton, self.resultPushButton, self.modifyPushButton,
        self.savePushButton, self.cancelPushButton, self.reportPushButton]
        
        self.editFinalizeWidgets = [self.savePushButton, self.cancelPushButton]

        self.findValues = ["id", "lot", "renewal_date"]
        self.findSizes = {
        'field_widths': [150, 150, 150],
        'window_height': 400,
        'window_width': 500,
        'zfill': [RENEWAL_ID_WIDTH, None, None],
        }
        
        #self.findValues = ["renewal.id", "test_num", "start_date", "result_date", "result"]
        #self.findSizes = {
        #'field_widths': [150, 50, 100, 100, 50],
        #'window_height': 400,
        #'window_width': 500,
        #'zfill': [RENEWAL_ID_WIDTH, None, None, None, None],
        #}
        self.sterilizeDateEdit.setCalendarPopup(True)
        self.allRecords = Test.objects.all()

        self.current_month = datetime.date.today().month
        self.current_year = datetime.date.today().year
        self.orderedByRecordNumber = False # We sort by date then record num
        self.startingTests = False
        self.enteringResults = False
        self.notifying = False
        self.lastInsert = None
        self.testResultPushButton.setFocusPolicy(Qt.NoFocus)
        self.controlResultPushButton.setFocusPolicy(Qt.NoFocus)
        self.prevDayPushButton.setFocusPolicy(Qt.NoFocus)
        self.nextDayPushButton.setFocusPolicy(Qt.NoFocus)
        self.suppliedPushButton.setFocusPolicy(Qt.NoFocus)
        self.omittedPushButton.setFocusPolicy(Qt.NoFocus)
        self.historyTableWidget.setColumnCount(NUM_HISTORY_COLUMNS)
        labels = ["renewal", "num", "run date", "start date", "result date", "result", "ctrl"]
        widths = [       70,    53,         70,           70,            70,       47,     47]
        self.historyTableWidget.setHorizontalHeaderLabels(labels)
        self.historyTableWidget.verticalHeader().hide()
        self.historyTableWidget.setSelectionBehavior(QTableView.SelectRows)
        for column, width in enumerate(widths):
            self.historyTableWidget.setColumnWidth(column, width)
        self.disableEditing()

    def findDatedRecord(self, id, date, testNum=None):
        #print "find", id, date, testNum
        if (date.month != self.current_month or date.year != self.current_year):
            self.current_month = date.month
            self.current_year = date.year
            self.loadPartialRecords()
        for index, record in enumerate(self.records):
            if record.renewal_id == id and \
               (not testNum or testNum == record.test_num):
                self.setRecordNum(index)
                return
        self.setRecordNum(0)

    def findRecord(self, id, record):
        #print "find test %s" % id
        if id:
            if record:
                record_date = record.start_date
                testNum = record.test_num
            else:
                record_date = self.getRecordDate(id)
                testNum = None
            return self.findDatedRecord(id, record_date, testNum)

    def loadPartialRecords(self):
        start_date, stop_date = self.getDateRange()
        #print "load start: %s, stop %s" % (str(start_date), str(stop_date))
        self.records = Test.objects.filter(start_date__gte=start_date)
        self.records = self.records.filter(start_date__lt=stop_date)
        self.records = self.records.order_by("start_date",  "renewal", "test_num")

    def getRecordDate(self, id):
        try:
            records = Test.objects.filter(renewal_id=id).order_by("-start_date")
            #print records
            return records[0].start_date
        except:
            return None

    def getLatest(self, partial_id):
        #unfortunately, leading zeros of the id are lost in database translation
        #we still need to use this information so dentist 2 doesn't become 20
        max_id = partial_id
        min_id = partial_id
        for i in xrange(0,RENEWAL_ID_WIDTH - len(partial_id)):
            max_id += '9'
            min_id += '0'
        records = Test.objects.filter(renewal__id__range=(int(min_id), int(max_id)))
        records = records.filter(renewal__id__startswith=int(partial_id)).order_by("-start_date")
        #print records
        if records:
            return records[0]
        else:
            return None

    def loadForm(self, record):
        #print "loading " + str(record)
        try:
            dentist = Dentist.objects.get(id=RenewalToDentistID(record.renewal.id))
            self.setWindowTitle("SMS Test - " + dentist.getFullName())
        except:
            self.setWindowTitle("SMS Renewal - " + "( Error retrieving dentist )")
            dentist = None
        self.renewalIdLineEdit.setText(
            str(record.renewal_id).zfill(RENEWAL_ID_WIDTH) if record.renewal_id else ""
        )
        self.renewalIdLineEdit.setAlignment(Qt.AlignHCenter)
        self.testNumLineEdit.setText(str(record.test_num))
        self.maxTestNumLineEdit.setText(str(record.renewal.num_tests))
        self.renewalDateEdit.setText(RecordDateToText(record.renewal.renewal_date))
        self.sterilizeDateEdit.setDate(record.sample_date)
        self.startDateLineEdit.setText(RecordDateToText(record.start_date))
        self.testResultPushButton.setText(record.result if record.result else "")
        self.notifyPushButton.setEnabled(self.testResultPushButton.text() == "+")
        self.controlResultPushButton.setText(record.control_result if record.control_result else "")
        self.resultDateLineEdit.setText(RecordDateToText(record.result_date))
        self.startedByLineEdit.setText(record.started_by)
        self.resultsByLineEdit.setText(record.finished_by)
        self.commentTextEdit.setText(record.comment)
        self.stripNumLineEdit.setText(str(record.strip_num) if record.strip_num else "")
        
        #if not self.historyIsLoaded():
        self.loadHistory(record)

    def verifyFormData(self):
        if not re.match("^\d{%s}$" % RENEWAL_ID_WIDTH, self.renewalIdLineEdit.text()):
            return self.renewalIdLineEdit, "Renewal ID has improper format."
        try:
            i = int(self.testNumLineEdit.text())
            assert i > 0 and i < 99
        except:
            return self.testNumLineEdit, "Invalid test number!"
        try:
            if self.stripNumLineEdit.text():
                strip = int(self.stripNumLineEdit.text())
                assert strip > 0 and strip < 100
                assert strip <= int(self.maxTestNumLineEdit.text())
        except:
            return self.stripNumLineEdit, "Invalid strip number."
        try:
            start_date = FormDateToRecord(self.startDateLineEdit.text())
            assert start_date.year > 1980
        except:
            return self.startDateLineEdit, "Invalid start date."
        if start_date < self.sterilizeDateEdit.date().toPyDate():
            return self.sterilizeDateEdit, "Start date can't be before sterilize date."
        try:
            if self.resultDateLineEdit.text():
                result_date = FormDateToRecord(self.resultDateLineEdit.text())
                assert result_date.year > 1980
            else:
                result_date = None
        except:
            return self.resultDateLineEdit, "Invalid result date."
        if result_date and result_date < start_date:
            return self.resultDateLineEdit, "Result date can't be before start date."
        if not self.startedByLineEdit.text():
            return self.startedByLineEdit, "Need initials."
        if len(self.startedByLineEdit.text()) > 3:
            return self.startedByLineEdit, "Initials too long."
        if self.resultDateLineEdit.text() and not self.resultsByLineEdit.text():
            return self.resultsByLineEdit, "Need initials."
        if len(self.resultsByLineEdit.text()) > 3:
            return self.resultsByLineEdit, "Initials too long."
        try:
            result = self.testResultPushButton.text()
            control = self.controlResultPushButton.text()
            assert result == "" or result == '+' or result == '-'
            assert control == "" or control == '+' or control == '-'
        except:
            return self.resultPushButton, "Invalid test result!"
        if (not result and control == '-'):
            # should assume control was used as test
            return self.resultPushButton, "Invalid test result.  Should consider test submitted as control; '- O' as result."
        if (result == '+' and not control):
            # should assume test was not submitted
            return self.resultPushButton, "Invalid test result.  Should consider control submitted as test; 'O +' as result."
        if (result == '+' and control == '-'):
            # should assume test and control swapped
            return self.resultPushButton, "Invalid test result.  Should consider control and test swapped; '- +' as result."
        if (result or control or self.resultsByLineEdit.text()) and not self.resultDateLineEdit.text():
            return self.resultDateLineEdit, "Need result date."
        return None, None

    def saveRecord(self, record, id=None):
        val = super(TestDlg, self).saveRecord(record)
        self.loadHistory(record)
        return val

    def saveForm(self, record, id=None):
        record.sample_date = self.sterilizeDateEdit.date().toPyDate()
        record.start_date = FormDateToRecord(self.startDateLineEdit.text())
        record.result = self.testResultPushButton.text()
        record.control_result = self.controlResultPushButton.text()
        record.result_date = FormDateToRecord(self.resultDateLineEdit.text())
        record.started_by = self.startedByLineEdit.text()
        record.finished_by = self.resultsByLineEdit.text()
        if str(self.commentTextEdit.toPlainText()).isspace():
            record.comment = ""
        else:
            record.comment = self.commentTextEdit.toPlainText()
        record.strip_num = int(self.stripNumLineEdit.text()) if self.stripNumLineEdit.text() else None
        self.notifyPushButton.setEnabled(self.testResultPushButton.text() == "+")

    def makeBookmark(self):
        if re.match("^\d{%s}$" % RENEWAL_ID_WIDTH, self.renewalIdLineEdit.text()) and \
           re.match("^\d{1,2}$", self.testNumLineEdit.text()):
            return {
            'dentist': self.renewalIdLineEdit.text()[0:DENTIST_ID_WIDTH],
            'sterilizer': self.renewalIdLineEdit.text()[0:STERILIZER_ID_WIDTH],
            'renewal': self.renewalIdLineEdit.text(),
            'lot': self.renewalIdLineEdit.text()[STERILIZER_ID_WIDTH:],
            #'test': self.renewalIdLineEdit.text() + self.testNumLineEdit.text(),
            }
        return {}

    def goToBookmark(self, bookmark):
        #print 'bookmark', bookmark
        if 'renewal' in bookmark and \
        bookmark['renewal'][0:STERILIZER_ID_WIDTH] == bookmark['sterilizer'] and \
        bookmark['renewal'][0:DENTIST_ID_WIDTH] == bookmark['dentist']:
            #print "renewal bookmark %s" % bookmark['renewal']
            record = self.getLatest(bookmark['renewal'])
            if not record:
                record = self.getLatest(bookmark['renewal'][0:STERILIZER_ID_WIDTH])
            if record:
                self.findRecord(record.renewal_id, record)
            else:
                self.reportNotFound('Test', 'Renewal', bookmark['renewal'])
        elif 'sterilizer' in bookmark and \
        bookmark['sterilizer'][0:DENTIST_ID_WIDTH] == bookmark['dentist']:
            #print "sterilizer bookmark %s" % bookmark['sterilizer']
            record = self.getLatest(bookmark['sterilizer'])
            if record:
                self.findRecord(record.renewal_id, record)
            else:
                self.reportNotFound('Test', 'Sterilizer', bookmark['sterilizer'])
        elif 'dentist' in bookmark:
            #print "dentist bookmark %s" % bookmark['dentist']
            record = self.getLatest(bookmark['dentist'])
            if record:
                self.findRecord(record.renewal_id, record)
            else:
                self.reportNotFound('Test', 'Dentist', bookmark['dentist'])

    def historyIsLoaded(self):
        try:
            row = self.historyTableWidget.currentRow()
            self.historyTableWidget.setCurrentCell(row, 0)
            if int(self.historyTableWidget.currentItem().text()) == \
                    int(self.idLineEdit.text()):
                self.historyTableWidget.setCuurentCell(row, 1)
                if int(self.historyTableWidget.currentItem.text()) == \
                    int(self.testNumLineEdit.text()):
                    return True
        except:
            pass
        return False

    def loadHistory(self, record):
        # fill table with column titles:
        #["renewal", "num", "run", "start", "result", "result", "ctrl"]
        start = str(record.renewal)[0:-3] + '000'
        stop = str(record.renewal)[0:-3] + '999'
        tests = Test.objects.filter(renewal__range=(start,stop))
        tests = tests.order_by("-start_date", "-renewal", "-test_num")
        self.historyTableWidget.setRowCount(len(tests))

        for row, test in enumerate(tests):
            if test.renewal_id == int(self.renewalIdLineEdit.text()) and \
            test.test_num == int(self.testNumLineEdit.text()):
                self.historyTableWidget.setCurrentCell(row, 0)
            text = range(0, NUM_HISTORY_COLUMNS)
            text[0] = str(test.renewal_id).zfill(RENEWAL_ID_WIDTH) 
            text[1] = str(test.test_num)
            text[2] = RecordDateToText(test.sample_date, shorten=True)
            text[3] = RecordDateToText(test.start_date, shorten=True)
            text[4] = RecordDateToText(test.result_date, shorten=True)
            text[5] = test.result if test.result else ""
            text[6] = test.control_result if test.control_result else ""
            for column in range(0, len(text)):
                item = QTableWidgetItem(text[column])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter)
                self.historyTableWidget.setItem(row, column, item)
        self.historyTableWidget.resizeColumnsToContents()

    def dlgPos(self):
        p = QPoint(self.rect().right(), self.rect().top())
        return self.pos() + p + QPoint(20, 30)
    
    def makeNotifyWindow(self, record, user):
        self.notifying = True
        for widget in self.editWidgets:
            widget.setDisabled(True)
        for widget in self.menuWidgets:
            widget.setDisabled(True)
        self.historyTableWidget.setSelectionMode(QTableView.NoSelection)
        self.notifyPushButton.setDisabled(True)
        notifyDlg = TestNotifyDlg(record, user, self.dlgPos(), self)
        notifyDlg.show()

        # notify window is not modal, but wait for it to close
        while notifyDlg.isVisible():
            QCoreApplication.instance().processEvents()
            time.sleep(0.04)
        if notifyDlg.comment:
            self.commentTextEdit.setText(self.commentTextEdit.toPlainText() +
                notifyDlg.comment)
        success, widget = self.saveRecord(self.getCurrentRecord())
        if not success:
            msg = "Database error:  Could not record contact results!  Make a " + \
              "paper record and enter it into the test's comment section as soon as possible."
            QMessageBox.warning(self, "Database Error", msg)

        self.historyTableWidget.setSelectionMode(QTableView.SingleSelection)
        self.notifying = False
        if not self.enteringResults:
            self.notifyPushButton.setEnabled(True)
            for widget in self.menuWidgets:
                if widget not in self.editFinalizeWidgets:
                    widget.setEnabled(True)

    def getIDinput(self, ttl):
        for widget in self.menuWidgets:
            widget.setDisabled(True)
        self.cancelPushButton.setEnabled(True)
        
        self.setWindowTitle(ttl)
        self.renewalIdLineEdit.setText("")
        self.testNumLineEdit.setText("")
        self.maxTestNumLineEdit.setText("")
        self.renewalDateEdit.setText("")
        self.sterilizeDateEdit.setDate(datetime.date.today())
        self.startDateLineEdit.setText("")
        self.testResultPushButton.setText("")
        self.notifyPushButton.setEnabled(False)
        self.controlResultPushButton.setText("")
        self.resultDateLineEdit.setText("")
        self.startedByLineEdit.setText("")
        self.resultsByLineEdit.setText("")
        self.commentTextEdit.setText("")
        self.stripNumLineEdit.setText("")
        self.historyTableWidget.setRowCount(0)
        self.renewalIdLineEdit.setAlignment(Qt.AlignLeft)
        self.renewalIdLineEdit.setEnabled(True)
        self.renewalIdLineEdit.setFocus()
        self.renewalIdLineEdit.grabKeyboard()
        self.editing = True
        self.lastInsert = None

    def startTests(self):
        self.getIDinput("Start New Test: Input Test ID")
        self.startingTests = True

    def startTest(self, id, strip, renewal, tests):
        try:
            try:
                assert not renewal.inactive_date
                assert not renewal.sterilizer.inactive_date
                assert not renewal.sterilizer.dentist.inactive_date
            except:
                ttl = "Inactive"
                msg = "The matching renewal, sterilizer, or dentist was previously " + \
                "marked inactive.  These must be active to process this test."
                assert False
            try:
                lot = Lot.objects.get(id=RenewalToLotID(id))
            except:
                ttl = "Database Error"
                msg = "Cannot find matching lot %d." % RenewalToLot(id)
                assert False
            try:
                assert not lot.inactive_date
                assert datetime.date.today() <= lot.expiration_date
            except:
                ttl = "Inactive Lot"
                msg = "This lot has been marked " + \
                "inactive or has expired.  This test cannot be processed."
                assert False
            try:
                for test in tests:
                    assert not strip or strip != test.strip_num
            except:
                ttl = "Input Error"
                msg = "This strip has already been processed.  It can't be processed " + \
                "twice."
                assert False
        except:
            QMessageBox.warning(self, ttl, msg)
            self.renewalIdLineEdit.setText("")
            self.renewalIdLineEdit.grabKeyboard()
            return

        try:
            if tests:
                assert tests[0].test_num < renewal.num_tests
        except:
            ttl = "Too Many Tests"
            msg = "The number of tests currently in the database for this renewal " + \
            "meets or exceeds the number of tests that were alloted.  This test may be " + \
            "valid if a test was mistakenly entered twice at some point. " + \
            "Do you wish to start this test?"
            if QMessageBox.warning(self, ttl, msg, QMessageBox.Yes, QMessageBox.No) != QMessageBox.Yes:
                self.renewalIdLineEdit.setText("")
                self.renewalIdLineEdit.grabKeyboard()
                return
        try:
            for test in tests:
                assert test.start_date != datetime.date.today() or \
                   ((strip and test.strip_num) and (strip != test.strip_num))
        except:
            ttl = "Ambiguous Test Found"
            msg = "Another test was started for this renewal today.  This may " + \
            "be a valid test if multiple tests were received and at least one " + \
            "was not entered with a strip number.  Do you wish to start this test?"
            if QMessageBox.warning(self, ttl, msg, QMessageBox.Yes, QMessageBox.No) != QMessageBox.Yes:
                self.renewalIdLineEdit.setText("")
                self.renewalIdLineEdit.grabKeyboard()
                return
        self.inserting = self.createTest(id, strip, renewal, tests)
        self.loadForm(self.inserting)
        self.editStart()

    def createTest(self, id, strip, renewal, tests):
        if tests:
            test_num = tests[0].test_num + 1
        else:
            test_num = 1
        return Test(
            renewal = renewal,
            test_num = test_num,
            sample_date = datetime.date.today(),
            start_date = datetime.date.today(),
            result = None,
            control_result = None,
            result_date = None,
            started_by = self.parent().user.initials,
            finished_by = "",
            comment = "",
            strip_num = strip if strip else "",
        )

    def editStart(self):
        self.renewalIdLineEdit.setDisabled(True)
        self.sterilizeDateEdit.setEnabled(True)
        self.prevDayPushButton.setEnabled(True)
        self.nextDayPushButton.setEnabled(True)
        self.suppliedPushButton.setEnabled(True)
        self.omittedPushButton.setEnabled(True)
    
    def stopEditStart(self):
        self.sterilizeDateEdit.setEnabled(False)
        self.prevDayPushButton.setEnabled(False)
        self.nextDayPushButton.setEnabled(False)
        self.suppliedPushButton.setEnabled(False)
        self.omittedPushButton.setEnabled(False)
        
    def enterResults(self):
        self.getIDinput("Enter Test Results: Input Test ID")
        self.enteringResults = True

    def enterResult(self, id, strip, renewal, tests):
        match = None
        count = 0
        if strip:
            # look for a matching strip number if available
            for test in tests:
                if strip == test.strip_num:
                    match = test
                    count = 1
        else:
            # if there is no strip number, look only for tests started 7 days prior
            date = datetime.date.today() - datetime.timedelta(days = DAYS_FOR_TEST)
            #print date
            for test in tests:
                if not test.strip_num and not test.result_date and test.start_date == date:
                    match = test
                    count += 1
            if not match:
                # if still not found, consider all tests as possible
                for test in tests:
                    if not test.strip_num and not test.result_date:
                        match = test
                        count += 1
        if not match:
            ttl = "Not Found"
            msg = "Test %d %s not found." % (id, (", strip %d" % strip) if strip else "")
            QMessageBox.warning(self, ttl, msg)
            self.renewalIdLineEdit.setText("")
            self.renewalIdLineEdit.grabKeyboard()
            return
        if count > 1:
            ttl = "Multiple Entries"
            msg = "Multiple tests with id %d found.  Please check run dates " % id + \
            "and select the appropriate test."
            QMessageBox.warning(self, ttl, msg)
        if match.result_date:
            # this can only happen if a strip number was provided
            ttl = "Previously Entered"
            msg = "Test results for id %d, strip %d has " % (id, strip) + \
            "already been entered.  Default results will not be entered " + \
            "to preserve the old data."
            QMessageBox.warning(self, ttl, msg)
        try:
            # None of these should fail, but double check to prevent data corruption
            self.findRecord(id, match)
            assert int(self.renewalIdLineEdit.text()) == match.renewal_id
            assert FormDateToRecord(self.startDateLineEdit.text()) == match.start_date
            assert not strip or not self.stripNumLineEdit.text() or \
                int(self.stripNumLineEdit.text()) == match.strip_num
        except:
            ttl = "Database Error"
            msg = "Could not load match from database."
            QMessageBox.warning(self, ttl, msg)
            self.renewalIdLineEdit.grabKeyboard()
            return
        if not match.result_date:
            self.initializeResults()
        self.editResults()
            
    def initializeResults(self):
        self.testResultPushButton.setText("-")
        self.controlResultPushButton.setText("+")
        self.resultDateLineEdit.setText(datetime.date.today().strftime(DATETIME_FORMAT))
        self.resultsByLineEdit.setText(self.parent().user.initials)
    
    def editResults(self):
        self.renewalIdLineEdit.setDisabled(True)
        self.testResultPushButton.setEnabled(True)
        self.controlResultPushButton.setEnabled(True)
        self.savePushButton.setEnabled(True)
        self.savePushButton.grabKeyboard()
    
    def stopEditResults(self):
        self.testResultPushButton.setDisabled(True)
        self.controlResultPushButton.setDisabled(True)
        self.savePushButton.setDisabled(True)
        self.savePushButton.releaseKeyboard()

    def insertTest(self, verified=True):
        self.stopEditStart()
        self.addStartComments(verified)
        success, widget = self.saveRecord(self.getCurrentRecord())
        if not success:
            ttl = "Database Error"
            msg = "Could not save test to database."
            QMessageBox.warning(self, ttl, msg)
            self.editStart()
        else:
            sterilizer = self.getCurrentRecord().renewal.sterilizer
            if self.getCurrentRecord().test_num == sterilizer.renew_test:
                sterilizer.renew = True
                #print "renew", sterilizer
                try:
                    sterilizer.save(False)
                except:
                    msg = "Could not renew sterilizer %d." % sterilizer.id
                    QMessageBox.warning(self, "Database Error", msg)
            self.inserting = None
            self.startTests()
            self.lastInsert = True
    
    def addStartComments(self, verified=True):
        sample_date = self.sterilizeDateEdit.date().toPyDate()
        try:
            start_date = FormDateToRecord(self.startDateLineEdit.text())
        except:
            return #will be caught in form verify
        comment = self.commentTextEdit.toPlainText()
        count = 0
        try:
            id = int(self.renewalIdLineEdit.text())
            count = Test.objects.filter(renewal_id=id).filter(start_date=datetime.date.today()).count()
        except:
            pass
        if count:
            comment = "Multiple Tests submitted on the same date; please mail day of testing.\n" + comment
        if sample_date + datetime.timedelta(days=7) < start_date:
            comment = "Late... Test Strips received greater than 7 days post " + \
                "testing.  Please mail day of testing.\n" + comment
        elif sample_date == start_date and not verified:
            comment = "Missing Testing Date... date required for accurate processing.\n" + \
                comment
        self.commentTextEdit.setText(comment)
    
    def addResultComments(self):
        result = self.testResultPushButton.text()
        control = self.controlResultPushButton.text()
        comment = self.commentTextEdit.toPlainText()
        if not result and not control:
            comment = "No test submitted.\n" + comment
        elif not result and control == '+':
            comment = "No Test Strip submitted.\n" + comment
        elif result == "-" and not control:
            comment = "No Control Strip submitted; unable to verify results.\n" + comment
        elif result == "-" and control == "-":
            comment = "Control Strip appears sterilized; unable to verify results.\n" + comment
        self.commentTextEdit.setText(comment)

    @pyqtSignature("QTableWidgetItem *")
    def on_historyTableWidget_itemClicked(self, item):
        if not self.editing and not self.notifying:
            row = self.historyTableWidget.currentRow()
            self.historyTableWidget.setCurrentCell(row, 0)
            id = int(self.historyTableWidget.currentItem().text())
            self.historyTableWidget.setCurrentCell(row, 1)
            testnum = int(self.historyTableWidget.currentItem().text())
            self.historyTableWidget.setCurrentCell(row, 3)
            date = FormDateToRecord(self.historyTableWidget.currentItem().text(),
                shortened=True)
            #print id, date, testnum
            self.findDatedRecord(id, date, testnum)

    @pyqtSignature("")
    def on_startPushButton_clicked(self):
        self.startTests()

    @pyqtSignature("")
    def on_resultPushButton_clicked(self):
        self.enterResults()

    @pyqtSignature("")
    def on_renewalIdLineEdit_returnPressed(self):
        self.renewalIdLineEdit.releaseKeyboard()
        try:
            text = self.renewalIdLineEdit.text()
            id = int(text[0:RENEWAL_ID_WIDTH])
            if len(text) > RENEWAL_ID_WIDTH:
                assert len(text) == RENEWAL_ID_WIDTH + STRIP_ID_WIDTH
                strip = int(text[RENEWAL_ID_WIDTH:])
            else:
                assert len(text) == RENEWAL_ID_WIDTH
                strip = None
        except:
            ttl = "Invalid Entry"
            msg = "Invalid input for the test ID.  If the barcode cannot be read," + \
            "please type the ID, including all leading zeroes."
            QMessageBox.warning(self, ttl, msg)
            self.renewalIdLineEdit.grabKeyboard()
            return
        
        try:
            renewal = Renewal.objects.get(id=id)
        except:
            ttl = "Not Found"
            msg = "Renewal %d not found." % id
            QMessageBox.warning(self, ttl, msg)
            self.renewalIdLineEdit.grabKeyboard()
            return

        try:
            tests = Test.objects.filter(renewal_id=id).order_by("-test_num")
        except:
            ttl = "Database Error"
            msg = "Could not read Test database."
            QMessageBox.warning(self, ttl, msg)
            self.renewalIdLineEdit.grabKeyboard()
            return

        if self.startingTests:
            self.startTest(id, strip, renewal, tests)
        elif self.enteringResults:
            self.enterResult(id, strip, renewal, tests)

    @pyqtSignature("QDate")
    def on_sterilizeDateEdit_dateChanged(self, q_date):
        if self.startingTests and q_date.toPyDate() != datetime.date.today():
            self.omittedPushButton.setEnabled(False)
        elif self.startingTests:
            self.omittedPushButton.setEnabled(True)
            
    @pyqtSignature("")
    def on_prevDayPushButton_clicked(self):
        date = self.sterilizeDateEdit.date().toPyDate() - datetime.timedelta(days=1)
        self.sterilizeDateEdit.setDate(date)

    @pyqtSignature("")
    def on_nextDayPushButton_clicked(self):
        date = self.sterilizeDateEdit.date().toPyDate() + datetime.timedelta(days=1)
        self.sterilizeDateEdit.setDate(date)

    @pyqtSignature("")
    def on_notifyPushButton_clicked(self):
        self.makeNotifyWindow(self.records[self.recordNum], self.parent().user)

    @pyqtSignature("")
    def on_reportPushButton_clicked(self):
        id = self.renewalIdLineEdit.text()
        dlg = ResultDlg(False, RenewalToSterilizerID(id), self)
        dlg.exec_()

    @pyqtSignature("")
    def on_testResultPushButton_clicked(self):
        if self.testResultPushButton.text() == "":
            self.testResultPushButton.setText("-")
        elif self.testResultPushButton.text() == "-":
            self.testResultPushButton.setText("+")
        else:
            self.testResultPushButton.setText("")

    @pyqtSignature("")
    def on_controlResultPushButton_clicked(self):
        if self.controlResultPushButton.text() == "":
            self.controlResultPushButton.setText("-")
        elif self.controlResultPushButton.text() == "-":
            self.controlResultPushButton.setText("+")
        else:
            self.controlResultPushButton.setText("")

    @pyqtSignature("")
    def on_suppliedPushButton_clicked(self):
        self.insertTest(True)

    @pyqtSignature("")
    def on_omittedPushButton_clicked(self):
        self.insertTest(False)

    @pyqtSignature("")
    def on_savePushButton_clicked(self):
        self.disableEditing()
        if self.enteringResults:
            self.addResultComments()
        success, widget = self.saveRecord(self.getCurrentRecord())
        if not success and not self.enteringResults:
            self.enableEditing()
            if widget:
                widget.setFocus()
        elif not success:
            msg = "Database error:  Error saving results!  If error persists, " + \
            "contact administrator."
            QMessageBox.warning(self, ttl, msg)
        elif self.enteringResults:
            if self.testResultPushButton.text() == "+":
                self.makeNotifyWindow(self.records[self.recordNum], self.parent().user)
            self.enterResults()

    @pyqtSignature("")
    def on_cancelPushButton_clicked(self):
        self.disableEditing()
        if not self.inserting and (self.startingTests or self.enteringResults):
            self.renewalIdLineEdit.releaseKeyboard()
            self.renewalIdLineEdit.setDisabled(True)
        self.inserting = None
        if self.startingTests:
            self.startingTests = False
            self.stopEditStart()
        if self.enteringResults:
            self.enteringResults = False
            self.stopEditResults()
        if self.lastInsert:
            self.lastInsert = False
            self.current_month = datetime.date.today().month
            self.current_year = datetime.date.today().year
            self.loadRecords()
        else:
            self.loadForm(self.records[self.recordNum])

    @pyqtSignature("")
    def on_findPushButton_clicked(self):
        records = Renewal.objects.all()
        findDlg = FindDlg(self.windowTitle(), records, self.findValues, self.findSizes, self)
        id = findDlg.exec_()
        if id:
            bookmark = {
            'dentist': str(RenewalToDentistID(id)).zfill(DENTIST_ID_WIDTH),
            'sterilizer': str(RenewalToSterilizerID(id)).zfill(STERILIZER_ID_WIDTH),
            'renewal': str(id).zfill(RENEWAL_ID_WIDTH),
            }
            self.goToBookmark(bookmark)