import requests
from geopy.distance import geodesic
import math

def fetch_schools(city_name):
    query = f"""
    [out:json];
    area["name"="{city_name}"]["admin_level"="8"];
    node["amenity"="school"](area);
    out body;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    response = requests.get(url, params={'data': query})
    
    if response.status_code == 200:
        data = response.json()
        return [{'name': school.get('tags', {}).get('name', 'Inconnu'),
                 'lat': school['lat'], 
                 'lon': school['lon']} for school in data['elements']]
    else:
        print("Erreur lors de la récupération des données :", response.status_code)
        return []

def fetch_train_stations(city_name):
    query = f"""
    [out:json];
    area["name"="{city_name}"]["admin_level"="8"];
    node["railway"="station"](area);
    out body;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    response = requests.get(url, params={'data': query})
    
    if response.status_code == 200:
        data = response.json()
        return [{'name': station.get('tags', {}).get('name', 'Inconnu'),
                 'lat': station['lat'], 
                 'lon': station['lon']} for station in data['elements']]
    else:
        print("Erreur lors de la récupération des données :", response.status_code)
        return []

def circle_intersection(lat1, lon1, r1, lat2, lon2, r2):
    # Fonction pour calculer les points d'intersection entre deux cercles
    R = 6371  # Rayon de la Terre en km
    dLat = (lat2 - lat1) * math.pi / 180
    dLon = (lon2 - lon1) * math.pi / 180

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c  # Distance entre les centres en km

    # Vérifier s'il y a une intersection
    if d > r1 + r2 or d < abs(r1 - r2):
        return []  # Pas d'intersection

    a1 = r1**2
    a2 = r2**2
    d1 = (a1 - a2 + d**2) / (2 * d)
    h = math.sqrt(a1 - d1**2)

    p2x = lon1 + d1 * (lon2 - lon1) / d
    p2y = lat1 + d1 * (lat2 - lat1) / d

    intersection1 = (p2y + h * (lon2 - lon1) / d, p2x + h * (lat2 - lat1) / d)
    intersection2 = (p2y - h * (lon2 - lon1) / d, p2x - h * (lat2 - lat1) / d)

    return [intersection1, intersection2]

def find_nearby_schools_and_stations(city_name, max_distance_km, r1, r2):
    schools = fetch_schools(city_name)
    stations = fetch_train_stations(city_name)
    city = search_location(city_name)
    
    nearby_pairs = []

    for school in schools:
        school_location = (school['lat'], school['lon'])
        for station in stations:
            station_location = (station['lat'], station['lon'])
            distance = geodesic(school_location, station_location).kilometers
            
            if distance <= max_distance_km:

                intersections = circle_intersection(school['lat'], school['lon'], r1, 
                                                    station['lat'], station['lon'], r2)
                
                nearby_pairs.append({
                    'latitude': city['latitude'],
                    'longitude': city['longitude'],
                    'display_name': city['display_name'],
                    'school_name': school['name'],
                    'school_lat': school['lat'],
                    'school_lon': school['lon'],
                    'station_name': station['name'],
                    'station_lat': station['lat'],
                    'station_lon': station['lon'],
                    'distance_km': distance,
                    'intersection1_lat': intersections[0][0],
                    'intersection1_lon': intersections[0][1],
                    'intersection1_lat': intersections[1][0],
                    'intersection1_lon': intersections[1][1]
                })
    
    return nearby_pairs

def search_location(query):
# URL de l'API Nominatim
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}"
    
    # Définir les en-têtes, y compris User-Agent
    headers = {
        'User-Agent': 'Dataviz/1.0 dataviz@ensea.fr'  # Remplacez avec votre nom d'application et votre email
    }

    try:
        # Effectuer la requête GET avec les en-têtes
        response = requests.get(url, headers=headers)
        
        # Convertir la réponse JSON en dictionnaire
        data = response.json()
        # Vérifier si des résultats ont été trouvés
        if data and len(data) > 0:
            # Prendre le premier résultat
            location = data[0]
            lat = location['lat']
            lon = location['lon']
            display_name = location['display_name']
            return {'latitude': lat, 'longitude': lon, 'display_name': display_name}
        else:
            return {'error': 'Location not found.'}
    except requests.RequestException as e:
        return {'error': f'Error fetching location data: {str(e)}'}
