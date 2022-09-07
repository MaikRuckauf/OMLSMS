import sys, os
from constants import *
import constants

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import ui, logindlg

sys.path.append(OMLWEB_PATH)
from django.conf import settings
import omlweb

import printpdf
import ctypes

def main(isTestEnviron, *argv):

    app=QApplication(sys.argv)
    app.setOrganizationName("Oral Microbiology Laboratory")
    app.setOrganizationDomain("unc.oml.edu")
    app.setApplicationName("Oral Microbiolgy Lab Database")
    app.setWindowIcon(QIcon("icon.ico"))

    # Get an icon other than python script icon
    myappid = 'oral_micro.sterilizer_monitoring.database_client' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    #  How to get the roaming app user directory to store user info.
    #  The Dental School doesn't support roaming so this will not be used.
    #  However, I left this here for possible future use.
    #import ctypes.wintypes
    #SIDL_APPDATA = 26       # My Documents
    #SHGFP_TYPE_CURRENT = 0   # Want current, not default value
    #buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    #ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_APPDATA, 0, SHGFP_TYPE_CURRENT, buf)
    #print buf.value

    cwd = os.getcwd()
    #webdir = (os.path.split(cwd)[0] + '\web\omlweb').replace('\\','/')
    webdir = OMLWEB_PATH.replace('\\','/') + "/omlweb"

    configValues = []
    try:
        configValues = readConfigValues(cwd + "\config.txt")
    except Exception, e:
        QMessageBox.critical(None, "Error Reading Configuration File", unicode(e))
    else:
        # Django settings
        settings.configure(
            DATABASES = {
                'default': {
                    'ENGINE': 'sqlserver_ado',
                    'NAME': configValues[DATABASE_NAME],
                    'USER': '', # value is altered in logindlg
                    'PASSWORD': '', # value is altered in logindlg
                    'HOST': configValues[SERVER_ADDRESS],
                    'PORT': configValues[SERVER_PORT],
                    'OPTIONS' : {
                                'provider': 'SQLOLEDB',
                                'use_mars': True,
                                },                     
                }
            },
            
            TEMPLATE_DIRS = (
                webdir + "/account",
                webdir + "/base",
                webdir + "/summary",
                webdir + "/billing",
                webdir + "/results",
                webdir + "/templatetags",
                webdir + "/letters",
                webdir + "/labels",
                webdir + "/reports",
            ),
            INSTALLED_APPS = (
                'omlweb',
            )
        )

        printpdf.pdfview_filename = configValues[PDF_VIEWER_PATH]
        printpdf.gsprint_filename = configValues[PDF_PRINTER_PATH]
        printpdf.htmltopdf_filename = configValues[HTML_CONVERTER_PATH]
        printpdf.labelPrinterName = configValues[LABEL_PRINTER]
        printpdf.defaultPrinterName = configValues[DEFAULT_PRINTER]
        printpdf.testPrinting = isTestEnviron
        constants.IMAGES_PATH = (webdir + "/images/").replace('/','\\')
        #constants.IMAGES_PATH = configValues[IMAGES_PATH]
        
        if len(argv):
            configValues[USER_INITIALS] = argv[0]

        login = logindlg.LoginDlg(configValues[DEFAULT_USER])
        if login.exec_():
            try:
                form=MainWindow(configValues, login.loginLineEdit.text(), configValues[USER_INITIALS])
                form.move(configValues[MAIN_X_POS], configValues[MAIN_Y_POS])
                form.show()
            except Exception, e:
                QMessageBox.critical(None, "Error Initializing Program", unicode(e))
            finally:
                app.exec_()


class MainWindow(QMainWindow, ui.Ui_mainWindow):
    

    def __init__(self, configValues, userName, defaultInitials, parent=None):
        super(MainWindow, self).__init__(parent)

        import dentistdlg, sterilizerdlg, lotdlg, renewaldlg, testdlg, reportdlg

        self.setupUi(self)
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle("OML Database")

        self.configValues = configValues
        self.userName = userName
        self.printer = None
        
        self.bookmark = {}
        self.currentChild = None

        self.dentistDlg = dentistdlg.DentistDlg(self)
        self.sterilizerDlg = sterilizerdlg.SterilizerDlg(self)
        self.lotDlg = lotdlg.LotDlg(self)
        self.renewalDlg = renewaldlg.RenewalDlg(self)
        self.testDlg = testdlg.TestDlg(self)
        self.reportDlg = reportdlg.ReportDlg(self)
        
        self.dialogs = [
        self.dentistDlg,
        self.sterilizerDlg,
        self.lotDlg,
        self.renewalDlg,
        self.testDlg,
        self.reportDlg
        ]

        self.userList = omlweb.models.ClientProfile.objects.all()
        self.userList = self.userList.order_by('userclass', 'last_name')
        self.director = self.userList[0]
        for number, user in enumerate(self.userList):
            self.userComboBox.insertItem(number, user.initials)
            if user.userclass == 1:
                self.director = user
            if number == 0 or user.initials == defaultInitials:
                self.user = self.userList[number]
                self.userComboBox.setCurrentIndex(number)
    
    def showMainDialog(self, show=None):
        # Note: only one MainDialog should be open at once
        # don't leave active dialog if currently editing
        for dialog in [x for x in self.dialogs if (x.isVisible() and x.editing)]:
            QApplication.beep()
            dialog.activateWindow()
            return
        # hide all dialogs, saving a bookmark from the visible dialog
        for dialog in self.dialogs:
            if dialog.isVisible():
                self.bookmark.update(dialog.makeBookmark())
                dialog.hide()
        # show the desired dialog, initialized as appropriate for the bookmark
        if show.isHidden():
            show.move(self.pos() + QPoint(5, self.height() + 50))
            show.show(self.bookmark)
            self.currentChild = show
    
    @pyqtSignature("")
    def on_dentistsPushButton_clicked(self):
        self.showMainDialog(self.dentistDlg)
        
    @pyqtSignature("")
    def on_sterilizersPushButton_clicked(self):
        self.showMainDialog(self.sterilizerDlg)

    @pyqtSignature("")
    def on_lotsPushButton_clicked(self):
        self.showMainDialog(self.lotDlg)

    @pyqtSignature("")
    def on_renewalsPushButton_clicked(self):
        self.showMainDialog(self.renewalDlg)

    @pyqtSignature("")
    def on_testsPushButton_clicked(self):
        self.showMainDialog(self.testDlg)

    @pyqtSignature("")
    def on_reportsPushButton_clicked(self):
        self.showMainDialog(self.reportDlg)
    
    @pyqtSignature("int")
    def on_userComboBox_activated(self, int):
        self.user = self.userList[int]
        if self.currentChild:
            # activate editing window again
            self.currentChild.activateWindow()

if __name__ == "__main__":
	main(True, *sys.argv[1:])