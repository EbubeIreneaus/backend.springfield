from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class UserSerializ(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email']

class profileSerial(serializers.ModelSerializer):
    user = UserSerializ()
    class Meta:
        model = Profile
        fields = '__all__'
