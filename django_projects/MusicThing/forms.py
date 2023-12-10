from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from MusicThing.models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = (
                 'email',
                 'username',
                )
class ProfileForm(ModelForm):
    class Meta:
         model = UserProfile
         fields = ('favorite_artist',)