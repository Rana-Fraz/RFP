# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64

from django.contrib.auth.models import User
from django.db import models
from core.models import Register,Packages
from django.utils import timezone
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.


#To store payment history and details
class Payment(models.Model):

    reg_fk = models.ForeignKey(Register,related_name='Register')
    pkg_fk = models.ForeignKey(Packages,related_name='packg')
    pay_date = models.DateField(default=timezone.now())
    end_date = models.DateField()
    is_paid = models.BooleanField()
    is_expired = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=500)
    request_count = models.IntegerField(default=0)

    def __str__(self):
        return self.reg_fk.user.username

#This model is used for (F) for delayed payment
class PaymentLogs(models.Model):

    log_reg_fk = models.ForeignKey(Register)
    log_pkg_fk = models.ForeignKey(Packages,related_name='pkg')
    log_pay_date = models.DateField(default=timezone.now())
    log_end_date = models.DateField()
    log_is_paid = models.BooleanField()
    log_is_expired = models.BooleanField(default=True)
    log_secret_key = models.CharField(max_length=500)
    log_request_count = models.IntegerField(default=0)

    def __str__(self):
        return self.log_reg_fk.user.username

class PaymentCardInfo(models.Model):

    user = models.ForeignKey(User, default='')
    number = models.CharField(max_length=5000)
    cvc =models.CharField(max_length=5000)
    expDate = models.CharField(max_length=20)
    pinCode = models.BigIntegerField(validators=[MaxValueValidator(9999)],blank=True,null=True)
    name = models.CharField(max_length=100,blank=True)
    street_address = models.CharField(max_length=500,blank=True)
    zipcode = models.CharField(max_length=200,blank=True)
    city = models.CharField(max_length=200,blank=True)
    state = models.CharField(max_length=200,blank=True)
    country = models.CharField(max_length=200,blank=True)
    default = models.BooleanField(default=False,blank=True)
    card_type = models.CharField(max_length=1000,null=True,blank=True)
    autopay=models.BooleanField(default=False,blank=True)
    test=models.CharField(max_length=200,blank=True)
    info =  models.CharField(max_length=2000,blank=True)

    def  __str__(self):
      return self.user.username
