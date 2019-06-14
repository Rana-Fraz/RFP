from django.db import models
from django.utils import timezone
from category.models import *
from django.contrib.auth.models import User

# Create your models here.

# Start Governments Bids
class GovernmentsBidsUser(models.Model):
    profile_url = models.CharField(max_length=1000, null=True)

class GovernmentBidsProfile(models.Model):
    governmentbidsusers = models.ForeignKey(GovernmentsBidsUser)
    rfpkey = models.CharField(max_length=50, null=True)
    profileurl = models.CharField(max_length=1000, null=True)
    title = models.CharField(max_length=1000, null=True)
    bid_type = models.CharField(max_length=200, null=True) #
    agency_type = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, default="Uncategorized")
    state = models.CharField(max_length=80, null=True) #
    date_entered = models.CharField(max_length=50, null=True)
    new_date_entered = models.CharField(max_length=50, null=True)
    due_date = models.CharField(max_length=50, null=True)
    new_due_date = models.CharField(max_length=50, null=True)
    agency = models.CharField(max_length=200, null=True)
    deescription = models.TextField(null=True)
    rfp_number = models.CharField(max_length=200, null=True)
    web_info = models.CharField(max_length=1000,null=True) #
    email = models.CharField(max_length=100,null=True)
    naics = models.CharField(max_length=500,null=True)
    rfp_reference = models.CharField(max_length=100,null=True)
    work_performance = models.TextField(null=True)
    city_or_county = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=50, null=True)
    buyer = models.CharField(max_length=100, null=True)
    award_date = models.CharField(max_length=100, null=True)
    seoTitleUrl = models.CharField(max_length=1000, blank=True)
    timestamp = models.DateTimeField(null=True,auto_now_add=True)
    contact = models.TextField(blank=True)
    descriptionTag = models.TextField(null=True)
    new_category = models.ForeignKey(Category, related_name='newcategory', blank=True, on_delete=models.CASCADE, null=True)
    sub_category = models.ForeignKey(SubCategory, related_name='subcategory', blank=True, on_delete=models.CASCADE,null=True)

# End Government Models


class DataCleaning_GovernmentBidsProfile(models.Model):
    governmentbidsusers = models.ForeignKey(GovernmentsBidsUser,related_name='user')
    rfpkey = models.CharField(max_length=50, null=True)
    profileurl = models.CharField(max_length=1000, null=False,unique=True)
    title = models.CharField(max_length=1000, null=True)
    bid_type = models.CharField(max_length=200, null=True) #
    agency_type = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, default="Uncategorized")
    state = models.CharField(max_length=80, null=True) #
    date_entered = models.CharField(max_length=50, null=True)
    new_date_entered = models.CharField(max_length=50, null=True)
    due_date = models.CharField(max_length=50, null=True)
    new_due_date = models.CharField(max_length=50, null=True)
    agency = models.CharField(max_length=200, null=True)
    deescription = models.TextField(null=True)
    rfp_number = models.CharField(max_length=200, null=True)
    web_info = models.CharField(max_length=1000,null=True) #
    email = models.CharField(max_length=100,null=True)
    naics = models.CharField(max_length=500,null=True)
    rfp_reference = models.CharField(max_length=100,null=True)
    work_performance = models.TextField(null=True)
    city_or_county = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=50, null=True)
    buyer = models.CharField(max_length=100, null=True)
    award_date = models.CharField(max_length=100, null=True)
    seoTitleUrl = models.CharField(max_length=1000,unique=True)
    timestamp = models.DateTimeField(null=True,auto_now_add=True)
    contact = models.TextField(blank=True)
    descriptionTag = models.TextField(null=True)
    new_category = models.ForeignKey(Category, related_name='testcategory', blank=True, on_delete=models.CASCADE, null=True)
    sub_category = models.ForeignKey(SubCategory, related_name='testsubcategory', blank=True, on_delete=models.CASCADE,null=True)





# Start Models
class RFPMartUser(models.Model):
    profile_url = models.CharField(max_length=1000, null=True)

class RFPMartUserProfile(models.Model):
    governmentbidsusers = models.ForeignKey(RFPMartUser)
    profileurl = models.CharField(max_length=1000, null=True)
    title = models.CharField(max_length=1000, null=True)
    bid_type = models.CharField(max_length=1000, null=True) #
    agency_type = models.CharField(max_length=1000, null=True)
    category = models.CharField(max_length=1000, null=True)
    state = models.CharField(max_length=1000, null=True) #
    date_entered = models.CharField(max_length=1000, null=True)
    due_date = models.CharField(max_length=1000, null=True)
    agency = models.CharField(max_length=1000, null=True)
    deescription = models.TextField(null=True)
    rfp_number = models.CharField(max_length=1000, null=True)
    web_info = models.CharField(max_length=1000,null=True) #
    email = models.CharField(max_length=1000,null=True)
    naics = models.CharField(max_length=1000,null=True)
    rfp_reference = models.CharField(max_length=1000,null=True)

