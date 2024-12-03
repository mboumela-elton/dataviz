import math
import requests

def haversine(lat1, lon1, lat2, lon2):
    # Convertir les degrés en radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Calculer les différences
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    # Appliquer la formule de Haversine
    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    # Rayon de la Terre en kilomètres
    r = 6371

    # Calculer la distance
    distance = r * c
    return distance

def fetch_train_stations(city_name):
    # Requête Overpass pour récupérer les gares de la ville
    query = f"""
    [out:json];
    area["name"="{city_name}"]["admin_level"="8"];
    node["railway"="station"](area);
    out body;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    response = requests.get(url, params={'data': query})
    
    # Vérifiez si la requête a réussi
    if response.status_code == 200:
        data = response.json()
        stations = data['elements']

        # Afficher les gares
        if stations:
            return stations
            
            # print(f"Gares dans {city_name} :")
            # for station in stations:
            #     name = station.get('tags', {}).get('name', 'Inconnu')
            #     lat = station['lat']
            #     lon = station['lon']
            #     print(f"Nom: {name}, Latitude: {lat}, Longitude: {lon}")
        else:
            print(f"Aucune gare trouvée dans {city_name}.")
    else:
        print("Erreur lors de la récupération des données :", response.status_code)


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
