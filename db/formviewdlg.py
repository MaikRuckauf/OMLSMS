import thread
from constants import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from finddlg import FindDlg
import printpdf


class MainDlg(QDialog):

    def makeBookmark(self):
        return {}

    def goToBookmark(self, bookmark):
        pass

    def printHTML(self, html, spawn=True, useLabelPrinter=False):
        if html:
            try:
                if spawn:
                    thread.start_new_thread(printpdf.printHTML, (html, useLabelPrinter))
                else:
                    printpdf.printHTML(html, useLabelPrinter)
            except Exception as e:
                QMessageBox.warning(None, "Print Error.", unicode(e))

    def printPDF(self, pdf):
        if pdf:
            try:
                thread.start_new_thread(printpdf.printPDF, (pdf,))
            except Exception as e:
                QMessageBox.warning(None, "Print Error.", unicode(e))

    def viewText(self, text):
        if text:
            try:
                thread.start_new_thread(printpdf.viewText, (text,))
            except Exception as e:
                QMessageBox.warning(None, "View Error.", unicode(e))

    def printText(self, text):
        if text:
            try:
                thread.start_new_thread(printpdf.printText, (text,))
            except Exception as e:
                QMessageBox.warning(None, "Print Error.", unicode(e))

    def _configValues(self):
        return(self.parent().configValues)
    configValues = property(fget=_configValues)


class FormViewDlg(MainDlg):

    def __init__(self, parent=None):
        super(FormViewDlg, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.editing = False
        self.inserting = None
        self.orderedByRecordNumber = True

    def initializeModel(self, bookmark={}):
        self.loadRecords()
        self.goToBookmark(bookmark)

    def loadRecords(self, record_id=None):
        # define for child class
        # load database records into self.records
        self.records = []
        #self.findRecord(record.id)

    def loadForm(self, record):
        # define for child class
        # load data from record to form
        pass
    
    def verifyFormData(self):
        # define for child class
        # verify form data, on error return a widget with data in violation
        return None, None

    def saveForm(self, record, id=None):
        # define for child class
        # save form data to database
        pass

    def prepareNewRecord(self):
        # define for child class
        # return a "blank" new record
        pass
    
    def getTargetInsertId(self, record):
        # define for child class
        # return the ID to assign for record when it is inserted
        return None

    def makeBookmark(self):
        # define for child class
        # return dictionary containing key information about the current record
        return {}

    def goToBookmark(self, bookmark):
        # define for child class
        # set the current record in response to the bookmark (if possible)
        pass

    def reportNotFound(self, search, type, id):
        msg = "Could not find %s for %s: %s" % (search, type, id)
        QMessageBox.warning(self, "Not Found", msg)

    def saveRecord(self, record, id=None):
        widget, message = self.verifyFormData()
        if widget:
            QMessageBox.warning(self, "Data Error", message)
            widget.setFocus()
            return False, widget
        else:
            try:
                self.saveForm(record, id)
                record.save(force_insert=True if self.inserting else False)
            except Exception as e:
                QMessageBox.critical(self, "Save Error", "Could not save to database: %s" % e)
                return False, None
        return True, None

    def getCurrentRecord(self):
        if self.inserting:
            return self.inserting
        else:
            return self.records[self.recordNum]
    
    def setRecordNum(self, value):
        if not self.records or not len(self.records):
            self.recordNum = None
        elif self.records and value >= 0 and value < len(self.records):
            self.recordNum = value
            self.loadForm(self.getCurrentRecord())

    def findRecord(self, id):
        if id and self.orderedByRecordNumber:
            for index, record in enumerate(self.records):
                if record.id >= id:
                    self.setRecordNum(index)
                    return
        elif id:
            for index, record in enumerate(self.records):
                if record.id == id:
                    self.setRecordNum(index)
                    return
        self.setRecordNum(0)

    def decrementRecordNum(self):
        if self.recordNum is not None:
            self.setRecordNum(self.recordNum - 1)

    def incrementRecordNum(self):
        if self.recordNum is not None:
            self.setRecordNum(self.recordNum + 1)

    def disableEditing(self):
        for widget in self.editWidgets:
            widget.setDisabled(True)
        for widget in self.menuWidgets:
            if widget not in self.editFinalizeWidgets:
                widget.setEnabled(True)
            else:
                widget.setDisabled(True)
        self.editing = False
        try:
            self.historyTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        except:
            pass
    
    def enableEditing(self):
        self.editing = True
        for widget in self.editWidgets:
            widget.setEnabled(True)
        for widget in self.menuWidgets:
            if widget in self.editFinalizeWidgets:
                widget.setEnabled(True)
            else:
                widget.setDisabled(True)
        try:
            self.historyTableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        except:
            pass

    def toggleActive(self, id, type, disableMsg, enableMsg):
        msgBox = QMessageBox()
        if not self.inactiveDateIsSet():
            ttl = "Disable %s" % type
            if QMessageBox.question(
                self, ttl, disableMsg, QMessageBox.Yes, QMessageBox.No
            ) == QMessageBox.Yes:
                self.dateInactiveLineEdit.setText(QDate.currentDate().toString("MM/dd/yyyy"))
                success, widget = self.saveRecord(self.getCurrentRecord())
                if success:
                    QMessageBox.information(
                        self, ttl, "%s %s disabled." % (type, id), QMessageBox.Ok
                    )
                self.loadForm(self.getCurrentRecord())
        else:
            ttl = "Enable %s" % type
            if QMessageBox.question(
                self, ttl, enableMsg, QMessageBox.Yes, QMessageBox.No
            ) == QMessageBox.Yes:
                self.dateInactiveLineEdit.clear()
                success, widget = self.saveRecord(self.getCurrentRecord())
                if success:
                    QMessageBox.information(
                        self, ttl, "%s %s enabled." % (type, id), QMessageBox.Ok
                    )
                self.loadForm(self.getCurrentRecord())

    def inactiveDateIsSet(self):
        return (len(self.dateInactiveLineEdit.text()) == 10)

    #@pyqtSignature("")
    def show(self, bookmark={}):
        try:
            self.initializeModel(bookmark)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Data Error", 
                "Could not load database: %s" % e,
                QMessageBox.Ok
            )
        super(FormViewDlg, self).show()

    @pyqtSignature("")
    def on_findPushButton_clicked(self):
        findDlg = FindDlg(self.windowTitle(), self.records, self.findValues, self.findSizes, self)
        if findDlg:
            self.findRecord(findDlg.exec_())
       
    @pyqtSignature("")
    def on_seekFirstPushButton_clicked(self):
        self.setRecordNum(0)

    @pyqtSignature("")
    def on_seekPreviousPushButton_clicked(self):
        self.decrementRecordNum()

    @pyqtSignature("")
    def on_seekNextPushButton_clicked(self):
        self.incrementRecordNum()

    @pyqtSignature("")
    def on_seekLastPushButton_clicked(self):
        if self.records:
            self.setRecordNum(len(self.records) - 1)

    @pyqtSignature("")
    def on_insertPushButton_clicked(self):
        self.inserting = self.prepareNewRecord()
        if self.inserting:
            self.loadForm(self.inserting)
            self.enableEditing()

    @pyqtSignature("")
    def on_modifyPushButton_clicked(self):
        self.enableEditing()

    @pyqtSignature("")
    def on_savePushButton_clicked(self):
        self.disableEditing()
        if self.inserting:
            id = self.getTargetInsertId(self.inserting)
        else:
            id = None
        success, widget = self.saveRecord(self.getCurrentRecord(), id)
        if not success:
            self.enableEditing()
            if widget:
                widget.setFocus()
        elif self.inserting:
            self.inserting = None
            self.loadRecords(id)

    @pyqtSignature("")
    def on_cancelPushButton_clicked(self):
        self.disableEditing()
        self.inserting = None
        self.loadRecords(self.getCurrentRecord().id)

