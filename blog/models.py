from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Bloginfo(models.Model):
     title = models.CharField(max_length=1000, null =True)
     description = models.TextField(null=True)
     image = models.FileField(null=True)
     publish_date = models.DateTimeField(default=timezone.now)
     def __str__(self):
         return self.title


class BecomePartner(models.Model):
    name=models.CharField(max_length=1000,null=True,blank=True)
    email=models.CharField(max_length=1000,null=True,blank=True)
    company_name=models.CharField(max_length=1000,null=True,blank=True)
    message=models.TextField(null=True,blank=True)




class Notification_Detail(models.Model):
    receiver=models.ForeignKey(User)
    type_of_notification=models.CharField(max_length=5000,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    target=models.CharField(max_length=5000,null=True,blank=True)
    read=models.BooleanField(default=False,blank=True)
    isdeleted=models.BooleanField(default=False,blank=True)
    timecreated=models.DateTimeField(auto_now_add=True,null=True)