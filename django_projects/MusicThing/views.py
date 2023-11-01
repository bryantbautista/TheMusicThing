from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django import forms


# Create your views here.

def index(request):
    context = {
        'test_var':1
    }
    return render(request, 'index.html', context)

def helloworld2(request):
    return HttpResponse("Hello, world 2!")

def logoutaccount(request):
    logout(request)
    return HttpResponseRedirect('/')