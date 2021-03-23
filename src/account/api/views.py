from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import login, authenticate, logout
from account.api.serializers import RegistrationSerializer, ChangePasswordSerializer
from account.models import Account
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect
import re

# Register
# Url: https://<your-domain>/api/account/register
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):

	if request.method == 'POST':
		data = {}
		data_request = {}
		email = request.data.get('email', '0').lower()
		#std email validation
		if not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
			data['response'] = 'Please Provide Valid Email'
			return Response(data)
		elif validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data)

		firstname = request.data.get('user_firstname', '-')
		lastname = request.data.get('user_lastname', '-')

		if firstname == "-" or lastname == "-":
			data['response'] = 'Firstname Lastname not provided'
			return Response(data)
		else:
			firstname = firstname.capitalize()
			lastname = lastname.capitalize()
			username = firstname + ' ' + lastname
		if validate_username(username) != None:
			data['error_message'] = 'That username is already in use.'
			data['response'] = 'Error'
			return Response(data)
		
		#min 8 length 1uppercase 1 lowercase
		password = request.data.get('password', '0')
		password2 = request.data.get('password2', '0')
		if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$',password):
			data['response'] = "The Password must have minimum length of 8 characters 1 UpperCase Letter and 1 Lowercase Letter"
			return Response(data)
		password2 = request.data.get('password2', '0')
		if password2!=password:
			data['response'] = "password must match"
			return Response(data)

		user_phone_number = request.data.get('user_phone_number','0')
		if not re.match(r'^\+?1?\d{10}$',user_phone_number):
			data['response'] = "Provide Valid phone number"
			return Response(data)
		user_address = request.data.get('user_address','-')
		user_city = request.data.get('user_city','-')
		user_state = request.data.get('user_state','-')
		user_country = request.data.get('user_country','-')
		user_pincode = request.data.get('user_pincode','0')
		if not re.match(r'^\d{6}$',user_pincode):
			data['response'] = "Pincode not valid"
			return Response(data)
		data_request['email'] = email
		data_request['username'] = username
		data_request['user_firstname'] = firstname
		data_request['user_lastname'] = lastname
		data_request['user_phone_number'] = user_phone_number
		data_request['user_address'] = user_address
		data_request['user_city'] = user_city
		data_request['user_state'] = user_state
		data_request['user_country'] = user_country
		data_request['user_pincode'] = user_pincode
		data_request['password'] = password
		data_request['password2'] = password2
		print("data_request ==>",data_request)
		serializer = RegistrationSerializer(data=data_request)
		
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			data['pk'] = account.pk
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

def validate_email(email):
	account = None
	try:
		account = Account.objects.get(email=email)
	except Account.DoesNotExist:
		return None
	if account != None:
		return email

def validate_username(username):
	account = None
	try:
		account = Account.objects.get(username=username)
	except Account.DoesNotExist:
		return None
	if account != None:
		return username


# LOGIN
# URL: http://127.0.0.1:8000/api/account/login
class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.POST.get('username')
		password = request.POST.get('password')
		account = authenticate(email=email, password=password)
		if account:
			try:
				token = Token.objects.get(user=account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=account)
			context['response'] = 'Successfully authenticated.'
			context['pk'] = account.pk
			context['email'] = email.lower()
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)

def logout_view(request):
	logout(request)
	return redirect('login')


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def does_account_exist_view(request):

	if request.method == 'POST':
		email = request.data.get('email', '0').lower()
		data = {}
		try:
			account = Account.objects.get(email=email)
			data['response'] = email
		except Account.DoesNotExist:
			data['response'] = "Account does not exist"
		return Response(data)



class ChangePasswordView(UpdateAPIView):

	serializer_class = ChangePasswordSerializer
	model = Account
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			# Check old password
			if not self.object.check_password(serializer.data.get("old_password")):
				return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

			# confirm the new passwords match
			new_password = serializer.data.get("new_password")
			confirm_new_password = serializer.data.get("confirm_new_password")
			if new_password != confirm_new_password:
				return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

			# set_password also hashes the password that the user will get
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			return Response({"response":"successfully changed password"}, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





















