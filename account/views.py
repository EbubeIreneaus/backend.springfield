from django.shortcuts import render
from authentication.models import Profile
from .serializers import accountSerialize
from.models import Account
from django.http import JsonResponse
# Create your views here.

def accountDetails(request, userId):

    try:
        account = Account.objects.get(profile__user__id = userId)
        serialized_account = accountSerialize(account)
        return JsonResponse(serialized_account.data, safe=False)
    except Account.DoesNotExist:
        return JsonResponse({'status':'failed', 'code':'account_not_found'})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'code': str(e)})
