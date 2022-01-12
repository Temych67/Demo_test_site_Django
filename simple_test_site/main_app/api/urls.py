from django.urls import path
from main_app import views

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'main_app'

urlpatterns = [
	# path('properties/update', update_account_view, name="update"),
	path('login/', obtain_auth_token, name="login"),
	path('registration/', views.registration_view, name="register"),
]