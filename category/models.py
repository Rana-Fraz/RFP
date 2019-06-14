# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=30,blank=True)

    def __str__(self):
        return str(self.category_name)


class SubCategory(models.Model):
    sub_category_name= models.CharField(max_length=30,blank=True)
    category=models.ForeignKey(Category,related_name='category',blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.sub_category_name)



class M_vendor(models.Model):
    profileurl=models.CharField(max_length=5000,blank=True,null=True)

    def __str__(self):
        return  self.profileurl


class Mapping(models.Model):
    subcategory=models.ForeignKey(SubCategory,null=True,blank=True)
    subcategory_name=models.CharField(max_length=2000,null=True,blank=True)
    govt_Category=models.CharField(max_length=2000,null=True,blank=True)
    updated=models.CharField(max_length=1000,null=True,blank=True)
