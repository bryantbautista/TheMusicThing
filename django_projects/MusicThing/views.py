from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    context = {
        'test_var':1
    }
    return render(request, 'index.html', context)
def helloworld2(request):
    return HttpResponse("Hello, world 2!")

