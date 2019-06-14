from django.contrib.auth.models import User
from rest_framework import serializers
from core.models import *
class RegisterSerializer (serializers.Serializer):
    user = serializers.CharField()
    phone = serializers.CharField()
    about = serializers.CharField()

    class Meta:
        model = Register
        fields = {
            'user',
            'phone',
            'about',
        }

    def create(self, validated_data):
        return Register.objects.create(**validated_data)

class User1Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username' , 'first_name','last_name' )


class Register1Serializer(serializers.ModelSerializer):
    user = User1Serializer()

    class Meta:
        model = Register
        fields = ('user','address','company')

    def create(self, validated_data):
        modelB = Register.objects.create(**validated_data)
        return User.objects.create(**validated_data)

class EmailExistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

class UserNameCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model =  User

        fields = ('id' ,'username' , 'first_name' , 'last_name' , 'email')
class Register1Serializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Register
        fields = ('user','address','company','zipcode','city','country','state','phone_no','newsletter','user_preference','state_preference','city_preference','county_preference','agency_preference')

    def create(self, validated_data):
        modelB = Register.objects.create(**validated_data)
        return User.objects.create(**validated_data)


class Register3Serializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Register
        fields = ('user','newsletter','user_preference','state_preference','city_preference','county_preference','agency_preference')

    def create(self, validated_data):
        modelB = Register.objects.create(**validated_data)
        return User.objects.create(**validated_data)

class Register2Serializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Register
        fields = ('user','address','company','zipcode','city','country','state','phone_no')

    def create(self, validated_data):
        modelB = Register.objects.create(**validated_data)
        return User.objects.create(**validated_data)

class AllagenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allagencies
        fields = '__all__'


class CitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'