class FormViewPartialLoadDlg(FormViewDlg):

    def __init__(self, parent=None):
        super(FormViewPartialLoadDlg, self).__init__(parent)

    def loadRecords(self, record_id=None):
        # partial load records by date to improve initial response time
        if record_id:
            self.findRecord(record_id, None)
        self.loadPartialRecords()
        while len(self.records) == 0 \
        and self.getDateRange()[0].year >= DATABASE_START_DATE.year:
            self.decrementDateRange()
            #self.loadPartialRecords()
        while len(self.records) == 0 \
        and self.getDateRange()[0].year <= DATABASE_STOP_DATE.year:
            self.incrementDateRange()
            #self.loadPartialRecords()
        if not record_id:
            self.setRecordNum(len(self.records) - 1)

    #
    # Redefine seek buttons to handle partial loading by month
    #

    @pyqtSignature("")
    def on_seekFirstPushButton_clicked(self):
        if self.recordNum > 0:
            self.setRecordNum(0)
        else:
            if self.decrementDateRange():
                self.setRecordNum(0)
            else:
                self.incrementDateRange()

    @pyqtSignature("")
    def on_seekPreviousPushButton_clicked(self):
        if self.recordNum > 0:
            self.decrementRecordNum()
        else:
            if self.decrementDateRange():
                self.setRecordNum(len(self.records) - 1)
            else:
                self.incrementDateRange()

    @pyqtSignature("")
    def on_seekNextPushButton_clicked(self):
        if self.records and self.recordNum < len(self.records) - 1:
            self.incrementRecordNum()
        else:
            if self.incrementDateRange():
                self.setRecordNum(0)
            else:
                self.decrementDateRange()

    @pyqtSignature("")
    def on_seekLastPushButton_clicked(self):
        if self.incrementDateRange():
            self.setRecordNum(0)
        else:
            self.decrementDateRange()
            self.setRecordNum(len(self.records) - 1)

    def getDateRange(self):
        return DateRangeForMonth(self.current_year, self.current_month)
    
    def decrementDateRange(self):
        month = self.current_month
        year = self.current_year
        if self.current_month > 1:
            self.current_month = self.current_month - 1
        else:
            self.current_year = self.current_year - 1
            self.current_month = 12
        self.loadPartialRecords()
        return self.records
    
    def incrementDateRange(self):
        month = self.current_month
        year = self.current_year
        if self.current_month < 12:
            self.current_month = self.current_month + 1
        else:
            self.current_year = self.current_year + 1
            self.current_month = 1
        self.loadPartialRecords()
        return self.records

    def findDatedRecord(self, id, date):
        if (date.month != self.current_month or date.year != self.current_year):
            self.current_month = date.month
            self.current_year = date.year
            self.loadPartialRecords()
        for index, record in enumerate(self.records):
            if record.id == id:
                self.setRecordNum(index)
                return
        self.setRecordNum(0)

    def findRecord(self, id, record=None):
        if id:
            record_date = self.getRecordDate(id)
            return self.findDatedRecord(id, record_date)

    @pyqtSignature("")
    def on_findPushButton_clicked(self):
        findDlg = FindDlg(self.windowTitle(), self.allRecords, self.findValues, self.findSizes, self)
        if findDlg:
            self.findRecord(findDlg.exec_())
