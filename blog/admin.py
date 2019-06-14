from django.contrib import admin
from .models import Bloginfo,BecomePartner,Notification_Detail
from django.contrib import admin


# Register your models here.
admin.site.register([Bloginfo,BecomePartner,Notification_Detail])
