import json
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse as JS, HttpResponse as HR
from django.contrib.auth.models import User
from .models import Profile
from account.models import Account
# Create your views here.

class Auth(APIView):
	def get(self, request):
		username = request.GET.get('username', '')
		password = request.GET.get('password', '')
		try:
			user = authenticate(username=username, password=password)
			if user is not None:
				return JS({'status': 'success', 'userId': user.id})
			else:
				return JS({'status': 'failed', 'code': "user not found"})
		except Exception as e:
			return JS({'status': 'failed', 'code': str(e)})

	def post(self, request):
		data = json.loads(request.body)
		try:
			user = User.objects.create_user(
				first_name=data['firstname'], last_name=data['lastname'], email=data['email'],
				username=data['username'], password=data['password'])
			profile = Profile.objects.create(user=user, country_code= data['code'],
											 phone=data['phone'], country=data['country'])
			Account.objects.create(profile=profile)
			return JS({'status':'success','userId':user.id})
		except IntegrityError as ie:
			try:
				user= User.objects.get(username = data['username'])
				return JS({'status': 'failed', 'code': "username_already_exist"})
			except User.DoesNotExist:
				pass
			try:
				user = User.objects.get(email = data['email'])
				return JS({'status': 'failed', 'code': "email_already_exist"})
			except User.DoesNotExist:
				pass

		except Exception as e:
			return JS({'status': 'failed', 'code':str(e)})
