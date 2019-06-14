# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Register(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=False)
    type = models.CharField(default="user",max_length=50,blank=True)
    company = models.CharField(max_length=500,blank=True)
    is_authenticated = models.BooleanField(default=False)
    # authenticate_code = models.TextField(unique=True,default=None,null=True)
    authenticate_code = models.TextField(default=None,null=True,blank=True)
    address = models.CharField(max_length=500,null= True,blank=True)
    phone_no = models.CharField(max_length=20,null= True,blank=True)
    zipcode = models.CharField(max_length=200, null=True,blank=True)
    city = models.CharField(max_length=200, null=True,blank=True)
    state = models.CharField(max_length=200,null= True,blank=True)
    country = models.CharField(max_length=200,null= True,blank=True)
    newsletter = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=timezone.now,blank=True)
    user_preference = ArrayField(models.CharField(max_length=200), null=True,blank=True)
    state_preference = ArrayField(models.CharField(max_length=200), null=True,blank=True)
    city_preference = ArrayField(models.CharField(max_length=200), null=True,blank=True)
    county_preference = ArrayField(models.CharField(max_length=200), null=True,blank=True)
    agency_preference = ArrayField(models.CharField(max_length=200), null=True,blank=True)
    user_states = ArrayField(models.CharField(max_length=200), null=True,blank=True)
    profilePhoto = models.CharField(default='', blank=True, max_length=500)
    is_social = models.BooleanField(default=False)
    social_id = models.CharField(max_length=200, default='', blank=True)
    social_provider = models.CharField(max_length=200, default='', blank=True)


    def __str__(self):
        return self.user.email + ' , ' + self.type

class Packages (models.Model):
    PACKAGE_TYPE_CHOICES = (
        ('B', 'Basic'),
        ('R', 'Regular'),
        ('C', 'Classic'),
        ('P', 'Premium'),
    )
    PACKAGE_DURATION_CHOICES = (
        ('M', 'Monthly'),
        ('Q', 'Quater'),
        ('S', 'SixMonths'),
        ('Y', 'Yearly'),
    )

    pkg_type = models.CharField(max_length=1, choices=PACKAGE_TYPE_CHOICES)
    request_count = models.IntegerField()
    duration = models.CharField(max_length=1, choices=PACKAGE_DURATION_CHOICES)
    batch_size = models.FloatField()
    pkg_price = models.FloatField()

    def __str__(self):
        return self.pkg_type


from django.conf import settings



# Model to store the list of logged in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user')
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Allagencies(models.Model):
    name=models.CharField(max_length=5000, null=True, blank=True,unique=True)
    def __str__(self):
        return self.name

class City(models.Model):
    name=models.CharField(max_length=5000, null=True, blank=True,unique=True)

    # def __str__(self):
    #     return self.name

class County(models.Model):
    name=models.CharField(max_length=5000, null=True, blank=True,unique=True)

    # def __str__(self):
    #     return self.name



# class Notification_Detail(models.Model):
#     receiver_data=models.ForeignKey(User)
#     type_of_notification=models.CharField(max_length=5000,null=True,blank=True)
#     description=models.TextField(null=True,blank=True)
#     target=models.CharField(max_length=5000,null=True,blank=True)
#     read=models.BooleanField(default=False,blank=True)
#     isdeleted=models.BooleanField(default=False,blank=True)
#     timecreated=models.DateTimeField(auto_now_add=True,null=True)

