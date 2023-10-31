import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from transaction.models import Transaction
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from transaction.models import Transaction
from transaction.serializers import transactionSerializer
# Create your views here.
def getTransaction(request):
    key = request.headers.get('session-key',"hello world")
    tid = request.GET.get('tId')
    if key != settings.ADMIN_KEY:
        return JsonResponse({'status':'failed', 'code':'invalid Session Key'})
    try:
        transaction = Transaction.objects.get(transact_id = tid)
        serialized_data = transactionSerializer(transaction, many=False)
        return JsonResponse(serialized_data.data, safe=False)
    except Exception as e:
        return JsonResponse({'status':'failed'})




@csrf_exempt
def auth(request):
    data = json.loads(request.body)
    password = data['password']
    if settings.ADMIN_PASS == password:
        return JsonResponse({'status': 'success', 'key': str(settings.ADMIN_KEY)})
    return JsonResponse({'status':'failed'})


@csrf_exempt
def approveTransaction(request):
    data = json.loads(request.body)
    key = request.headers.get('session-key', "")
    tid = data['tId']
    if key != settings.ADMIN_KEY:
        return JsonResponse({'status': 'failed', 'code': 'invalid Session Key'})
    try:
        transaction = Transaction.objects.get(transact_id=tid)
        transaction.status = 1
        transaction.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'failed'})


def rejectTransaction(request):
    data = json.loads(request.body)
    key = request.headers.get('session-key', "")
    tid = data['tId']
    if key != settings.ADMIN_KEY:
        return JsonResponse({'status': 'failed', 'code': 'invalid Session Key'})
    try:
        transaction = Transaction.objects.get(transact_id=tid)
        return JsonResponse({'status': 'succed'})
    except Exception as e:
        return JsonResponse({'status': 'failed'})