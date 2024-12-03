from django.http import HttpResponse
import requests
from .forms import UserInfoForm
from django.shortcuts import render

from .utils import search_location

# Create your views here.

def map_view(request):
    # Contexte par défaut avec des données de Paris
    context = {
        'latitude': 48.8566,  # Latitude de Paris
        'longitude': 2.3522,   # Longitude de Paris
        'display_name': 'Paris'
    }
    
    if request.method == 'POST':
        query = request.POST.get('city')  # Obtenez la requête de l'utilisateur
        print(query)
        if query:
            location_data = search_location(query)  # Appelez la fonction pour rechercher la localisation
            if location_data and 'latitude' in location_data and 'longitude' in location_data:
                # Mettre à jour le contexte avec les nouvelles coordonnées
                context['latitude'] = location_data['latitude']
                context['longitude'] = location_data['longitude']
                context['display_name'] = location_data['display_name']
            else:
                context['message'] = 'Location not found.'  # Ajoutez un message d'erreur au contexte

    return render(request, 'index.html', context)

# def user_info_view(request):
#     if request.method == 'POST':
#         form = UserInfoForm(request.POST)
#         if form.is_valid():
#             # Afficher les données dans la console
#             print("Nom :", form.cleaned_data['name'])
#             print("Adresse :", form.cleaned_data['address'])
#             # Vous pouvez aussi rediriger ou afficher un message ici
#     else:
#         form = UserInfoForm()
    
#     return render(request, 'user_info.html', {'form': form})