from rest_framework import serializers
from .models import Transaction
from authentication.serializers import profileSerial
class transactionSerializer(serializers.ModelSerializer):
    profile = profileSerial()
    class Meta:
        model = Transaction
        fields = '__all__'