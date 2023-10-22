from rest_framework import serializers
from .models import Account
from authentication.serializers import profileSerial
class accountSerialize(serializers.ModelSerializer):
    profile = profileSerial()
    class Meta:
        model = Account
        fields = "__all__"