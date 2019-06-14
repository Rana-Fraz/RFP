# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class notification_test_data(models.Model):
    description=models.TextField()

class transfer_test_data(models.Model):
    record=models.TextField()