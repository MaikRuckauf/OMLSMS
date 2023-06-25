import datetime, locale, sys

#locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )
locale.setlocale( locale.LC_ALL, '' )

# Configuration File Constants
CONFIG_FILENAME = "\OMLSMS\config.txt"
#must be set here for imports
#OMLWEB_PATH = "C:\omlsms\web" #test directory
OMLWEB_PATH = "J:\Share\D R C\OML\OMLSMSv2\web" #installation directory
IMAGES_PATH = "" #set by configuration file

# Defines a range of dates that should be in the database
# This does not need to be updated unless this range is no longer covered
DATABASE_START_DATE = datetime.date(year = 1990, month=1, day=1)
DATABASE_STOP_DATE = datetime.date(year = 2050, month=1, day=1)

# Database File Constants
DENTIST_ID_WIDTH = 5
STERILIZER_ID_WIDTH = 7
RENEWAL_ID_WIDTH = 10
LOT_ID_WIDTH = 3
#TEST_ID_WIDTH = 9 #?
TEST_ID_WIDTH = 12
STRIP_ID_WIDTH = 2

# Policy settings
DAYS_UNTIL_OVERDUE = 30
COMPLIANT_TESTS_PER_YEAR = 42
REPORT_HISTORY_EXTRA_DAYS = 14
REPORT_HISTORY_DEFAULT_DAYS = 1000
MAX_LATE_FEE = 100
MAX_DAYS_FOR_COLLECTIONS = 730
DAYS_FOR_TEST = 7
MAX_DAYS_FOR_TEST_ENTRY = 60

# Display settings
MAX_FIND_DISPLAY_ROWS = 10000

# Default values for new records
DEFAULT_NUM_TESTS = 13
DEFAULT_RENEWAL_TEST = 9
DEFAULT_RENEWAL_FEE = 75.00
DEFAULT_STERILIZER_METHOD = 1 # 1 = Steam
DEFAULT_LOT_COUNT = 10000
DEFAULT_CHEMICAL_VAPOR = 3 # 3 = Ignore

# Text File Configuration
NUM_CONFIG_VALUES = 12
[
USER_INITIALS,
DEFAULT_USER,
SERVER_ADDRESS,
SERVER_PORT,
DATABASE_NAME,
MAIN_X_POS,
MAIN_Y_POS,
PDF_VIEWER_PATH,
PDF_PRINTER_PATH,
HTML_CONVERTER_PATH,
#IMAGES_PATH,
LABEL_PRINTER,
DEFAULT_PRINTER,
] = range(NUM_CONFIG_VALUES)

def readConfigValues(filename):
    configValues = []
    configFile = open(filename,"r")
    for line in configFile:
        value = line.split('#')[0].strip()
        if value != "":
            configValues.append(value)
    assert len(configValues) == NUM_CONFIG_VALUES
    if configValues[SERVER_PORT] == 'default':
        configValues[SERVER_PORT] = ''
    else:
        configValues[SERVER_PORT] = int(configValues[SERVER_PORT])
    configValues[MAIN_X_POS] = int(configValues[MAIN_X_POS])
    configValues[MAIN_Y_POS] = int(configValues[MAIN_Y_POS])
    return configValues

#
# Date formating and conversions
#
DATETIME_FORMAT = "%m/%d/%Y"
SHORT_DATETIME_FORMAT = "%m/%d/%y"

def RecordDateToText(value, shorten=False):
    return value.strftime(SHORT_DATETIME_FORMAT if shorten else DATETIME_FORMAT) \
        if value else ""
   
def FormDateToRecord(value, shortened=False):
    return datetime.datetime.strptime(
        str(value), SHORT_DATETIME_FORMAT if shortened else DATETIME_FORMAT
    ).date() if value else None

def DateRangeForMonth(year, month):
        start = datetime.date(year, month, 1)
        stop = datetime.date(
            year if month < 12 else year + 1,
            month + 1 if month < 12 else 1,
            1
        )
        return start, stop

#
# Currency formating
#
def NumToCurrency(value):
    try:
        return locale.currency(float(value), grouping=True)
    except:
        return ""

def CurrencyToNum(value):
    try:
        return float(value.translate(None, "$,"))
    except:
        return None

def GetSterilizerIDRange(dentist_id):
    w = STERILIZER_ID_WIDTH - DENTIST_ID_WIDTH
    start = dentist_id * (10 ** w)
    stop = ((dentist_id + 1) * (10 ** w)) - 1
    return (start, stop)

def SterilizerToRenewalIDRange(sterilizer_id):
    w = RENEWAL_ID_WIDTH - STERILIZER_ID_WIDTH
    start = sterilizer_id * (10 ** w)
    stop = ((sterilizer_id + 1) * (10 ** w)) - 1
    return (start, stop)

def SterilizerToDentistID(sterilizer_id):
    return int(str(sterilizer_id).zfill(STERILIZER_ID_WIDTH)[0:DENTIST_ID_WIDTH])

def RenewalToDentistID(renewal_id):
    return int(str(renewal_id).zfill(RENEWAL_ID_WIDTH)[0:DENTIST_ID_WIDTH])

def RenewalToSterilizerID(renewal_id):
    return int(str(renewal_id).zfill(RENEWAL_ID_WIDTH)[0:STERILIZER_ID_WIDTH])

def RenewalToLotID(renewal_id):
    return int(str(renewal_id).zfill(RENEWAL_ID_WIDTH)[STERILIZER_ID_WIDTH:])

def ZeroNone(value):
    if value:
        return value
    else:
        return 0
    
def NullNone(value):
    if value:
        return value
    else:
        return ""
