from django.urls import path
from account.api.views import(
	registration_view,
	ObtainAuthTokenView,
	does_account_exist_view,
	ChangePasswordView,
	logout_view
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'

urlpatterns = [
	path('check_if_account_exists/', does_account_exist_view, name="check_if_account_exists"),
	path('change_password/', ChangePasswordView.as_view(), name="change_password"),
 	path('login', ObtainAuthTokenView.as_view(), name="login"), 
	path('logout', logout_view, name="logout"),
	path('register', registration_view, name="register"),

]