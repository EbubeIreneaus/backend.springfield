from rest_framework import serializers
from .models import Transaction

class transactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'