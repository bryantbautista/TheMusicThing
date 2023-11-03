from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput)

class RegistrationForm(UserCreationForm):
    emails = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")