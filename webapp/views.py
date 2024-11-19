from django.http import HttpResponse
from .forms import UserInfoForm
from django.shortcuts import render

# Create your views here.
def index(request, *args, **kwargs):
    hello = 'Bonjour les amis'
    context = {
        'hello': hello,
    }
    return render(request, 'index.html', context)

def user_info_view(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            # Afficher les données dans la console
            print("Nom :", form.cleaned_data['name'])
            print("Adresse :", form.cleaned_data['address'])
            # Vous pouvez aussi rediriger ou afficher un message ici
    else:
        form = UserInfoForm()
    
    return render(request, 'user_info.html', {'form': form})