class RFPGurusStates(models.Model):
    state = models.CharField(max_length=1000, null=True)
    icon_image=models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.icon_image

class RFP_County(models.Model):
    state = models.ForeignKey(RFPGurusStates)
    county=models.CharField(max_length=2000, null=True , blank=True)

class RFP_City(models.Model):
    county = models.ForeignKey(RFP_County)
    city=models.CharField(max_length=2000, null=True , blank=True)
    population = models.CharField(max_length=2000, null=True, blank=True)




class RFPGurusMainCategory(models.Model):
    category = models.CharField(max_length=1000, null=True)
    icon_image=models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.category


class allWebsitesLink(models.Model):
    link = models.CharField( unique=True, max_length=1000)
    state = models.CharField(max_length=1000 , null=True)
    city_county = models.CharField(max_length=1000 , null=True)

class rfpWebsitesLink(models.Model):
    link = models.CharField(max_length=1000, unique=True)
    parentlink = models.CharField(max_length=1000, unique=True)
    state = models.CharField(max_length=1000, null=True)
    city_county = models.CharField(max_length=1000, null=True)
    city = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return 'Link ' + self.link + " ParentLink " + self.state + " State " + str(self.state) + " County " + str(self.city_county) + " City " + str(self.city)




class UsaStates(models.Model):
        state = models.CharField(primary_key=True, max_length=1000, unique=True, db_index=False)

class StatesCityCounty(models.Model):
        state = models.ForeignKey(UsaStates)
        city = models.CharField(unique=True, max_length=1000, null=True)



class StateCityCounty(models.Model):
    state = models.CharField(max_length=50, null=False)
    city = models.CharField( max_length=100, null=True)
    county = models.CharField(max_length=100, null=True)
    population = models.CharField(max_length=10, null=True)
    def __str__(self):
        return 'State '+ self.state + ' County '+ str(self.county) + ' City '+ str(self.city) + ' Population ' + str(self.population)

class VendorsContact(models.Model):
    email = models.CharField(unique=True, max_length=1000)
    name = models.CharField(max_length=1000, null=True)
    address = models.CharField(max_length=1000 , null=True)
    fax = models.CharField(max_length=1000 , null=True)
    phone = models.CharField(max_length=1000, null=True)


class Contact(models.Model):
    name = models.CharField(max_length=1000, null=True)
    email = models.EmailField(unique=False)
    phone = models.CharField(max_length=1000, null=True)
    message = models.TextField(max_length=1000 , null=True)

    def __str__(self):
        return self.name + ' , ' + self.email + ' , ' + self.phone + ' , ' + self.message

class Subscribers(models.Model):
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.email

class UnsubscriberQuery(models.Model):
    email = models.EmailField()
    comments = models.TextField(null=True)


class UserWishlist(models.Model):
    wrfp = models.ForeignKey(DataCleaning_GovernmentBidsProfile)
    user = models.ForeignKey(User, default='')

    def __str__(self):
        return self.wrfp.title

class FPDS_DATA(models.Model):
    awardId = models.CharField(max_length=100, null=True)
    awardType = models.CharField(max_length=100, null=True)
    link = models.TextField(blank=True)
    venddorName = models.CharField(max_length=200, null=True)
    contractingAgency = models.CharField(max_length=100, null=True)  #
    dateSigned = models.CharField(max_length=100, null=True)
    actionObligation = models.CharField(max_length=50, null=True, default="Uncategorized")
    referenceIDV = models.CharField(max_length=100, null=True)  #
    contracttingOffice = models.CharField(max_length=500, null=True)
    naicsCode = models.CharField(max_length=500, null=True)
    pscCode = models.CharField(max_length=500, null=True)
    vendorCity = models.CharField(max_length=100, null=True)
    vendorDuns = models.CharField(max_length=50, null=True)
    vendorState = models.CharField(max_length=50, null=True)  #
    vendorZip = models.CharField(max_length=50, null=True)
    globalVendorName = models.CharField(max_length=200, null=True)
    globalDunsNumber = models.CharField(max_length=50, null=True)

class NEWRFPLINK(models.Model):
    parent = models.TextField(unique=True)
    link   = models.TextField()
    extra  = models.TextField(null=True)
    state  = models.TextField(null=True)
    county = models.TextField(null=True)
    city   = models.TextField(null=True)
    query  = models.TextField(null=True)


# class Notification_Detail(models.Model):
#     receiver=models.ForeignKey(User)
#     type_of_notification=models.CharField(max_length=5000,null=True,blank=True)
#     description=models.TextField(null=True,blank=True)
#     target=models.CharField(max_length=5000,null=True,blank=True)
#     read=models.NullBooleanField(default=None,blank=True)
#     isdeleted=models.NullBooleanField(default=None,blank=True)
#     timecreated=models.DateTimeField(auto_now_add=True,null=True)



