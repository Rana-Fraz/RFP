# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from core.models import Register,Packages
from django.utils import timezone
from jsonfield import JSONField
# Create your models here.
#
# class Payment(models.Model):
#
#     reg_fk = models.ForeignKey(Register)
#     # reg_fk = models.ForeignKey(User,related_name='paid_user',on_delete=models.CASCADE,default=None)
#     pkg_fk = models.ForeignKey(Packages,related_name='packg')
#     pay_date = models.DateTimeField(default=timezone.now())
#     end_date = models.DateTimeField()
#     is_paid = models.BooleanField()
#     is_expired = models.BooleanField(default=False)
#     secret_key = models.CharField(max_length=500, unique=True)
#     request_count = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.reg_fk.user.username

# class Log (models.Model):
#     payment_fk = models.ForeignKey(Payment)
#     request_timestamp = models.DateTimeField(default=timezone.now())
#     customer_file_url = models.URLField()
#     file_details = JSONField()
#     response_timestamp = models.DateTimeField()
#     status = models.BooleanField()
#     result_file_url = models.URLField()
#     is_successful = models.BooleanField()
#
#     def __Payment__(self):
#         return self.payment_fk

