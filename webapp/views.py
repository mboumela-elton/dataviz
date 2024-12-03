from django.http import HttpResponse
from django.shortcuts import render

from .utils import search_location, find_nearby_schools_and_stations

radiusOptions = [0.5, 1, 5, 10, 25, 35, 50]

def map_view(request):
    # Contexte par défaut avec des données de Paris
    context = {
        'latitude': 48.8566,  # Latitude de Paris
        'longitude': 2.3522,   # Longitude de Paris
        'display_name': 'Paris'
    }
    
    if request.method == 'POST':
        city = request.POST.get('city')  # Obtenez la requête de l'utilisateur
        location_data = search_location(city) 
        
        if request.POST.get('city'):
            print(location_data)
            if location_data and 'latitude' in location_data and 'longitude' in location_data:
                # Mettre à jour le contexte avec les nouvelles coordonnées
                context = location_data
            else:
                context['message'] = 'Location not found.'  # Ajoutez un message d'erreur au contexte
        if request.POST.get('school'):
            r1 = radiusOptions[int(request.POST.get('school'))]
            r2 = radiusOptions[int(request.POST.get('station'))]
            d = (r1+r2)/2
            city_name = city.split(',', 1)[0]
            find = find_nearby_schools_and_stations(city_name, 3, 5, 5)
            context = location_data | { 'zones' : find}
                
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