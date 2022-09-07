import sys
from datetime import date, timedelta
import cStringIO as StringIO
from constants import *

from xhtml2pdf.document import pisaDocument

sys.path.append(OMLWEB_PATH)
from django.template import Context, Template
from django.template.loader import get_template
from omlweb.views import getBillingData
from omlweb.models import Dentist, State, Renewal, Sterilizer, Test


def getBillForSterilizer(sterilizer_id, dentist=None, renewal=None):
    if not dentist:
        dentist_id = int(str(sterilizer_id).zfill(STERILIZER_ID_WIDTH )[0:DENTIST_ID_WIDTH])
        dentist = Dentist.objects.get(id=dentist_id)
    t = get_template('bill.html')
    payment = getBillingData(sterilizer_id)

    # want to show unpaid balances plus last paid balance
    # show at least the last three balances if possible
    i = 1
    while i < len(payment['balances']) and payment['balances'][-i]['amount'] != 0:
        i = i + 1

    payment['renewals'] = payment['renewals'][:]
    value = min(len(payment['renewals']), max(i, 3))
    payment['renewals'] = payment['renewals'][-value:]

    if renewal:
        payment['renewals'].append(renewal)
        amount = ZeroNone(renewal.renewal_fee) + ZeroNone(renewal.late_fee) - \
                 ZeroNone(renewal.payment_amount)
        dict = {
        'renewal_id' : renewal.id,
        'amount' : amount,
        }
        payment['balances'].append(dict)
        payment['amount'] = payment['amount'] + amount
        payment['due_date'] = renewal.renewal_date + datetime.timedelta(days=30)

    c = Context({
    'dentist': dentist,
    'payment': payment,
    })
    #pdf = create_PDF(t, c).getvalue()
    return(t.render(c))

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

def encodeTo128Font(value):
    if value == 0:
        return 128
    elif value >= 95:
        return value + 50
    else:
        return value + 32

def encodeToCode128(id):
    # Encode ID string to condensed Code 128c
    # (Start C) (Encoded Pairs) (Checksum) (End Char)
    # Checksum =  Value of Start C + (Value * Position) of Encoded Pairs
    checksum = 105
    code = ""
    for position, pair in enumerate(chunker(id, 2)):
        checksum += int(pair) * (position + 1)
        code = code + "&#%d" % encodeTo128Font(int(pair))
    checksum = encodeTo128Font(checksum % 103)
    return "&#155" + code + ("&#%d" % checksum) + "&#156"

def getRenewalLabelsForSterilizers(sterilizers, dentists, lot):
    t = get_template('renewallabel.html')
    renewal_ids = []
    barcodes = []
    numLabels = 0
    for sterilizer in sterilizers:
        numLabels += sterilizer.num_tests
        base = ("%d%d" % (sterilizer.id, lot.id)).zfill(RENEWAL_ID_WIDTH)
        ids = []
        codes = []
        for strip in range(1, sterilizer.num_tests + 1):
            id = "%s%s" % (base, str(strip).zfill(STRIP_ID_WIDTH))
            ids.append(id)
            codes.append(encodeToCode128(id))
        #renewal_ids.append(id)
        #barcodes.append(encodeToCode128(id))
        renewal_ids.append(ids)
        barcodes.append(codes)

    z = zip(sterilizers,renewal_ids,barcodes)

    c = Context({
    'today': date.today(),
    'sterilizers': sterilizers,
    'dentists': dentists,
    'lot': lot,
    'zips': z,
    'image_directory': IMAGES_PATH,
    'num_labels': numLabels,
    })
    return(t.render(c))
    
def getBillsForDentist(dentist):
    #dentist = Dentist.objects.get(id=dentist_id)
    (start, stop) = GetSterilizerIDRange(dentist.id)
    sterilizers = Sterilizer.objects.filter(id__range=(start, stop))\
                     .filter(inactive_date=None)
    if not sterilizers:
        return ""
    html = ""
    for i,sterilizer in enumerate(sterilizers):
        if i != len(sterilizers) - 1:
            html += getBillForSterilizer(sterilizer.id, dentist) + \
            "\r\n" + "<pdf:nextpage />" + "\r\n"
        else:
            html += getBillForSterilizer(sterilizer.id, dentist) 
    return(html)

'''
def create_PDF(template, context):
    html  = template.render(context)
    result = StringIO.StringIO()
    #print html.encode("ISO-8859-1")
    pdf = pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result
    return None
'''

def getResultsDateRange(sterilizer):
    r = Renewal.objects.filter(sterilizer__id=sterilizer.id)
    r = r.filter(inactive_date__isnull=True).order_by("-renewal_date")
    if len(r) > 1:
        # For sterilizer with multiple renewals, include history from shortly
        # before previous renewal until today
        start_date = r[1].renewal_date - timedelta(days=REPORT_HISTORY_EXTRA_DAYS)
    elif r:
        # For sterilizer with only one renewal, report whole history
        start_date = r[0].renewal_date
    else:
        # Report for sterilizer with no renewals (this really should not be done)
        start_date = date.today() - timedelta(days=REPORT_HISTORY_DEFAULT_DAYS)
    return (start_date, date.today())
  
