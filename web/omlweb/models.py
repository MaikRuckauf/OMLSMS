from django.db import models
from django.contrib.auth.models import User


class Update(models.Model):
    update_date = models.DateField()

    class Meta:
        db_table = 'update'
        
    def __unicode__(self):
        return u'Date'


class State(models.Model):
    abbreviation = models.CharField(max_length=2, primary_key = True)
    name = models.CharField(max_length=80, unique = True)

    class Meta:
        db_table = 'ref_state'
        
    def __unicode__(self):
        return u'%s' % (self.abbreviation)


class Dentist(models.Model):
    id = models.IntegerField(primary_key = True)
    practice_name = models.CharField(max_length=80)
    lname = models.CharField(max_length=80)
    fname = models.CharField(max_length=24)
    title = models.CharField(max_length=6)
    contact_lname = models.CharField(max_length=80)
    contact_fname = models.CharField(max_length=24)
    contact_title = models.CharField(max_length=6)
    address1 = models.CharField(max_length=80)
    address2 = models.CharField(max_length=80)
    city = models.CharField(max_length=40)
    state = models.ForeignKey(State)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=25)
    fax = models.CharField(max_length=25)
    email = models.EmailField(max_length=254)
    enroll_date = models.DateField()
    inactive_date = models.DateField(blank=True, null=True)
    comment = models.TextField()

    class Meta:
        db_table = 'sms_dentist'

    def getFullName(self):
        if self.lname:
            return "%s%s%s%s%s" % (self.title, 
                " " if self.title else "", self.fname,
                " " if self.fname else "", self.lname)
        else:
            return self.practice_name
        
    def __unicode__(self):
        return u'%s %s %s' % (self.practice_name, self.fname, self.lname)


class SterilizerMethod(models.Model):
    name = models.CharField(max_length=20)
    label = models.CharField(max_length=20)
    active = models.BooleanField()

    class Meta:
        db_table = 'ref_sterilizer_method'
        
    def __unicode__(self):
        return u'%s' % (self.name)


class Sterilizer(models.Model):
    id = models.IntegerField(primary_key = True)
    dentist = models.ForeignKey(Dentist)
    sterilizer = models.IntegerField()
    enroll_date = models.DateField()
    num_tests = models.IntegerField()
    renew_test = models.IntegerField()
    renew_fee = models.DecimalField(max_digits=8, decimal_places=2)
    serial_num = models.CharField(max_length = 20)
    model = models.CharField(max_length = 50) #todo: standardize
    method = models.ForeignKey(SterilizerMethod)
    last_report_date = models.DateField(blank=True, null=True)
    last_certificate_date = models.DateField(blank=True, null=True)
    inactive_date = models.DateField(blank=True, null=True)
    comment = models.TextField()
    renew = models.BooleanField()
    suspend = models.BooleanField()

    class Meta:
        db_table = 'sms_sterilizer'
        
    def __unicode__(self):
        return u'%d' % (self.id)


class Vapor(models.Model):
    name = models.TextField(max_length=10)
    active = models.BooleanField()

    class Meta:
        db_table = 'ref_vapor'

    def __unicode__(self):
        return u'%s' % (self.name)

    
class Lot(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.TextField(max_length=12)
    receive_date = models.DateField()
    expiration_date = models.DateField()
    count = models.IntegerField()
    vapor = models.ForeignKey(Vapor)
    inactive_date = models.DateField(blank=True, null=True)
    comment = models.TextField()

    class Meta:
        db_table = 'sms_lot'
        
    def __unicode__(self):
        return u'%d' % (self.id)


class Renewal(models.Model):
    id = models.IntegerField(primary_key = True)
    sterilizer = models.ForeignKey(Sterilizer)
    lot =  models.CharField(max_length=12) #todo: models.ForeignKey(Lot)?
    renewal_date = models.DateField()
    num_tests = models.IntegerField()
    renewal_fee = models.DecimalField(max_digits=8, decimal_places=2)
    late_fee = models.DecimalField(max_digits=8, decimal_places=2,
                                   blank=True, null=True)
    # todo: decouple payment data
    payment_date = models.DateField(blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2,
                                          blank=True, null=True)
    check_num = models.CharField(max_length = 20)
    comment = models.TextField()
    inactive_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'sms_renewal'
        
    def __unicode__(self):
        return u'%d' % (self.id)


class Test(models.Model):
    renewal = models.ForeignKey(Renewal)
    test_num = models.IntegerField()
    sample_date = models.DateField()
    start_date = models.DateField()
    result = models.CharField(max_length=1, blank=True, null=True)
    control_result = models.CharField(max_length=1, blank=True, null=True)
    result_date = models.DateField(blank=True, null=True)
    started_by = models.CharField(max_length=3)
    finished_by = models.CharField(max_length=3)
    comment = models.TextField()
    strip_num = models.IntegerField(null=True)

    class Meta:
        db_table = 'sms_test'
        
    def __unicode__(self):
        return u'%d %d' % (self.renewal.id, self.test_num)

    
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    # Other fields here
    dentist = models.OneToOneField(Dentist)
    
    def __unicode__(self):
        return self.dentist.__unicode__()    

class ClientProfile(models.Model):
    name_title = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    title = models.TextField()
    initials = models.TextField()
    userclass = models.IntegerField()
    signature_file = models.TextField()

    class Meta:
        db_table = 'client_user'
        
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
