from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput)
    verifyPassword = forms.CharField(label="Verify Password", max_length=30, widget=forms.PasswordInput)
