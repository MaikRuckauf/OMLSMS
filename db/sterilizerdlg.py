import sys, re
from constants import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import ui
from formviewdlg import FormViewDlg
from finddlg import FindDlg
from printlabeldlg import PrintLabelDlg

sys.path.append(OMLWEB_PATH)
from omlweb.models import Dentist, Sterilizer, SterilizerMethod
from django.db.models import Max
from printlabeldlg import PrintLabelDlg
import djprint
from result import ResultDlg


class SterilizerDlg(FormViewDlg, ui.Ui_sterilizerDlg):

    def __init__(self, parent=None):
        super(SterilizerDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("SMS Sterilizer")

        self.editWidgets = [self.enrollDateEdit, self.numTestsSpinBox,
        self.renewalTestSpinBox, self.renewalFeeSpinBox, self.serialNumLineEdit,
        self.modelLineEdit, self.methodComboBox, self.commentLineEdit,
        self.suspendRenewalsCheckBox]
        
        self.menuWidgets = [self.findPushButton, self.seekFirstPushButton,
        self.seekNextPushButton, self.seekPreviousPushButton, self.seekLastPushButton,
        self.insertPushButton, self.modifyPushButton, self.savePushButton,
        self.cancelPushButton, self.labelPushButton, self.billPushButton, self.reportPushButton,
        self.timeToRenewCheckBox, self.suspendRenewalsCheckBox, self.dateInactivePushButton]
        
        self.editFinalizeWidgets = [self.savePushButton, self.cancelPushButton]
        
        self.findValues = ["id", "enroll_date", "comment"]
        self.findSizes = {
        'field_widths': [100, 200, 250],
        'window_height': 400,
        'window_width': 600,
        'zfill': [STERILIZER_ID_WIDTH, None, None, None, None],
        }
        self.disableEditing()

    def initializeModel(self, bookmark):
        if not self.methodComboBox.count():
            methods = SterilizerMethod.objects.filter(active=True).order_by("id")
            for method in methods:
                self.methodComboBox.insertItem(method.id, method.name)
        self.loadRecords()
        self.goToBookmark(bookmark)
    
    def loadRecords(self, record_id=None):
        self.records = Sterilizer.objects.all().order_by("id")
        if record_id:
            self.findRecord(record_id)

    def loadForm(self, record):
        try:
            dentist = record.dentist
            self.setWindowTitle("SMS Sterilizer - " + dentist.getFullName())
        except:
            self.setWindowTitle("SMS Sterilizer - " + "( Error retrieving dentist )")
            dentist = None
        self.idLineEdit.setText(
            str(record.id).zfill(STERILIZER_ID_WIDTH) if record.id else ""
        )
        self.enrollDateEdit.setDate(record.enroll_date)
        self.numTestsSpinBox.setValue(record.num_tests)
        self.renewalTestSpinBox.setValue(record.renew_test)
        self.renewalFeeSpinBox.setValue(record.renew_fee)
        self.serialNumLineEdit.setText(record.serial_num)
        self.modelLineEdit.setText(record.model)
        self.methodComboBox.setCurrentIndex(record.method.id - 1)
        #self.monthlyReportLineEdit.setText(RecordDateToText(record.last_report_date))
        #self.yearlyReportLineEdit.setText(RecordDateToText(record.last_certificate_date))
        if record.inactive_date:
            self.dateInactiveLineEdit.setText(RecordDateToText(record.inactive_date))
        else:
            try:
                value = RecordDateToText(dentist.inactive_date)
                if value:
                    self.dateInactiveLineEdit.setText("(" + value + ")")
                else:
                    self.dateInactiveLineEdit.setText("")
            except:
                self.dateInactiveLineEdit.setText("(Data Error)")
        self.commentLineEdit.setText(record.comment)
        self.timeToRenewCheckBox.setChecked(record.renew)
        self.suspendRenewalsCheckBox.setChecked(record.suspend)
    
    def verifyFormData(self):
        if self.idLineEdit.text() != "" and \
                not re.match("^\d{%s}$" % STERILIZER_ID_WIDTH, self.idLineEdit.text()):
            return self.idLineEdit, "Sterilizer ID has improper format."
        enroll_date = self.enrollDateEdit.date().toPyDate()
        if enroll_date.year < 1980:
            return self.enrollDateEdit, "Invalid enroll date."
        try:
            SterilizerMethod.objects.get(id=self.methodComboBox.currentIndex() + 1)
        except:
            return self.methodComboBox, "Can't access Sterilizer Method from database."
        if self.dateInactiveLineEdit.text() != "":
            try:
                if not re.match("$\(", self.dateInactiveLineEdit.text()):
                    inactive = FormDateToRecord(self.dateInactiveLineEdit.text())
                    assert inactive >= enroll_date
            except:
                return self.dateInactiveLineEdit, "Invalid inactive date."
        return None, None

    def saveForm(self, record, id=None):
        assert record.id == int(self.idLineEdit.text())
        record.enroll_date = self.enrollDateEdit.date().toPyDate()
        record.num_tests = self.numTestsSpinBox.value()
        record.renew_test = self.renewalTestSpinBox.value()
        record.renew_fee = self.renewalFeeSpinBox.value()
        record.serial_num = self.serialNumLineEdit.text()
        record.model = self.modelLineEdit.text()
        record.method = SterilizerMethod.objects.get(id=self.methodComboBox.currentIndex() + 1)
        if not re.match("$\(", self.dateInactiveLineEdit.text()):
            record.inactive_date = \
                FormDateToRecord(self.dateInactiveLineEdit.text())
        record.comment = self.commentLineEdit.text()
        record.renew = self.timeToRenewCheckBox.isChecked()
        record.suspend = self.suspendRenewalsCheckBox.isChecked()

    def prepareNewRecord(self):
        self.dentistForInsert = self.selectDentistForInsert()
        try:
            method = SterilizerMethod.objects.get(id=DEFAULT_STERILIZER_METHOD)
            dentist = Dentist.objects.get(id=self.dentistForInsert)
        except:
            return None
        dentist_factor = 10 ** (STERILIZER_ID_WIDTH - DENTIST_ID_WIDTH)
        target_id = self.getTargetInsertId(None)
        return Sterilizer(
        id = target_id,
        dentist = dentist,
        sterilizer = target_id % dentist_factor,
        enroll_date = datetime.date.today(),
        num_tests = DEFAULT_NUM_TESTS,
        renew_test = DEFAULT_RENEWAL_TEST,
        renew_fee = DEFAULT_RENEWAL_FEE,
        method = method,
        renew = True,
        suspend = False,
        )
    
    def getTargetInsertId(self, record):
        try:
            dentist_factor = 10 ** (STERILIZER_ID_WIDTH - DENTIST_ID_WIDTH)
            id_lower = self.dentistForInsert * dentist_factor
            id_upper = id_lower + dentist_factor
            value = Sterilizer.objects.filter(id__gt=id_lower).filter(id__lt=id_upper)
            if len(value):
                value = value.aggregate(Max('id'))['id__max'] + 1
            else:
                value = id_lower + 1
            # Limited to 99 sterilizers per dentist by convention!!
            # if we overflow, at least don't corrupt the database
            assert value / dentist_factor == self.dentistForInsert
        except:
            return None
        return value

    def makeBookmark(self):
        if re.match("^\d{%s}$" % STERILIZER_ID_WIDTH, self.idLineEdit.text()):
            return {
            'dentist': self.idLineEdit.text()[0:DENTIST_ID_WIDTH],
            'sterilizer': self.idLineEdit.text()
            }
        return {}

    def goToBookmark(self, bookmark):
        dentist_factor = 10 ** (STERILIZER_ID_WIDTH - DENTIST_ID_WIDTH)
        if 'sterilizer' in bookmark and \
        bookmark['sterilizer'][0:DENTIST_ID_WIDTH] == bookmark['dentist']:
            self.findRecord(int(bookmark['sterilizer']))
        elif 'dentist' in bookmark:
            self.findRecord(int(bookmark['dentist']) * dentist_factor)
        else:
            self.findRecord(None)

    def selectDentistForInsert(self):
        findDlg = FindDlg(
        "Dentist",
        Dentist.objects.filter(inactive_date__isnull=True),
        ["id", "practice_name", "lname", "fname"],
        {
        'field_widths': [50, 250, 160, 90],
        'window_height': 400,
        'window_width': 600,
        'zfill': [DENTIST_ID_WIDTH, None, None, None]
        },
        self
        )
        return (findDlg.exec_())

    @pyqtSignature("")
    def on_dateInactivePushButton_clicked(self):
        #msgBox = QMessageBox()
        id = self.idLineEdit.text()
        type = "Sterilizer"
        disableMsg = "Disabling this sterilizer will disable all associated " + \
            "renewals.  Proceed?"
        enableMsg = "Enabling this sterilizer will enable all associated " + \
            "renewals that were not individually disabled.  Proceed?"
        self.toggleActive(id, type, disableMsg, enableMsg)
    
    @pyqtSignature("")
    def on_timeToRenewCheckBox_clicked(self):
        success, widget = self.saveRecord(self.getCurrentRecord())
        self.loadForm(self.getCurrentRecord())

    @pyqtSignature("")
    def on_suspendRenewalsCheckBox_clicked(self):
        success, widget = self.saveRecord(self.getCurrentRecord())
        self.loadForm(self.getCurrentRecord())
    
    #@pyqtSignature("")
    #def on_renewalTimePushButton_clicked(self):
    #    if self.renewalLineEdit.text() == 'yes':
    #        self.renewalLineEdit.setText('no')
    #    else:
    #        self.renewalLineEdit.setText('yes')
    #    success, widget = self.saveRecord(self.getCurrentRecord())
    #    self.loadForm(self.getCurrentRecord())

    @pyqtSignature("")
    def on_labelPushButton_clicked(self):
        labelDlg = PrintLabelDlg(self)
        labelDlg.exec_()

    @pyqtSignature("")
    def on_billPushButton_clicked(self):
        self.printHTML(djprint.getBillForSterilizer(self.getCurrentRecord().id))
        
    @pyqtSignature("")
    def on_reportPushButton_clicked(self):
        id = self.idLineEdit.text()
        dlg = ResultDlg(False, id, self)
        dlg.exec_()
