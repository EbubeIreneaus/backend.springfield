import json
import random

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from authentication.models import Profile
from .models import Transaction
import string
from .serializers import transactionSerializer as ts
def validate_deposit(amount, plan):
    if not amount or amount == '' or amount is None or not plan or plan == '' or plan is None:
        return False
    if (amount >= 50 and amount <= 349) and plan != 'bronze':
        return False
    if (amount >= 350 and amount <= 899) and plan != 'silver':
        return False
    if (amount >= 900 and amount <= 4999) and plan != 'gold':
        return False
    if (amount >= 5000 and amount <= 14999) and plan != 'estate':
        return False
    return True

def generateKey(length):
    key = ''
    for i in range(length):
        key += random.choice(string.ascii_letters + string.digits)
    try:
        t = Transaction.objects.get(transact_id=key)
        generateKey(length)
    except Transaction.DoesNotExist:
            pass
    return key

# Create your views here.
class Transactions(APIView):
    def post(self, request):
        data = json.loads(request.body)
        key = generateKey(30)
        if not validate_deposit(amount=data['amount'], plan=data['plan']):
            return JsonResponse({'status': 'failed', 'code': 'bad_data_integrity'})
        try:
            try:
                profile = Profile.objects.get(user__id=data['userId'])
            except Profile.DoesNotExist:
                return JsonResponse({'status': 'failed', 'code': 'user_not_found'})

            Transaction.objects.create(profile=profile, transact_id=key, plan=data['plan'], amount=data['amount'],
                                       channel=data['channel'], type='deposit')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'code': str(e)})

    def get(self, request):
        userId = request.GET.get('userId')
        try:
            transactions = Transaction.objects.filter(profile__user__id = userId)
            st = ts(transactions, many=True)
            return JsonResponse(st.data, safe=False)
        except Exception as e:
            return HttpResponse(str(e))