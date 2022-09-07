import sys, datetime

from constants import *

sys.path.append(OMLWEB_PATH)
from omlweb.models import Update, Renewal, Sterilizer, Dentist
from django.db.models import F

import bulkops

def updateDatabase():
    #updates = Update.objects.all().order_by('-update_date')
    updateLateFees()
    #if not updates or updates[0].update_date != datetime.date.today():
    #    updateLateFees()
    #    update = Update(update_date = datetime.date.today())
    #    update.save()

def updateLateFees():
    date = datetime.date.today() - datetime.timedelta(days=MAX_DAYS_FOR_COLLECTIONS)
    list = Renewal.objects.filter(renewal_date__gte=date)
    list = list.exclude(payment_amount__gte=F('renewal_fee')) #if they pay the principal, don't add to late fees
    list = list.exclude(renewal_fee=0)
    #list = list.exclude(late_fee=MAX_LATE_FEE)
    
    #list = list.filter(inactive_date__isnull=True)
    #list = list.filter(sterilizer__inactive_date__isnull=True)
    #list = list.filter(sterilizer__dentist__inactive_date__isnull=True)
    
    updated = []
    for renewal in list:
        lateFee = calculateLateFee(renewal)
        if lateFee != renewal.late_fee:
            renewal.late_fee = lateFee
            updated.append(renewal)
    if updated:
        bulkops.update_many(updated, ["late_fee"]) #update all lateFees in one query

#
# How to calculate late fees
#
# $5 for every 30 days, no charge until 45 days
# No late fee to exceed MAX_LATE_FEE (to prevent accidental excessive bills)
#
def calculateLateFee(renewal):
    if renewal.renewal_fee == 0:
        return 0
    daysOverdue = (datetime.date.today() - renewal.renewal_date).days
    if daysOverdue < 45:
        return 0
    else:
        return min((daysOverdue/30) * 5, MAX_LATE_FEE)