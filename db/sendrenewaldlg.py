import sys, re, datetime
from constants import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import ui
from formviewdlg import FormViewPartialLoadDlg
from printlabeldlg import PrintLabelDlg

from omlweb.models import Renewal, Sterilizer, Dentist, Lot, Test
import djprint
import reportdlg

NUM_TABLE_COLUMNS = 4

class StartRenewalDlg(QDialog, ui.Ui_startRenewalDlg):

    def __init__(self, parent=None):
        super(StartRenewalDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Start Renewals")
        
        self.error_initializing = False
        self.lot = None
        self.statusLabel.setText("")
        
        if not self.initializeSterilizers():
            return
        self.initializeSterilizerTable()
        if not self.initializeLots():
            return

    def initializeSterilizers(self):
        # some code duplicated in overdue report
        try:
            sterilizers = Sterilizer.objects.filter(renew=True)
            sterilizers = sterilizers.filter(inactive_date__isnull=True)
            sterilizers = sterilizers.filter(suspend=False)
            sterilizers = sterilizers.filter(dentist__inactive_date__isnull=True)
            self.numberNeedingRenewalLineEdit.setText(str(len(sterilizers)))
        except:
            QMessageBox.information(self, "Database Error", "Error reading database.")
            self.error_initializing = True

        try:
            assert len(sterilizers) != 0
        except:
            QMessageBox.information(self, "No Renewals", "No sterilizers are in need of renewal.")
            self.error_initializing = True
            return False
        
        try:
            renewals = Renewal.objects.filter(sterilizer__in=sterilizers)
            latest_renewal = {}
            latest_lot = {}
            for renewal in renewals:
                sterilizer_id = RenewalToSterilizerID(renewal.id)
                if not (sterilizer_id in latest_renewal) or \
                latest_lot[sterilizer_id] < RenewalToLotID(renewal.id):
                    latest_lot[sterilizer_id] = RenewalToLotID(renewal.id)
                    if not renewal.inactive_date:
                        latest_renewal[sterilizer_id] = renewal
            latest_renewals = [renewal for key, renewal in latest_renewal.iteritems()]
            tests = Test.objects.filter(renewal_id__in=latest_renewals)
            latest_test = {}
            for test in tests:
                sterilizer_id = RenewalToSterilizerID(test.renewal_id)
                if not (sterilizer_id in latest_test) or \
                    (latest_test[sterilizer_id].renewal_id < test.renewal_id) or \
                    (latest_test[sterilizer_id].renewal_id == test.renewal_id and \
                    latest_test[sterilizer_id].test_num < test.test_num):
                    latest_test[sterilizer_id] = test
            self.sterilizerList = []
            for sterilizer in sterilizers:
                renewal = latest_renewal[sterilizer.id] if sterilizer.id in latest_renewal else None
                test = latest_test[sterilizer.id] if sterilizer.id in latest_test else None
                if renewal:
                    numTests = max(0, renewal.num_tests - (test.test_num if test else 0))
                else:
                    numTests = 0
                self.sterilizerList.append((
                    sterilizer,
                    sterilizer.num_tests,
                    latest_lot[sterilizer.id] if renewal else 0,
                    numTests))
            self.sterilizerList.sort(key=lambda tup: tup[3])
        except:
            self.error_initializing = True
            return False
        return True
    
    def initializeSterilizerTable(self):
        self.tableWidget.setColumnCount(NUM_TABLE_COLUMNS)
        labels = ["sterlizer", "last renewal", "strips", "tests remaining"]
        widths = [         80,             80,               80,                80]
        self.tableWidget.setHorizontalHeaderLabels(labels)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget.setSelectionMode(QTableView.ExtendedSelection)
        
        for column, width in enumerate(widths):
            self.tableWidget.setColumnWidth(column, width)
        self.tableWidget.setRowCount(len(self.sterilizerList))
        row = 0
        for sterilizer, num, lot, left in self.sterilizerList:
            text = [
            str(sterilizer.id).zfill(STERILIZER_ID_WIDTH),
            str(lot),
            str(num),
            str(left),
            ]
            for column in range(0, len(text)):
                    item = QTableWidgetItem(text[column])
                    #item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row, column, item)
            row += 1
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.selectAll()

    def initializeLots(self):
        today = datetime.date.today()
        try:
            self.lotList = Lot.objects.filter(inactive_date__isnull=True)
            self.lotList = self.lotList.filter(expiration_date__gte=today)
            self.lotList = self.lotList.order_by('-id')
            self.lot = self.lotList[0]
        except:
            QMessageBox.information(self, "Database Error", "Error reading database.")
            self.error_initializing = True

        try:
            assert len(self.lotList) != 0
        except:
            QMessageBox.warning(self, "No Lots", "No valid lots found for renewal.")
            self.error_initializing = True
            return False
        
        for number, lot in enumerate(self.lotList):
            self.lotComboBox.insertItem(number, str(lot.id))
        self.lotComboBox.setCurrentIndex(0)
        return True

    def updateCounts(self):
        count = 0
        strips = 0
        for row in range(0, len(self.sterilizerList)):
            if self.tableWidget.item(row, 0).isSelected():
                count += 1
                strips += self.sterilizerList[row][1]
        self.renewalsSelectedLineEdit.setText(str(count))
        self.stripsRequiredLineEdit.setText(str(int(strips/DEFAULT_NUM_TESTS)))
    
    def selectLot(self, index):
        for row in range(0, len(self.sterilizerList)):
            if self.lotList[index].id <= self.sterilizerList[row][2]:
                for col in range(0, NUM_TABLE_COLUMNS):
                    self.tableWidget.item(row, col).setFlags(Qt.NoItemFlags)
                    text = self.tableWidget.item(row, col).text()
                    if text and text[0] != '(':
                        self.tableWidget.item(row, col).setText('(' + text + ')')
            else:
                for col in range(0, NUM_TABLE_COLUMNS):
                    self.tableWidget.item(row, col).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    text = self.tableWidget.item(row, col).text()
                    if text and text[0] == '(':
                        self.tableWidget.item(row, col).setText(text[1:-1])
        self.updateCounts()

    def selectNumRenewals(self, num):
        i = 0
        index = self.lotComboBox.currentIndex()
        for row in range(0, len(self.sterilizerList)):
            if self.lotList[index].id > self.sterilizerList[row][2]:
                i += 1
                for col in range(0, NUM_TABLE_COLUMNS):
                    self.tableWidget.item(row,col).setSelected(True)
            if i >= num:
                break

    def selectNumStrips(self, num):
        i = 0
        index = self.lotComboBox.currentIndex()
        for row in range(0, len(self.sterilizerList)):
            if self.lotList[index].id > self.sterilizerList[row][2]:
                print row, i, int(self.sterilizerList[row][0].num_tests/DEFAULT_NUM_TESTS), num
                if i + int(self.sterilizerList[row][0].num_tests/DEFAULT_NUM_TESTS) <= num:
                    i += int(self.sterilizerList[row][0].num_tests/DEFAULT_NUM_TESTS)
                    for col in range(0, NUM_TABLE_COLUMNS):
                        self.tableWidget.item(row,col).setSelected(True)
            if i == num:
                break
        
    def startRenewal(self, sterilizers):
        lot = self.lotList[self.lotComboBox.currentIndex()]

        '''
        dentist_ids = []
        dentists = []
        for sterilizer in sterilizers:
            id = SterilizerToDentistID(sterilizer.id)
            dentist_ids.append(id)
        
        dentistList = Dentist.objects.filter(id__in=dentist_ids)
        
        for id in dentist_ids:
            for dentist in dentistList:
                if id == dentist.id:
                    dentists.append(dentist)
        '''
        
        sortList = [(SterilizerToDentistID(x.id), x) for x in sterilizers]
        sortList.sort()
        list = []
        last_id = SterilizerToDentistID(sortList[0][0])
        list = [sortList[0][1]]
        for id, sterilizer in sortList[1:]:
            if last_id != id:
                list.append(None)
                last_id = id
            list.append(sterilizer)
        names = reportdlg.getDentistNames(list, False)
            
        self.parent().viewText(djprint.printRenewalsStarted(list, names))
        
        # have to do one at a time due to the current barcode printer limitations
        for sterilizer in list:
            if sterilizer:
                dentist = sterilizer.dentist
                self.parent().printHTML(djprint.getRenewalLabelsForSterilizers([sterilizer], [dentist], lot), spawn=False, useLabelPrinter=True)

    @pyqtSignature("")
    def on_sendPushButton_clicked(self):
        self.statusLabel.setText("Printing Renewals")
        # Process events so user sees status update
        QCoreApplication.instance().processEvents()
        sterilizers = []
        for row, data in enumerate(self.sterilizerList):
            if self.tableWidget.item(row, 0).isSelected():
                sterilizers.append(data[0])
        self.startRenewal(sterilizers)

    @pyqtSignature("")
    def on_tableWidget_itemSelectionChanged(self):
        self.updateCounts()

    @pyqtSignature("")
    def on_cancelPushButton_clicked(self):
        self.close()
        
    @pyqtSignature("int")
    def on_lotComboBox_currentIndexChanged(self, index):
        self.selectLot(index)

    @pyqtSignature("")
    def on_renewalsSelectedLineEdit_editingFinished(self):
        try:
            num = int(self.renewalsSelectedLineEdit.text())
            assert num > 0
            self.tableWidget.clearSelection()
        except:
            pass
        else:
            self.selectNumRenewals(num)
        finally:
            self.tableWidget.setFocus()
            self.updateCounts()

    @pyqtSignature("")
    def on_stripsRequiredLineEdit_editingFinished(self):
        try:
            num = int(self.stripsRequiredLineEdit.text())
            assert num > 0
            self.tableWidget.clearSelection()
        except:
            print "error"
            pass
        else:
            self.selectNumStrips(num)
        finally:
            self.tableWidget.setFocus()
            self.updateCounts()
    
    def selectSterilizer(self):
        findDlg = FindDlg(
        "Sterilizer",
        self.sterilizerList,
        ["id", "enroll_date"],
        {
        'field_widths': [250, 200],
        'window_height': 400,
        'window_width': 600
        },
        self
        )
        return (findDlg.exec_())


class SendRenewalDlg(QDialog, ui.Ui_sendRenewalDlg):

    def __init__(self, parent=None):
        super(SendRenewalDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Send Renewal")
        
        self.statusLabel.setText("Enter or Scan Renewal Number")
        self.numRenewalsLineEdit.setText("0")
        self.printMailingLabelsPushButton.setAutoDefault(False)
        self.printReportsPushButton.setAutoDefault(False)
        self.exitPushButton.setAutoDefault(False)
        self.renewalIdLineEdit.grabKeyboard()
        self.renewals = []

        self.printMailingLabelsPushButton.setDisabled(True)
        self.printReportsPushButton.setDisabled(True)
        self.mailingLabelsPrinted = False
        self.reportsPrinted = False

        self.error_initializing = False
        self.sterilizers = {}
        self.lots = {}
        today = datetime.date.today()
        try:
            sterilizers = Sterilizer.objects.filter(renew=True)
            sterilizers = sterilizers.filter(inactive_date__isnull=True)
            sterilizers = sterilizers.filter(dentist__inactive_date__isnull=True)
            
            for sterilizer in sterilizers:
                self.sterilizers[sterilizer.id] = sterilizer
            
            lots = Lot.objects.filter(inactive_date__isnull=True)
            lots = lots.filter(expiration_date__gte=today)
            
            for lot in lots:
                self.lots[lot.id] = lot

        except:
            self.error_initializing = True

    def createRenewal(self, sterilizer, lot):
        renewal = Renewal()
        renewal.id = int(str(sterilizer.id) + str(lot.id))
        renewal.sterilizer = sterilizer
        renewal.lot = lot.name
        renewal.renewal_date = datetime.date.today()
        renewal.num_tests = sterilizer.num_tests
        renewal.renewal_fee = sterilizer.renew_fee
        renewal.late_fee = 0
        renewal.payment_date = None
        renewal.payement_amount = None
        renewal.check_num = ""
        renewal.comment = ""
        renewal.inactive_date = None
        return renewal

    def insertIntoDatabase(self, renewal):
        renewal.save(force_insert=True)
        sterilizer = renewal.sterilizer
        sterilizer.renew = False
        sterilizer.save()

    def getSterilizers(self):
        # get sterilizers in same order as self.renewals with one database access
        sterilizer_ids = []
        for renewal in self.renewals:
            sterilizer_ids.append(RenewalToSterilizerID(renewal.id))
        sterilizers = Sterilizer.objects.filter(id__in=sterilizer_ids)
        lookup = {}
        for sterilizer in sterilizers:
            lookup[sterilizer.id] = sterilizer
        list = []
        for renewal in self.renewals:
            list.append(lookup[RenewalToSterilizerID(renewal.id)])
        return list
        
    def getDentists(self):
        dentist_ids = []
        for renewal in self.renewals:
            dentist_ids.append(RenewalToDentistID(renewal.id))
        list = Dentist.objects.filter(id__in=dentist_ids)
        return list
    
    def printBill(self, renewal):
        id = RenewalToSterilizerID(renewal.id)
        self.parent().printHTML(djprint.getBillForSterilizer(id))

    def printMailingLabels(self):
        dentists = self.getDentists()
        labelDlg = PrintLabelDlg(self.parent(), dentists)
        labelDlg.exec_()

    def printReports(self):
        sterilizers = self.getSterilizers()
        for sterilizer in sterilizers:
            self.parent().printHTML(djprint.getReportForSterilizer(sterilizer.id), spawn=False)

    @pyqtSignature("")
    def on_renewalIdLineEdit_returnPressed(self):
        text = self.renewalIdLineEdit.text()
        status_text = "Error: Could not add renewal #%s." % text
        try:
            try:
                assert len(text) >= RENEWAL_ID_WIDTH
                assert len(text) <= RENEWAL_ID_WIDTH + STRIP_ID_WIDTH
                if len(text) > RENEWAL_ID_WIDTH:
                    text = text[0:RENEWAL_ID_WIDTH]
                id = int(text)
                sterilizer_id = RenewalToSterilizerID(id)
                lot_id = RenewalToLotID(id)
            except:
                status_text = "Improper ID entered."
                assert False
            
            try:
                lot = self.lots[RenewalToLotID(id)]
            except:
                status_text = "Can't use lot number %d." % lot_id
                assert False
            
            try:
                assert not Renewal.objects.filter(id=id)
            except:
                status_text = "Renewal %s already in database." % str(id).zfill(RENEWAL_ID_WIDTH)
                assert False

            try:
                sterilizer = self.sterilizers[RenewalToSterilizerID(id)] 
            except:
                status_text = "Sterilizer %s not up for renewal." % str(sterilizer_id).zfill(STERILIZER_ID_WIDTH)
                assert False

            for renewal in self.renewals:
                if renewal.id == id:
                    status_text = "Renewal %s already added." % str(id).zfill(RENEWAL_ID_WIDTH)
                    assert False
                if RenewalToSterilizerID(renewal.id) == RenewalToSterilizerID(id):
                    status_text = "Renewal for sterilizer %s already added." % str(sterilizer_id).zfill(STERILIZER_ID_WIDTH)
                    assert False
            
            renewal = self.createRenewal(sterilizer, lot)
            self.insertIntoDatabase(renewal)
            self.renewals.append(renewal)
            self.printBill(renewal)
            status_text = "Renewal %s added" % text
            self.printMailingLabelsPushButton.setEnabled(True)
            self.printReportsPushButton.setEnabled(True)
        except:
            QApplication.beep()
        finally:
            self.numRenewalsLineEdit.setText(str(len(self.renewals)))
            self.statusLabel.setText(status_text)
            self.renewalIdLineEdit.setText("")
            self.renewalIdLineEdit.setFocus()

    @pyqtSignature("")
    def on_printMailingLabelsPushButton_clicked(self):
        self.renewalIdLineEdit.releaseKeyboard()
        self.renewalIdLineEdit.setText("")
        self.renewalIdLineEdit.setDisabled(True)
        if self.mailingLabelsPrinted:
            msgBox = QMessageBox()
            ttl = "Already Printed"
            msg = "Mailing labels for the dentist offices have already been" + \
                " sent to the printer.  Do you wish to attempt to send another" + \
                " copy to the printer?"
            if QMessageBox.question(
                self, ttl, msg, QMessageBox.Yes, QMessageBox.No
            ) == QMessageBox.No:
                return

        self.printMailingLabels()
        self.mailingLabelsPrinted = True

    @pyqtSignature("")
    def on_printReportsPushButton_clicked(self):
        self.renewalIdLineEdit.releaseKeyboard()
        self.renewalIdLineEdit.setText("")
        self.renewalIdLineEdit.setDisabled(True)
        if self.reportsPrinted:
            msgBox = QMessageBox()
            ttl = "Already Printed"
            msg = "Reports for the corresponding sterilizers have already been" + \
                " sent to the printer.  Do you wish to attempt to send another" + \
                " copy to the printer?"
            if QMessageBox.question(
                self, ttl, msg, QMessageBox.Yes, QMessageBox.No
            ) == QMessageBox.No:
                return

        self.printReports()
        self.reportsPrinted = True

    @pyqtSignature("")
    def on_exitPushButton_clicked(self):
        self.close()

    def keyPressEvent(self, event):
        if not event.key() == Qt.Key_Escape:
            super(SendRenewalDlg, self).keyPressEvent(event)
        else:
            self.close()

    def close(self):
        self.renewalIdLineEdit.releaseKeyboard()
        self.renewalIdLineEdit.setDisabled(True)
        close = True
        if self.renewals and not self.mailingLabelsPrinted:
            msgBox = QMessageBox()
            ttl = "Mailing Labels Not Printed"
            msg = "Mailing labels for the dentist offices have not been" + \
                " sent to the printer.  Do you wish exit anyway?"
            if QMessageBox.question(
                self, ttl, msg, QMessageBox.Yes, QMessageBox.No
            ) == QMessageBox.No:
                close = False
        elif self.renewals and not self.reportsPrinted:
            msgBox = QMessageBox()
            ttl = "Reports Not Printed"
            msg = "Reports for the corresponding sterilizers have not been" + \
                " sent to the printer.  Do you wish exit anyway?"
            if QMessageBox.question(
                self, ttl, msg, QMessageBox.Yes, QMessageBox.No
            ) == QMessageBox.No:
                close = False
        if close:
            super(SendRenewalDlg, self).close()
        elif not self.mailingLabelsPrinted and not self.reportsPrinted:
            self.renewalIdLineEdit.setEnabled(True)
            self.renewalIdLineEdit.grabKeyboard()
            self.renewalIdLineEdit.setFocus()