def getResultsLetter(dentist, sterilizers, date_range):
    results_list = []
    for sterilizer in sterilizers:
        if not date_range:
            (start_date, stop_date) = getResultsDateRange(sterilizer)
        else:
            (start_date, stop_date) = date_range
        q = Test.objects.filter(renewal_id__sterilizer_id=sterilizer.id)
        q = q.filter(start_date__range=(start_date, stop_date))
        q = q.order_by('sample_date')
        dict = {
        'tests':q,
        'sterilizer': sterilizer,
        'start_date': start_date,
        'stop_date': stop_date,
        }
        results_list.append(dict)

    t = get_template('report.html')
    c = Context({
    'today': date.today(),
    'dentist': dentist,
    'result_summaries': results_list,
    'image_directory': IMAGES_PATH,
    })
    return(t.render(c))
    
def getReportForSterilizer(sterilizer_id, date_range = None):
    dentist_id = str(sterilizer_id).zfill(STERILIZER_ID_WIDTH)[0:DENTIST_ID_WIDTH]
    dentist = Dentist.objects.get(id=dentist_id)
    sterilizer = Sterilizer.objects.get(id=sterilizer_id)
    sterilizers = [sterilizer]
    return getResultsLetter(dentist, sterilizers, date_range)

def getReportForDentist(dentist_id, date_range = None):
    dentist = Dentist.objects.get(id=dentist_id)
    sterilizers = Sterilizer.objects.filter(dentist__id=dentist_id)
    sterilizers = sterilizers.filter(inactive_date__isnull=True)
    if not sterilizers:
        return ""
    return getResultsLetter(dentist, sterilizers, date_range)

def printNotifyLetter(dentist, test, user, contacted):
    t = get_template('notify_letter.html')
    c = Context({
    'today': date.today(),
    'dentist': dentist,
    'test': test,
    'user': user,
    'contacted': contacted,
    'image_directory': IMAGES_PATH,
    })
    return(t.render(c))

def printDentistLabelSheet(dentists, skip):
    t = get_template('dentist_labelsheet.html')
    c = Context({
    'dentists': dentists,
    'skip': skip,
    })
    return(t.render(c))
    
def printSterilizerLabelSheet(sterilizers, dentists, skip):
    t = get_template('sterilizer_labelsheet.html')
    c = Context({
    'sterilizers': sterilizers,
    'dentists': dentists,
    'skip': skip,
    })
    return(t.render(c))

def testCountReport(title, testList):
    t = get_template('testcount.txt')
    c = Context({
    'title': title,
    'tests': testList,
    })
    return(t.render(c))

def inactivityReport(sterilizerList, names, weeks, activity):
    t = get_template('inactivityreport.txt')
    c = Context({
    'sterilizers': sterilizerList,
    'names': names,
    'activity': activity,
    'weeks': weeks,
    })
    return(t.render(c))

def getAnomalyReport(suspended, s_names, overlooked, o_names):
    t = get_template('anomalyreport.txt')
    c = Context({
    'suspended': suspended,
    's_names': s_names,
    'overlooked': overlooked,
    'o_names': o_names,
    })
    return(t.render(c))

def printOverdueAccountList(renewalList, namesList):
    t = get_template('overduereport.txt')
    c = Context({
    'renewals': renewalList,
    'names': namesList,
    })
    return(t.render(c))

def printDailyPaymentReport(renewalList, namesList):
    t = get_template('paymentreport.txt')
    c = Context({
    'renewals': renewalList,
    'names': namesList,
    })
    return(t.render(c))

def printQuarterlyPaymentSummary(values):
    t = get_template('accountssummary.txt')
    c = Context(values)
    return(t.render(c))

def viewRenewals(renewalList, namesList, header, start, stop):
    t = get_template('renewallist.txt')
    c = Context({
    'renewals': renewalList,
    'names': namesList,
    'header': header,
    'begin_date': start,
    'end_date': stop,
    })
    return(t.render(c))

def viewTests(testList, header, start, stop):
    t = get_template('testcount.txt')
    c = Context({
    'tests': testList,
    'title': header,
    'begin_date': start,
    'end_date': stop,
    })
    return(t.render(c))

def printYearlyComplianceLetter(dentist, sterilizer, compliance, year, numTests, user):
    t = get_template('complianceletter.html')
    c = Context({
    'today': date.today(),
    'dentist': dentist,
    'sterilizer': sterilizer,
    'number_of_tests': numTests,
    'user': user,
    'report_year': year,
    'compliance': compliance,
    'image_directory': IMAGES_PATH,
    })
    return(t.render(c))

def printLotRecall(renewalList, namesList):
    t = get_template('lotrecall.txt')
    c = Context({
    'renewals': renewalList,
    'names': namesList,
    })
    return(t.render(c))

def printRenewalsStarted(sterilizerList, namesList):
    t = get_template('startrenewal.txt')
    c = Context({
    'sterilizers': sterilizerList,
    'names': namesList,
    })
    return(t.render(c))