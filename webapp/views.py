from django.shortcuts import render
from .utils import search_location, find_nearby_schools_and_stations
from .zones import recherche_globale
radius_options = [100, 250, 500, 750, 1000, 1500, 3000]

def map_view(request):
    context = {
        # 'latitude': 48.8566,
        # 'longitude': 2.3522,
        'latitude' : 49.0365,
        'longitude' : 2.0603,
        # 'display_name': 'Paris',
        'display_name': 'Cergy',
        'zones': [],
        'message': '',
        'r1': 0,
        'r2': 0,
    }
    
    if request.method == 'POST':
        city = request.POST.get('city')
        location_data = search_location(city) 
        
        if location_data and 'latitude' in location_data and 'longitude' in location_data:
            context['latitude'] = location_data['latitude']
            context['longitude'] = location_data['longitude']
            context['display_name'] = location_data.get('display_name', city)
        else:
            context['message'] = 'Location not found.'

        if request.POST.get('school') and request.POST.get('station'):
            radius_school = radius_options[int(request.POST.get('school'))]
            radius_station = radius_options[int(request.POST.get('station'))]
            max_radius = max(radius_school, radius_station)
            city_name = city.split(',', 1)[0]
            # nearby_zones = find_nearby_schools_and_stations(city_name, max_radius, radius_school, radius_station)
            nearby_zones = recherche_globale(lon=location_data['longitude'], lat=location_data['latitude'] , distance_sncf=radius_station , distance_ecole=radius_school )
            context['zones'] = nearby_zones
            # context['r1'] = radius_school * 1000
            # context['r1'] = radius_station * 1000

    return render(request, 'index.html', context)