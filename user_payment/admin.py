# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Payment,PaymentLogs, PaymentCardInfo
# Register your models here.
admin.site.register([Payment,PaymentLogs,PaymentCardInfo])