from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Hello, world!")
def helloworld2(request):
    return HttpResponse("Hello, world 2!")
