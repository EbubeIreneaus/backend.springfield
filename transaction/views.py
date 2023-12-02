import json
import random

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from authentication.models import Profile
from .models import Transaction
import string
from .serializers import transactionSerializer as ts
from account.models import Account
import re
from django.db import transaction
import datetime
from django.utils import timezone
import datetime
import time
class customException(Exception):
    pass


def validate_deposit(amount, plan):
    if not amount or amount == '' or amount is None or not plan or plan == '' or plan is None:
        return False
    if (50 <= amount <= 349) and plan != 'bronze':
        return False
    if (350 <= amount <= 899) and plan != 'silver':
        return False
    if (900 <= amount <= 4999) and plan != 'gold':
        return False
    if (5000 <= amount <= 14999) and plan != 'estate':
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
def validate_withdraw(amount, profileid, wallet_address):
    try:
        amount = int(amount)
        if re.search('[!@#$%^()-+=:;\'\"<>?~]', wallet_address):
            raise customException('Invalid Wallet Address')
        if type(amount) != int:
            raise customException('amount must be a number, undefined character given')

        account = Account.objects.get(profile__id=profileid)
        if account.balance < amount:
            raise customException('Insufficient Funds !!!')

    except Account.DoesNotExist:
        return {'status': 'failed', 'code': 'unidentified user please Sign In again!!!'}

    except customException as e:
        return {'status': 'failed', 'code': str(e)}
    except Exception as e:
        return {'status': 'failed', 'code': 'unknown error please try again later!!!'}
    return {'status':'true'}


def updateTransactions(userId):
    try:
        with transaction.atomic():
            now = timezone.now()
            ts = Transaction.objects.filter(profile__id=userId)
            tplan = {'bronze':0.2,'silver':0.4,'gold':0.6,'estate':0.8,'pro':1}
            for x in ts:
                if now >= x.end_date and x.progress == 'active':
                    trans = Transaction.objects.get(pk = x.pk)
                    account = Account.objects.get(profile__id = trans.profile.id)
                    earning = tplan[trans.plan] * trans.amount
                    trans.progress = 'completed'
                    account.balance += (trans.amount + earning)
                    account.active_investment -= trans.amount
                    account.Total_earnings += earning
                    trans.save()
                    account.save()
    except Exception as e:
        print(f'Could not update transaction {str(e)}')
    return True

class Transactions(APIView):
    def post(self, request):
        data = json.loads(request.body)
        key = generateKey(30)
        now = datetime.datetime.now()
        tplan = {'bronze': 24, 'silver': 48, 'gold': 72, 'estate': 48, 'pro': 96}
        expires = datetime.datetime.fromtimestamp(time.time()+(60 * 60 * tplan[data['plan']]))
        with transaction.atomic():
            try:
                try:
                    profile = Profile.objects.get(id=data['userId'])
                    account = Account.objects.select_for_update().get(profile__id = profile.id)
                except Profile.DoesNotExist:
                    return JsonResponse({'status': 'failed', 'code': 'user_not_found'})
                if 'plan' in data:
                    if not validate_deposit(amount=data['amount'], plan=data['plan']):
                        return JsonResponse({'status': 'failed', 'code': 'bad_data_integrity'})

                    if data['channel'] == 'balance' and account.balance >= data['amount']:
                        ts = Transaction(profile=profile, transact_id=key,plan=data['plan'], amount=data['amount'],
                                         channel=data['channel'], type='deposit', status=1, progress='active',
                                         start_date=now, end_date=expires)
                        account.active_investment = float(account.active_investment) + float(data['amount'])
                        account.balance = float(account.balance) - float(data['amount'])
                        ts.save()
                        account.save()
                    elif data['channel']== 'USDT' or data['channel']=='BTC':
                        Transaction.objects.create(profile=profile, transact_id=key, plan=data['plan'], amount=data['amount'],
                                               channel=data['channel'], type='deposit')
                else:
                    validate = validate_withdraw(amount=data['amount'], profileid=profile.id, wallet_address=data['wallet'])
                    if validate['status'] != 'true':
                        return JsonResponse({'status': 'failed', 'code':str(validate['code'])})
                    Transaction.objects.create(profile=profile, transact_id=key, amount=data['amount'],
                                               channel=data['channel'], address=data['wallet'], type='withdraw')
                return JsonResponse({'status': 'success'})
            except Exception as e:
                return JsonResponse({'status': 'failed', 'code': str(e)})

    def get(self, request):
        userId = request.GET.get('userId')
        if updateTransactions(userId):

            try:
                transactions = Transaction.objects.filter(profile__id=userId).order_by('-id')
                st = ts(transactions, many=True)
                return JsonResponse(st.data, safe=False)
            except Exception as e:
                return HttpResponse(str(e))
