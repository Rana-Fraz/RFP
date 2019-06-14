from rest_framework import serializers
from .models import  Bloginfo,BecomePartner,Notification_Detail

class BlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bloginfo
        fields = '__all__'




class BecomePartnerSerializers(serializers.ModelSerializer):
    class Meta:
        model = BecomePartner
        fields = '__all__'




class NotifySerializer(serializers.ModelSerializer):
    class Meta:
        model =Notification_Detail
        fields = ('id','description','type_of_notification','read','target')