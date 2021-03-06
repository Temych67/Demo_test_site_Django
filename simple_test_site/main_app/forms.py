from django import forms
from django.contrib.auth.forms import UserCreationForm
from main_app.models import User_Custom_Model
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = User_Custom_Model
        fields = ("email", "username", "password1", "password2")


class AuthenticattionForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User_Custom_Model
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login. Please check your email and password and try again")
