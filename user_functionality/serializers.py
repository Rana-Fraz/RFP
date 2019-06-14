from django.contrib.auth.models import User
from rest_framework import  serializers
# from .models import Payment
from core.models import Packages,Register

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Register
        fields = '__all__'
class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packages
        # fields = '__all__'
        fields = ('pkg_type', 'duration', 'pkg_price',)

# class PurchaseHistorySerializer(serializers.ModelSerializer):
    # pkg_fk = serializers.PrimaryKeyRelatedField(source='pkg_fk.pkg_type', read_only=True)
    #
    # class Meta:
    #     model = Payment
    #     fields = ('id','pay_date','end_date','is_paid','is_expired','request_count','pkg_fk')

    # pkg_fk = PackageSerializer()
    # # reg_fk = UserSerializer()
    # class Meta:
    #     model = Payment
    #     fields = ('id','pay_date','end_date','is_paid','is_expired','request_count','pkg_fk')

        # fields = '__all__'
