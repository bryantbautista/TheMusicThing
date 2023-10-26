from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms


# Create your views here.

def index(request):
    return render(request, 'index.html')
def helloworld2(request):
    return HttpResponse("Hello, world 2!")