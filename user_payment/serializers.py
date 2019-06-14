from django.contrib.auth.models import User
from rest_framework import  serializers
from .models import Payment,PaymentCardInfo
from core.models import Packages,Register



class User1Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username' , 'first_name','last_name' )

class User2Serializer(serializers.ModelSerializer):
    user = User1Serializer()
    class Meta:
        model = Register
        fields = ['address','user']


class PackageSerializer(serializers.ModelSerializer):
    pkg_price=serializers.FloatField()
    class Meta:
        model = Packages
        # fields = '__all__'
        fields = ('pkg_type', 'duration', 'pkg_price',)

class PurchaseHistorySerializer(serializers.ModelSerializer):
    # pkg_fk = serializers.PrimaryKeyRelatedField(source='pkg_fk.pkg_type', read_only=True)
    #
    # class Meta:
    #     model = Payment
    #     fields = ('id','pay_date','end_date','is_paid','is_expired','request_count','pkg_fk')

    pkg_fk = PackageSerializer()
    reg_fk = User2Serializer()
    class Meta:
        model = Payment
        fields = ('id','pay_date','end_date','is_paid','is_expired','request_count','pkg_fk','reg_fk')

        # fields = '__all__'

class updateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCardInfo
        fields = (
        'name', 'expDate', 'pinCode', 'street_address', 'zipcode', 'city', 'state', 'country',
        'default', 'autopay')
        extra_kwargs = {'pinCode': {'required': False}}


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentCardInfo
        fields = ('id','name','number','cvc','expDate','pinCode','street_address','zipcode','city','state','country','default','card_type','autopay')
        extra_kwargs = {'pinCode': {'required': False}}

class CardPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentCardInfo
        fields = ('user','name','number','cvc','expDate','pinCode','street_address','zipcode','city','state','country','default','card_type','autopay','info')
        extra_kwargs={'pinCode':{'required':False}}
