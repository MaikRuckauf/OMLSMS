import sys, re, datetime
from constants import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
import ui
from finddlg import FindDlg
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QTreeWidgetItem

from omlweb.models import Dentist, Sterilizer
import djprint

class PrintLabelDlg(QDialog, ui.Ui_printLabelDlg):

    def __init__(self, parent=None, dentists=None):
        super(PrintLabelDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowTitleHint)
        self.setWindowTitle("Print Sterilizer Labels")
        
        self.treeWidget.setHeaderLabels(["Labels"])
        self.dentists = {}
        self.sterilizers = {}
        if dentists:
            self.initializeDentists(dentists)
        else:
            self.printDentistsPushButton.setDisabled(True)
        self.printSterilizersPushButton.setDisabled(True)
    
    def initializeDentists(self, dentists):
        for dentist in dentists:
            text = "%s - %s %s %s" % (
                   str(dentist.id).zfill(DENTIST_ID_WIDTH),
                   dentist.title,
                   dentist.fname,            
                   dentist.lname)
            item = QTreeWidgetItem(None, [text])
            self.treeWidget.addTopLevelItem(item)
            self.dentists[dentist.id] = (dentist, True, item)

    def addDentist(self, dentist_id, printLabel=True):
        if not dentist_id in self.dentists:
            dentist = Dentist.objects.get(id=dentist_id)
            text = "%s - %s %s %s" % (
                   str(dentist.id).zfill(DENTIST_ID_WIDTH),
                   dentist.title,
                   dentist.fname,
                   dentist.lname)
            item = QTreeWidgetItem(None, [text])
            if not printLabel:
                item.setTextColor(0, Qt.gray)
            self.treeWidget.addTopLevelItem(item)
            self.treeWidget.expandItem(item)
            self.dentists[dentist_id] = (dentist, printLabel, item)
        elif printLabel and not self.dentists[dentist_id][1]:
            dentist = self.dentists[dentist_id][0]
            item = self.dentists[dentist_id][2]
            item.setTextColor(0, Qt.black)
            self.dentists[dentist_id] = (dentist, printLabel, item)
        if printLabel:
            self.printDentistsPushButton.setEnabled(True)
    
    def addSterilizer(self, sterilizer_id):
        if not sterilizer_id in self.sterilizers:
            sterilizer = Sterilizer.objects.get(id=sterilizer_id)
            text = "%s - %s" % (
                str(sterilizer.id).zfill(STERILIZER_ID_WIDTH),
                sterilizer.comment)
            dentist_id = \
               int(str(sterilizer_id).zfill(STERILIZER_ID_WIDTH)[0:DENTIST_ID_WIDTH])
            if dentist_id in self.dentists:
                parent = self.dentists[dentist_id][2]
            else:
                self.addDentist(dentist_id, False)
                parent = self.dentists[dentist_id][2]
            item = QTreeWidgetItem(parent, [text])
            self.sterilizers[sterilizer_id] = (sterilizer)
        self.printSterilizersPushButton.setEnabled(True)
        
    #@pyqtSlot("")
    def on_addDentistPushButton_clicked(self):
        dentist_id = self.selectDentist()
        if dentist_id:
            self.addDentist(dentist_id)

    #@pyqtSlot("")
    def on_addSterilizerPushButton_clicked(self):
        sterilizer_id = self.selectSterilizer()
        if sterilizer_id:
            self.addSterilizer(sterilizer_id)

    #@pyqtSlot("")
    def on_addByDentistPushButton_clicked(self):
        dentist_id = self.selectDentist()
        if dentist_id:
            self.addDentist(dentist_id, False)
            start,stop = GetSterilizerIDRange(dentist_id)
            sterilizers = \
                Sterilizer.objects.filter(id__range=(start,stop)).filter(inactive_date__isnull=True)
            for sterilizer in sterilizers:
                        self.addSterilizer(sterilizer.id)

    #@pyqtSlot("")
    def on_addOfficePushButton_clicked(self):
        dentist_id = self.selectDentist()
        if dentist_id:
            self.addDentist(dentist_id)
            start,stop = GetSterilizerIDRange(dentist_id)
            sterilizers = \
                Sterilizer.objects.filter(id__range=(start,stop)).filter(inactive_date__isnull=True)
            for sterilizer in sterilizers:
                self.addSterilizer(sterilizer.id)

    #@pyqtSlot("")
    def on_printDentistsPushButton_clicked(self):
        skip = 10*(self.columnSpinBox.value()-1) + (self.rowSpinBox.value()-1)
        labelList = []
        for entry in sorted(self.dentists.items()):
            if entry[1][1]:
                labelList.append(entry[1][0])
        self.parent().printHTML(djprint.printDentistLabelSheet(labelList, skip))

    #@pyqtSlot("")
    def on_printSterilizersPushButton_clicked(self):
        skip = 10*(self.columnSpinBox.value()-1) + (self.rowSpinBox.value()-1)
        sterilizers = []
        dentists = []
        for entry in sorted(self.sterilizers.items()):
            sterilizers.append(entry[1])
            dentists.append(self.dentists[SterilizerToDentistID(entry[1].id)][0])
        self.parent().printHTML(djprint.printSterilizerLabelSheet(sterilizers, dentists, skip))
    
    #@pyqtSlot("")
    def on_cancelPushButton_clicked(self):
        self.close()

    def selectDentist(self):
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
    
    def selectSterilizer(self):
        findDlg = FindDlg(
        "Sterilizer",
        Sterilizer.objects.filter(inactive_date__isnull=True),
        ["id", "enroll_date"],
        {
        'field_widths': [250, 200],
        'window_height': 400,
        'window_width': 600,
        'zfill':[STERILIZER_ID_WIDTH, None]
        },
        self
        )
        return (findDlg.exec_())