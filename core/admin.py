# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.contrib import admin

# Register your models here.
admin.site.register([Register,Packages,LoggedInUser,Allagencies,City,County])