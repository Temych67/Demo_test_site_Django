from django import forms
from django.contrib.auth.forms import UserCreationForm
from main_app.models import User_Custom_Model



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = User_Custom_Model
        fields = ("email", "username", "password1", "password2")
