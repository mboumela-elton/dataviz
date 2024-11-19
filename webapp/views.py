from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request, *args, **kwargs):
    hello = 'Bonjour les amis'
    context = {
        'hello': hello,
    }
    return render(request, 'index.html', context)