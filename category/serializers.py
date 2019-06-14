from rest_framework import serializers
from rfp.models import *



class CategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentBidsProfile
        fields = ('category',)


