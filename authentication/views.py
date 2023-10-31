import json
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse as JS, HttpResponse as HR
from django.contrib.auth.models import User
from .models import Profile
from account.models import Account
from mail import Mail
import string
import random


# Create your views here.
def generateProfileKey(length):
	key = ''
	for i in range(length):
		key += random.choice(string.ascii_letters + string.digits)
	try:
		p = Profile.objects.get(id=key)
		generateProfileKey(length)
	except Profile.DoesNotExist:
		pass
	return key


def generateKey(length):
	key = ''
	for i in range(length):
		key += random.choice(string.ascii_letters + string.digits)
	return key


def resend_link(request):
	userId = request.GET.get('userId', '')
	key = generateKey(80)
	try:
		profile = Profile.objects.get(id=userId)
		email = profile.user.email
	except Exception as e:
		return JS({'status': 'failed', 'code': str(e)})
	try:
		mail = Mail(subject="Email Verification")
		mail.recipient = [email]
		mail.html_message = '<div><div style="font-family: Arial, sans-serif;max-width: 600px;margin: 0 auto;' \
							'padding: 20px;border: 1px solid #e9e9e9;border-radius: 5px;"><h2> Dear User,' \
							' </h2 ><p>Thank you for registering on our website. Please click on the link below ' \
							'to verify your account:</p ><p><a href = "{link}"style = "display:' \
							' inline-block;background-color: #4caf50;border: none;color: white;padding: 10px 20px;' \
							'text-align: center;text-decoration: none;font-size: 16px;margin: 4px 2px;' \
							'cursor: pointer;border-radius: 5px;">Verify Account</a></p ><p>' \
							'If the button does not work, you can also copy and paste the following link into ' \
							'your browser: </p ><p> {link} </p ><p> We are excited ' \
							'to have you on board! </p></div>' \
							'</div>'.format(link=f'https://springfieldinvest.com/auth/verify/{profile.id}')
		mail.send_mail()
	except Exception as e:
		return HR(str(e))
	return JS({'status': 'success', 'userId': profile.id})

@csrf_exempt
def reset(request):
	data = json.loads(request.body)
	profile_id = request.headers.get('id')
	try:
		profile = Profile.objects.get(id=profile_id)
		user = User.objects.get(id=profile.user.id)
		user.set_password(data['password'])
		user.save()
		return JS({'status':'success'})
	except Exception as e:
		return JS({'status': 'failed', 'code':str(e)})

def psreset_link(request):
	username = request.GET.get('username', '')
	try:
		user = User.objects.get(username = username)
		email = user.email
		profile = Profile.objects.get(user__id = user.id)
	except Exception as e:
		return JS({'status': 'failed', 'code': str(e)})
	try:
		mail = Mail(subject="Password Reset")
		mail.recipient = [email]
		mail.html_message = '<div><div style="font-family: Arial, sans-serif;max-width: 600px;margin: 0 auto;' \
							'padding: 20px;border: 1px solid #e9e9e9;border-radius: 5px;"><h2> Dear User,' \
							' </h2 ><p>Thank you for investing with us. Please click on the link below ' \
							'to reset your password:</p ><p><a href = "{link}"style = "display:' \
							' inline-block;background-color: #4caf50;border: none;color: white;padding: 10px 20px;' \
							'text-align: center;text-decoration: none;font-size: 16px;margin: 4px 2px;' \
							'cursor: pointer;border-radius: 5px;">Reset Password</a></p ><p>' \
							'If the button does not work, you can also copy and paste the following link into ' \
							'your browser: </p ><p> {link} </p ><p> please disregard this email ' \
							'if you did not request for password resetting</p></div>' \
							'</div>'.format(link=f'https://springfieldinvest.com/auth/reset/{profile.id}')
		mail.send_mail()
	except Exception as e:
		return HR(str(e))
	return JS({'status': 'success'})


@csrf_exempt
def verify_account(request):
	data = json.loads(request.body)
	userId = data['key']
	try:
		profile = Profile.objects.get(id = userId)
		if profile.verified:
			return JS({'status':'failed'})
		profile.verified = True
		profile.save()
		return JS({'status':'success'})
	except Exception as e:
		return JS({'status': 'failed'})


class Auth(APIView):
	def get(self, request):
		username = request.GET.get('username', '')
		password = request.GET.get('password', '')
		try:
			user = authenticate(username=username, password=password)
			if user is not None:
				profile = Profile.objects.get(user__id = user.id)
				if profile.verified:
					return JS({'status': 'success', 'userId': profile.id})
				else:
					return JS({'status': 'unverified', 'userId': profile.id})
			else:
				return JS({'status': 'failed', 'code': "user not found"})
		except Exception as e:
			return JS({'status': 'failed', 'code': str(e)})

	def post(self, request):
		data = json.loads(request.body)
		profileId = generateProfileKey(60)
		try:
			user = User.objects.create_user(
				first_name=data['firstname'], last_name=data['lastname'], email=data['email'],
				username=data['username'], password=data['password'])
			profile = Profile.objects.create(id=profileId, user=user, country_code=data['code'],
											 phone=data['phone'], country=data['country'])
			Account.objects.create(profile=profile)
			return JS({'status': 'success', 'userId': profile.id})

		except IntegrityError as ie:
			try:
				user = User.objects.get(username=data['username'])
				return JS({'status': 'failed', 'code': "username_already_exist"})
			except User.DoesNotExist:
				pass
			try:
				user = User.objects.get(email=data['email'])
				return JS({'status': 'failed', 'code': "email_already_exist"})
			except User.DoesNotExist:
				pass

		except Exception as e:
			return JS({'status': 'failed', 'code': str(e)})

		# try:
		# 	mail = Mail(subject="Email Verification")
		# 	mail.recipient = [data['email']]
		# 	mail.html_message = '<div><div style="font-family: Arial, sans-serif;max-width: 600px;margin: 0 auto;' \
		# 						'padding: 20px;border: 1px solid #e9e9e9;border-radius: 5px;"><h2> Dear User,' \
		# 						' </h2 ><p>Thank you for registering on our website. Please click on the link below ' \
		# 						'to verify your account:</p ><p><a href = "{link}"style = "display:' \
		# 						' inline-block;background-color: #4caf50;border: none;color: white;padding: 10px 20px;' \
		# 						'text-align: center;text-decoration: none;font-size: 16px;margin: 4px 2px;' \
		# 						'cursor: pointer;border-radius: 5px;">Verify Account</a></p ><p>' \
		# 						'If the button does not work, you can also copy and paste the following link into ' \
		# 						'your browser: </p ><p> {link} </p ><p> We are excited ' \
		# 						'to have you on board! </p></div>' \
		# 						'</div>'.format(link=f'https://springfieldinvest.com/auth/verify/{key}')
		# 	mail.send_mail()
		# except Exception as e:
		# 	pass

