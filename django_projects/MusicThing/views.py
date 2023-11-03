from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, RegistrationForm


# Create your views here.

def index(request):
    return render(request, 'index.html')

def logoutView(request):
    logout(request)
    return redirect('/')

def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username = form.cleaned_data["username"], password = form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "User not found.")
        else:
            messages.error(request, "Invalid input.")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})

def registerView(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    return render(request, "registration/register.html", {"form": form})