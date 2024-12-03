# import requests

# def get_city_coordinates(city_name):
#     # Requête Overpass pour récupérer la zone de la ville
#     query = f"""
#     [out:json];
#     area["name"="{city_name}"]["admin_level"="8"];
#     out center;
#     """
    
#     url = "https://overpass-api.de/api/interpreter"
#     response = requests.get(url, params={'data': query})
    
#     # Vérifiez si la requête a réussi
#     if response.status_code == 200:
#         data = response.json()
#         if data['elements']:
#             print(data['elements'][0]['center']['lat'])
#             latitude = data['elements'][0]['center']['lat']
#             longitude = data['elements'][0]['center']['lon']
#             return latitude, longitude
#         else:
#             print(f"Aucune donnée trouvée pour la ville '{city_name}'.")
#     else:
#         print("Erreur lors de la récupération des données :", response.status_code)

# # Demander à l'utilisateur d'entrer le nom d'une ville
# city = "Paris"
# get_city_coordinates(city_name=city)
import requests

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
        print(data)
        # Vérifier si des résultats ont été trouvés
        if data and len(data) > 0:
            # Prendre le premier résultat
            location = data[0]
            lat = location['lat']
            lon = location['lon']
            display_name = location['display_name']
            return {
                'latitude': lat,
                'longitude': lon,
                'display_name': display_name
            }
        else:
            return {'error': 'Location not found.'}
    except requests.RequestException as e:
        return {'error': f'Error fetching location data: {str(e)}'}

# Exemple d'utilisation
if __name__ == "__main__":
    query = "7 rue des chenes d'or"
    result = search_location(query)
    
    if 'error' in result:
        print(result['error'])
    else:
        print(f"Location found: {result['display_name']}")
        print(f"Latitude: {result['latitude']}, Longitude: {result['longitude']}")