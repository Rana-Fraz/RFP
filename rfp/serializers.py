from rest_framework import serializers
from .models import DataCleaning_GovernmentBidsProfile, RFPGurusMainCategory, VendorsContact,UserWishlist,RFPGurusStates
from django.contrib.auth.models import User



class DataCleaning_GovernmentBidsProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = DataCleaning_GovernmentBidsProfile
        # fields = '__all__'
        # fields = ('id','rfp_number','title','category','state','date_entered','due_date' )
        fields = ('id', 'rfpkey','rfp_number', 'title','deescription','descriptionTag','category', 'state','agency', 'date_entered', 'due_date','web_info','rfp_reference','seoTitleUrl')

# class GovernmentBidsSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = DataCleaning_GovernmentBidsProfile
#         fields = ('id','rfpkey', 'rfp_number', 'title','deescription','category', 'state', 'date_entered', 'due_date')


class CityBidsSerializers(serializers.ModelSerializer):
    class Meta:
        model = DataCleaning_GovernmentBidsProfile
        fields = ('id','rfpkey', 'rfp_number', 'title','deescription','descriptionTag','category', 'state','agency', 'date_entered', 'due_date','web_info','rfp_reference','seoTitleUrl')


class GovernmentBidsSerializers(serializers.ModelSerializer):
    class Meta:
        model = DataCleaning_GovernmentBidsProfile
        fields = ('id','rfpkey', 'rfp_number', 'title','deescription','descriptionTag','category', 'state','agency', 'date_entered', 'due_date','web_info','rfp_reference','seoTitleUrl')
 # fields = '__all__'


class SubGovernmentBidsSerializers(serializers.ModelSerializer):
    class Meta:
        model = DataCleaning_GovernmentBidsProfile
        fields = (
        'id', 'rfpkey','rfp_number', 'title', 'deescription','descriptionTag' ,'category', 'state', 'date_entered', 'due_date','seoTitleUrl','agency')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        icon_image=serializers.CharField()
        model = RFPGurusMainCategory
        fields = ('category','icon_image')

class stateSerializer(serializers.ModelSerializer):
    class Meta:
        icon_image=serializers.CharField()
        model = RFPGurusStates
        fields = ('state','icon_image')



class GovernmentBidsSerializersForSubscribers(serializers.ModelSerializer):
    class Meta:
        model = DataCleaning_GovernmentBidsProfile
        fields = ('id','rfpkey', 'rfp_number', 'title','deescription','descriptionTag','category', 'state','agency', 'date_entered', 'due_date','web_info','rfp_reference','seoTitleUrl')
        # fields =  '__all__'

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataCleaning_GovernmentBidsProfile
        fields = ('state',)
class ContactSeializer(serializers.ModelSerializer):
    class Meta:
        model = VendorsContact
        fields = ('name','email','phone','address')

class WishListSerializer(serializers.ModelSerializer):
    wrfp = SubGovernmentBidsSerializers(read_only=True)
    class Meta:
        model = UserWishlist
        fields = '__all__'
class WishListPostSerializer(serializers.ModelSerializer):
    wrfp = DataCleaning_GovernmentBidsProfile()
    user = User()

    class Meta:
        model =  UserWishlist
        fields = ('user', 'wrfp')


class GovernmentBids_emailSerializers(serializers.ModelSerializer):
    class Meta:
        model = DataCleaning_GovernmentBidsProfile
        fields = ('title','category', 'state','agency', 'date_entered', 'due_date','seoTitleUrl')