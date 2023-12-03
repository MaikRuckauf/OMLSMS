from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from omlweb.models import Dentist, Sterilizer, Renewal, Test
from xhtml2pdf.document import pisaDocument
import cStringIO as StringIO
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from django.db.models import F, Max, Sum

def today():
    return date(2010,7,1)


def home(request):

    t = get_template("home.html")
    c = Context({
    })
    return HttpResponse(t.render(c))


def summary(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    
    d = request.user.get_profile().dentist
    sterilizers = Sterilizer.objects.filter(dentist=d).filter(inactive_date=None)
    summaries = []
    for s in sterilizers:
        amount, due_date = getSterilizerPaymentSummary(s.id)
        if due_date and today() > due_date:
            overdue = True
        else:
            overdue = False
        tests, positives, positive_date = getSterilizerResultsSummary(s.id)
        dict = {
        'id': s.id,
        'total_due': amount,
        'due_date': due_date,
        'overdue': overdue,
        'num_recent_tests': tests,
        'num_recent_positives': positives,
        'last_positive_date': positive_date,
        }
        summaries.append(dict)
    
    t = get_template('summary.html')
    c = Context({
    'page_summary': True,
    'today': today(),
    'username': request.user.username,
    'dentist': d,
    'sterilizers': summaries
    })
    return HttpResponse(t.render(c))


def getSterilizerPaymentSummary(sterilizer_id):
    q = getRecentRenewals(sterilizer_id)
    renewals = selectRenewalsToPay(q)
    amount_due = zeroNone(renewals.aggregate(Sum('renewal_fee'))['renewal_fee__sum']) + \
                 zeroNone(renewals.aggregate(Sum('late_fee'))['late_fee__sum']) - \
                 zeroNone(renewals.aggregate(Sum('payment_amount'))['payment_amount__sum'])
    due_date = renewals.aggregate(Max('renewal_date'))['renewal_date__max']
    if due_date:
        due_date = due_date + timedelta(days=30)
    return (amount_due, due_date)


def getRecentRenewals(sterilizer_id):
    # sterilizer_id refers to different things below (table field, argument)
    q = Renewal.objects.filter(sterilizer_id=sterilizer_id)
    return q.exclude(renewal_date__lt=today() - timedelta(days=300))


def selectRenewalsToPay(query):
    q = query.exclude(renewal_fee=F('payment_amount')-F('late_fee'))
    q = q | query.filter(payment_amount=None)
    return q.order_by('renewal_date')


def getSterilizerResultsSummary(sterilizer_id):
    recent = getRecentResults(sterilizer_id)
    positives = selectPositiveResults(recent)
    most_recent_date = positives.aggregate(Max('result_date'))['result_date__max']
    if most_recent_date:
        most_recent_date = most_recent_date.date()
    return (len(recent), len(positives), most_recent_date)


def getRecentResults(sterilizer_id):
    # sterilizer_id refers to different things below (table field, argument)
    q = Test.objects.filter(renewal_id__sterilizer_id=sterilizer_id)
    return q.exclude(sample_date__lt=today() - timedelta(days=90))


def selectPositiveResults(query):
    return query.filter(result='+')


def zeroNone(value):
    if value:
        return value
    else:
        return 0


def billing(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    d = request.user.get_profile().dentist
    sterilizers = Sterilizer.objects.filter(dentist=d).filter(inactive_date=None)
    payment_list = []
    for s in sterilizers:
        dict = getBillingData(s.id)
        dict['sterilizer'] = s
        payment_list.append(dict)

    t = get_template('billing.html')
    c = Context({
    'page_billing': True,
    'today': today(),
    'username': request.user.username,
    'dentist': d,
    'payment_list': payment_list,
    })
    return HttpResponse(t.render(c))


def getBillingData(sterilizer_id):
    balances = []
    q = getRecentRenewals(sterilizer_id).order_by('renewal_date')
    amount, due_date = getSterilizerPaymentSummary(sterilizer_id)
    if due_date and today() > due_date:
        overdue = True
    else:
        overdue = False

    for renewal in q:
        balance = zeroNone(renewal.renewal_fee) + zeroNone(renewal.late_fee) - \
                  zeroNone(renewal.payment_amount)
        balances.append({'renewal_id': renewal.id, 'amount':balance})
    dict = {
    'renewals':q,
    'balances':balances,
    'amount':amount,
    'due_date':due_date,
    'overdue': overdue,
    }
    return dict


def results(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    d = request.user.get_profile().dentist
    sterilizers = Sterilizer.objects.filter(dentist=d).filter(inactive_date=None)
    results_list = []
    for s in sterilizers:
        dict = getResultsData(s.id)
        dict['sterilizer'] = s
        results_list.append(dict)
        
    t = get_template('results.html')
    c = Context({
    'page_results': True,
    'today': today(),
    'username': request.user.username,
    'dentist': d,
    'result_summaries': results_list
    })
    return HttpResponse(t.render(c))


def getResultsData(sterilizer_id):
    q = getRecentResults(sterilizer_id).order_by('sample_date')
    dict = {
    'tests':q,
    }
    return dict


def billPDF(request, sterilizer_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    d = request.user.get_profile().dentist
    try:
        s = Sterilizer.objects.get(id=sterilizer_id)
        assert s.dentist.id == d.id
    except:
        return HttpResponseRedirect('/invalid/sterilizer_id/%s' % sterilizer_id)

    payment = getBillingData(s.id)
    t = get_template('bill.html')
    c = Context({
    'dentist': d,
    'payment': payment,
    })
    #return HttpResponse(t.render(c))
    return render_to_pdf(t,c)


def resultsPDF(request, sterilizer_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)

    d = request.user.get_profile().dentist
    sterilizers = Sterilizer.objects.filter(dentist=d).filter(inactive_date=None)
    results_list = []
    for s in sterilizers:
        dict = getResultsData(s.id)
        dict['sterilizer'] = s
        results_list.append(dict)
        
    t = get_template('report.html')
    c = Context({
    'dentist': d,
    'result_summaries': results_list
    })

    '''d = request.user.get_profile().dentist
    try:
        s = Sterilizer.objects.get(id=sterilizer_id)
        assert s.dentist.id == d.id
    except:
        return HttpResponseRedirect('/invalid/sterilizer_id/%s' % sterilizer_id)

    summary = getResultsData(s.id)
    t = get_template('report.html')
    c = Context({
    'dentist': d,
    'summary': summary,
    })'''
    return render_to_pdf(t,c)


def invalidSterilizer(request, sterilizer_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    s = "We're sorry, we can not provide the requested information for \
         sterilizer #%s" % sterilizer_id
    return HttpResponse(s)
    
    
def render_to_pdf(template, context):
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error encoding PDF <pre>%s</pre>' % cgi.escape(html))
