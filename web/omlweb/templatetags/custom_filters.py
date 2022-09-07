from django import template
import locale
import datetime

STERILIZER_ID_DIGITS = 7
RENEWAL_ID_DIGITS = 10
TEST_ID_DIGITS = 12

#locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )
locale.setlocale( locale.LC_ALL, '' )

register = template.Library()

@register.filter(name='zfill')
def zfill_filter(value, num_digits):
    try:
        s = str(value).zfill(num_digits)
    except:
        s = 'Err'
    return s

@register.filter(name='currency')
def currency_filter(i):
    try:
        s = locale.currency(float(i), grouping=True)
    except:
        s = 'Err'
    return s

@register.filter(name='payment')
def payment(value):
    try:
        s = "{:7.2f}".format(value)
    except:
        s = 'Err'
    return s

@register.filter(name='renewal_id')
def renewal_id_filter(i):
    try:
        s = str(i).zfill(RENEWAL_ID_DIGITS)
        s = s[0:STERILIZER_ID_DIGITS] + "-" + s[STERILIZER_ID_DIGITS:]
    except:
        s = 'Err'
    return s

@register.filter(name='test_result')
def test_result(i):
    if i:
        return i
    else:
        return ""

@register.filter(name='test_id')
def renewal_id_filter(i):
    try:
        s = str(i).zfill(TEST_ID_DIGITS)
        s = s[0:STERILIZER_ID_DIGITS] + "-" \
            + s[STERILIZER_ID_DIGITS:RENEWAL_ID_DIGITS] + "-" + \
            s[RENEWAL_ID_DIGITS:]
    except:
        s = 'Err'
    return s

@register.filter(name='days_overdue')
def days_overdue_filter(d):
    try:
        s = str((datetime.date.today() - d).days)
        #s = str(max((datetime.date.today() - renewal.renewal_date).days - 30,0))
    except:
        s = 'Err'
    return s

@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)

@register.filter(name='zip2')
def zip_lists2(a, b):
    return zip(zip(*a)[0], zip(*a)[1], b)

@register.filter(name='times') 
def times(number):
    return range(number)

@register.filter(name='my_add')
def my_add(a,b):
    try:
        return (a if a else 0) + (b if b else 0)
    except:
        return 'Err'

@register.filter(name='multiply')
def multiply(a,b):
    try:
        return a * b
    except:
        return 'Err'

@register.filter(name='next_label') 
def next_label(number, skip):
    if (number + skip) % 30 == 0:
        return "<pdf:nextpage />"
    else:
        return "<pdf:nextframe />"
    
@register.filter(name='next_frame')
def next_frame(number, num_per_page):
    if number % num_per_page == 0:
        return "<pdf:nextpage />"
    else:
        return "<pdf:nextframe />"
