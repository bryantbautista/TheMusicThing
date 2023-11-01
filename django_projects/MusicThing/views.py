from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, RegistrationForm


# Create your views here.

def index(request):
    return render(request, 'index.html')

def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/')

def loginView(request):
    error = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data["username"], password = form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                error = "User not found."
        else:
            error = "Invalid input."
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form, "error":error})

def registerView(request):
    form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def home_page(request):
    return render(request, 'home_page.html')