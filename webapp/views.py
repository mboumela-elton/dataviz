from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request, *args, **kwargs):
    hello = 'Welcome to our first page'
    context = {
        'hello': hello,
    }
    return render(request, 'index.html', context)