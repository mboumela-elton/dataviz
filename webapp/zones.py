# COORDONNEES : [ LONGITUDE, LATITUDE ]

# IMPORTS

import json
import math
import gc
# pip install requests
import requests
# pip install shapely
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

# CHEMINS D'ACCES
communesjson = "./static/db/communes.geojson"
regionsjson = "./static/db/Recherche/regions.geojson"
sncfjson = "./static/db/gares.geojson"
crousjson = "./static/db/crous.geojson"
ecolejson = "./static/db/ecole.geojson"
universitejson = "./static/db/universite.geojson"
regionidfjson = "./static/db/regionidf.geojson"
busidfjson = "./static/db/bus-idf.geojson"
metroidfjson = "./static/db/metro-idf.geojson"

departementjson1, departementjson2 = "./static/db/Recherche/regions/", "/departements.geojson"
villejson1, villejson2 = "./static/db/Recherche/departements/", "/communes.geojson"

# communesjson = "../static/db/communes.geojson"
# regionsjson = "../static/db/Recherche/regions.geojson"
# sncfjson = "../static/db/gares.geojson"
# crousjson = "../static/db/crous.geojson"
# ecolejson = "../static/db/ecole.geojson"
# universitejson = "../static/db/universite.geojson"
# regionidfjson = "../static/db/regionidf.geojson"
# busidfjson = "../static/db/bus-idf.geojson"
# metroidfjson = "../static/db/metro-idf.geojson"

# departementjson1, departementjson2 = "../static/db/Recherche/regions/", "/departements.geojson"
# villejson1, villejson2 = "../static/db/Recherche/departements/", "/communes.geojson"

# OUVERTURE DE CERTAINS FICHIER JSON

with open(communesjson, "r") as f:
    datacommunes = json.load(f)

with open(regionsjson, "r") as f:
    dataregions = json.load(f)

with open(regionidfjson, "r") as f:
    dataregionidf = json.load(f)

# RECHERCHE DES POSITIONS DES LIEUX

def Recherchemot(lon,lat,recherche,rayon):
    """Recherche la liste des lieux correspondants au mot utilisé"""
    sortie = []  # Liste pour stocker les résultats

    query = f"""
    [out:json];
    {recherche}(around:{rayon},{lat},{lon});
    out body;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    response = requests.get(url, params={'data': query})
    
    if response.status_code == 200:
        data = response.json()
        
        for place in data.get('elements', []):
            sortie.append([place['lon'], place['lat']])  # Longitude avant latitude

    return sortie  # Retourne la liste des résultats

def Coordunique(Liste):
    Liste_unique = []
    for coord in Liste:
        if not coord in Liste_unique:
            Liste_unique.append(coord)
    return Liste_unique

def Distance_Haversine(coord1, coord2):
    """Calcul de la distance en mètres entre 2 coordonnées"""
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371000  # Rayon moyen de la Terre en mètres
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance en mètres

def Rayonrecherche(lon, lat, liste_coord_ville):
    """Recherche la distance la plus grande parmis un centre ville et les villes alentours"""
    rayon_max = 0
    coordrecherche = [lon,lat]
    for ville in liste_coord_ville:
        for coord in ville:
            distance = Distance_Haversine(coordrecherche,coord)
            if distance > rayon_max:
                rayon_max = distance
    return rayon_max

def testidf(ville):
    for feature in dataregionidf["features"]:
        code = feature["properties"]["code"]
        if ville == code: # Ville en Ile de France
            return True
    
    return False # Ville hors de l'ile de france

def recherche_sncf(liste_ville):
    """Recherche la liste des gares de train les plus proche à partir des coordonnées de la zone voulue"""

    with open(sncfjson, "r") as f:
        datasncf = json.load(f)

    # A compléter avec la recherche de coordonnées de gare de train
    liste_coord = []

    for feature in datasncf["features"]:
        if feature["properties"]["voyageurs"] == "O":
            coord = feature["properties"]["c_geo"]
            lon, lat = coord["lon"], coord["lat"]
            code = feature["properties"]["code_commune"]
            for ville in liste_ville:
                if ville == code:
                    liste_coord.append([lon,lat])
    
    del datasncf
    gc.collect()

    return Coordunique(liste_coord)

def recherche_metro(liste_ville_idf, liste_ville_hidf, lon, lat, rayon):
    """Recherche la liste des gares de métro et RER les plus proche à partir des coordonnées de la zone voulue"""
    
    with open(metroidfjson, "r") as f:
        datametroidf = json.load(f)

    # A compléter avec la recherche de la position d'une gare de métro
    liste_coord = []

    if len(liste_ville_idf) > 0:
        for feature in datametroidf["features"]:
            coord = feature["geometry"]["coordinates"]
            code = feature["properties"]["code_commune"]
            for ville in liste_ville_idf:
                if ville == code:
                    liste_coord.append(coord)
    
    del datametroidf
    gc.collect()

    if len(liste_ville_hidf) > 0:
        liste_coord += Recherchemot(lon,lat,'node["railway"="station"]["station"="subway"]',rayon)
        liste_coord += Recherchemot(lon,lat,'node["public_transport"="station"]["station"="subway"]',rayon)

    return Coordunique(liste_coord)

def recherche_ecole(liste_ville):
    """Recherche la liste des écoles les plus proche à partir des coordonnées de la zone voulue"""

    with open(ecolejson, "r") as f:
        dataecole = json.load(f)

    # A compléter avec la recherche de la position d'une école
    liste_coord = []

    for feature in dataecole["features"]:
        coord = feature["geometry"]
        code = feature["properties"]["code_commune"]
        for ville in liste_ville:
            if feature["geometry"] != None:
                if ville == code:
                    liste_coord.append(coord["coordinates"])
    
    del dataecole
    gc.collect()
    
    return Coordunique(liste_coord)

def recherche_universite(liste_ville):
    """Recherche la liste des universités proche à partir des coordonnées de la zone voulue"""

    with open(universitejson, "r") as f:
        datauniversite = json.load(f)
    
    # A compléter avec la recherche de la position d'une université
    liste_coord = []

    for feature in datauniversite["features"]:
        coord = feature["geometry"]["coordinates"]
        code = feature["properties"]["com_code"]
        for ville in liste_ville:
            if ville == code:
                liste_coord.append(coord)
    
    del datauniversite
    gc.collect()
    
    return Coordunique(liste_coord)

def recherche_crous(liste_ville):
    """Recherche la liste des crous proche à partir des coordonnées de la zone voulue"""

    with open(crousjson, "r") as f:
        datacrous = json.load(f)

    # A compléter avec la recherche de la position d'un crous
    liste_coord = []

    for feature in datacrous["features"]:
        coord = feature["geometry"]["coordinates"]
        code = feature["properties"]["code_commune"]
        for ville in liste_ville:
            if ville == code:
                    liste_coord.append(coord)
    
    del datacrous
    gc.collect()
    
    return Coordunique(liste_coord)

def recherche_parc(lon, lat, rayon):
    """Recherche la liste des parcs proche à partir des coordonnées de la zone voulue"""

    # A compléter avec la recherche de la position d'un parc
    liste_coord =  []
    liste_coord += Recherchemot(lon, lat, 'node["name"~"Parc",i]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["name"~"Jardin",i]', rayon)

    return Coordunique(liste_coord)

def recherche_pharmacie(lon, lat, rayon):
    """Recherche la liste des pharmacies proche à partir des coordonnées de la zone voulue"""

    # A compléter avec la recherche de la position d'une pharmacie
    liste_coord =  []
    liste_coord += Recherchemot(lon, lat, 'node["amenity"="pharmacy"]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["name"~"Pharmacie",i]', rayon)

    return Coordunique(liste_coord)

def recherche_boulangerie(lon, lat, rayon):
    """Recherche la liste des boulangerie proche à partir des coordonnées de la zone voulue"""

    # A compléter avec la recherche de la position d'une boulangerie
    liste_coord = []
    liste_coord += Recherchemot(lon, lat, 'node["shop"="bakery"]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["name"~"Boulangerie",i]', rayon)

    return Coordunique(liste_coord)

def recherche_medecin(lon, lat, rayon):
    """Recherche la liste des médecin proche à partir des coordonnées de la zone voulue"""

    # A compléter avec la recherche de la position d'un médecin
    liste_coord =  []
    liste_coord += Recherchemot(lon, lat, 'node["amenity"="doctors"]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["healthcare"="doctor"]', rayon)

    return Coordunique(liste_coord)

def recherche_bus(liste_ville_idf, liste_ville_hidf, lon, lat, rayon):
    """Recherche la liste des arrêt de bus proche à partir des coordonnées de la zone voulue"""

    with open(busidfjson, "r") as f:
        databusidf = json.load(f)

    # A compléter avec la recherche de la position d'un arrêt de bus
    liste_coord = []

    if len(liste_ville_idf) > 0:
        for feature in databusidf["features"]:
            coord = feature["geometry"]["coordinates"]
            code = feature["properties"]["code_insee"]
            for ville in liste_ville_idf:
                if ville == code:
                    liste_coord.append(coord)
    
    del databusidf
    gc.collect()
    
    if len(liste_ville_hidf) > 0:
        liste_coord += Recherchemot(lon, lat, 'node["highway"="bus_stop"]', rayon)
        liste_coord += Recherchemot(lon, lat, 'node["public_transport"="platform"]["bus"="yes"]', rayon)

    return Coordunique(liste_coord)

def recherche_supermarche(lon, lat, rayon):
    """Recherche la liste des supermarchés proche à partir des coordonnées de la zone voulue"""

    # A compléter avec la recherche de la position d'un supermarché
    liste_coord =  []
    liste_coord += Recherchemot(lon, lat, 'node["shop"="supermarket"]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["shop"="convenience"]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["name"~"Carrefour",i]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["name"~"Auchan",i]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["name"~"Leclerc",i]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["name"~"Casino",i]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["name"~"Lidl",i]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["name"~"Aldi",i]', rayon)

    return Coordunique(liste_coord)

def recherche_piscine(lon, lat, rayon):
    """Recherche la liste des piscine proche à partir des coordonnées de la zone voulue"""

    # A compléter avec la recherche de la position d'une piscine
    liste_coord =  []
    liste_coord += Recherchemot(lon, lat, 'node["sport"="swimming"]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["name"~"Piscine",i]', rayon)

    return Coordunique(liste_coord)

def recherche_sport(lon, lat, rayon):
    """Recherche la liste des salles de sports proche à partir des coordonnées de la zone voulue"""

    # A compléter avec la recherche de la position d'une salle de sport
    liste_coord =  []
    liste_coord += Recherchemot(lon, lat, 'node["leisure"="fitness_centre"]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["sport"="fitness"]', rayon)

    return Coordunique(liste_coord)

def recherche_cinema(lon, lat, rayon):
    """Recherche la liste des cinéma proche à partir des coordonnées de la zone voulue"""

    # A compléter avec la recherche de la position d'un cinéma
    liste_coord =  []
    liste_coord += Recherchemot(lon, lat, 'node["amenity"="cinema"]', rayon)
    liste_coord += Recherchemot(lon, lat, 'node["name"~"Cinéma",i]', rayon)

    return Coordunique(liste_coord)

# FONCTIONS POUR AVOIR LES SURFACES 2D A PARTIR D'UN POINT

def coord_surface(lon, lat, rayon):
    """Renvoie les coordonnées du contour de la surface à partir des coordonnées d'un point et du rayon en mètre"""
   
    R = 6371000     # Rayon moyen de la Terre en mètres
    coords = []     # Liste des coordonnées du contour 
    n = 32          # Nombre de points du contour de la surface

    for i in range(n):
        angle = 2 * math.pi * i / n  # Divise le cercle en n
        lat_offset = (rayon / R) * math.cos(angle)  # Déplacement en radians
        lon_offset = (rayon / (R * math.cos(math.radians(lat)))) * math.sin(angle)

        lat_cercle = lat + math.degrees(lat_offset)
        lon_cercle = lon + math.degrees(lon_offset)

        coords.append([lon_cercle, lat_cercle])

    return coords

def liste_surface(liste_coord, rayon):
    """Renvoie la liste des surfaces à partir de la liste de coordonnées et du rayon"""

    liste = [] # Liste des surfaces des zones voulues

    for coord in liste_coord:
        lon, lat = coord[0], coord[1]
        liste.append(coord_surface(lon, lat , rayon))
    
    return liste
    # Renvoie une liste de liste contenant les différentes surfaces associé à chaque coordonnées et rayon

def intersection_zone(zone1, zone2):
    """Détermine la zone d'intersection entre deux zones"""
    
    # Créer les polygones
    poly1, poly2 = Polygon(zone1), Polygon(zone2)
    
    # Vérifier la validité des polygones
    if not poly1.is_valid:
        poly1 = poly1.buffer(0)  # Correction de l'invalidité, généralement en créant un polygone valide
    
    if not poly2.is_valid:
        poly2 = poly2.buffer(0)  # Correction de l'invalidité, généralement en créant un polygone valide

    # Si poly1 contient totalement poly2
    if poly1.contains(poly2):  
        return zone2

    # Si poly2 contient totalement poly1
    if poly2.contains(poly1):  
        return zone1

    # Calculer l'intersection
    intersection = poly1.intersection(poly2)
    
    # Vérifier si l'intersection est vide
    if intersection.is_empty:
        return None
    
    # Si l'intersection est un polygone, retourner ses coordonnées extérieures
    if isinstance(intersection, Polygon):
        return list(intersection.exterior.coords)[:-1]  # Retirer le dernier point identique au premier

def liste_intersection_zone(liste1,liste2):
    """Détermine l'ensemble des intersections entre deux zone"""

    liste_intersection = []

    for zone1 in liste1:
        for zone2 in liste2:
            liste_intersection.append(intersection_zone(zone1,zone2))
    
    return [zone for zone in liste_intersection if zone is not None]

def simplification_coord(liste_intersection):
    """Simplifie les intersections, enlève les superpositions de zones"""

    # Convertir les zones en polygones Shapely
    polygones = [Polygon(zone) for zone in liste_intersection]

    # Étape 1 : Supprimer les polygones contenus dans d'autres
    polygones = [
        poly for poly in polygones 
        if not any(other.contains(poly) and other != poly for other in polygones)
    ]

    # Étape 2 : Fusionner les zones qui se chevauchent
    union_polygones = unary_union(polygones)

    # Vérifier si on a une liste de polygones ou un seul
    if union_polygones.geom_type == 'Polygon':
        liste_simplifiee = [list(union_polygones.exterior.coords)]
    else:  # Plusieurs polygones
        liste_simplifiee = [list(poly.exterior.coords) for poly in union_polygones.geoms]

    return liste_simplifiee 

# FONCTIONS POUR RECHERCHER UNE VILLE A PARTIR DES COORDONNEES

def recherche_region(lon, lat):
    """Renvoie le numéro de la région associé aux coordonnées"""
    
    point = Point(lon, lat)  # Point de shapely

    for feature in dataregions["features"]:
        coords = feature["geometry"]["coordinates"]
        
        # Assurer que nous avons bien un Polygone (et non un MultiPolygon)
        if feature["geometry"]["type"] == "Polygon":
            exterior = coords[0]  # Anneau extérieur
            holes = coords[1:] if len(coords) > 1 else []  # Trous éventuels
            polygon = Polygon(exterior, holes)  # Création correcte du polygone

            if polygon.contains(point):
                return feature['properties']['code']

    return 11  # Retourne None si aucune région trouvée

def recherche_departement(lon, lat, num):
    """Renvoie le numéro du département associé aux coordonnées"""
    
    departementjson = departementjson1 + str(num) + departementjson2
    with open(departementjson, "r") as f:
        datadepartement = json.load(f)

    point = Point(lon, lat)  # Point de shapely

    for feature in datadepartement["features"]:
        coords = feature["geometry"]["coordinates"]
        
        # Assurer que nous avons bien un Polygone (et non un MultiPolygon)
        if feature["geometry"]["type"] == "Polygon":
            exterior = coords[0]  # Anneau extérieur
            holes = coords[1:] if len(coords) > 1 else []  # Trous éventuels
            polygon = Polygon(exterior, holes)  # Création correcte du polygone

            if polygon.contains(point):
                return feature['properties']['code']

    return 95  # Retourne None si aucun département trouvée

def recherche_ville(lon,lat,num):
    """Renvoie le code communale insee de la ville associé aux coordonnées"""

    villejson = villejson1 + str(num) + villejson2

    with open(villejson, "r") as f:
        datavilles = json.load(f)

    point = Point(lon, lat)  # Point de shapely

    for feature in datavilles["features"]:
        coords = feature["geometry"]["coordinates"]
        
        # Assurer que nous avons bien un Polygone (et non un MultiPolygon)
        if feature["geometry"]["type"] == "Polygon":
            exterior = coords[0]  # Anneau extérieur
            holes = coords[1:] if len(coords) > 1 else []  # Trous éventuels
            polygon = Polygon(exterior, holes)  # Création correcte du polygone

            if polygon.contains(point):
                return feature['properties']['code'], exterior

    return 95127, [[2.03823,49.03373],[2.04006,49.03589],[2.03506,49.03871],[2.03185,49.03677],[2.02732,49.03766],[2.02527,49.03842],[2.02226,49.0385],[2.01583,49.03987],[2.01044,49.04385],[2.00705,49.04457],[2.00903,49.04672],[2.00833,49.04829],[2.00473,49.05024],[1.99997,49.05177],[2.00324,49.05379],[2.01001,49.05558],[2.0106,49.05612],[2.01531,49.05507],[2.02409,49.05423],[2.02777,49.0565],[2.02899,49.05601],[2.03858,49.05531],[2.04276,49.05425],[2.04658,49.05408],[2.04678,49.05619],[2.05472,49.055],[2.05472,49.05428],[2.06021,49.05312],[2.06535,49.05124],[2.06891,49.04954],[2.07222,49.04716],[2.07511,49.04502],[2.08058,49.04157],[2.08732,49.0383],[2.08295,49.03473],[2.08534,49.0333],[2.08418,49.0324],[2.08455,49.02907],[2.08962,49.0285],[2.09112,49.02733],[2.08964,49.02432],[2.09066,49.02397],[2.08847,49.021],[2.0855,49.01976],[2.08087,49.019],[2.0766,49.01926],[2.07546,49.018],[2.07298,49.01839],[2.06654,49.02134],[2.06097,49.02546],[2.05914,49.02474],[2.05777,49.02279],[2.05615,49.02319],[2.05011,49.02669],[2.04982,49.02878],[2.03823,49.03373]] # Retourne None si aucune région trouvée

def recherche_liste_ville(lon,lat):
    region = recherche_region(lon,lat)
    departement = recherche_departement(lon,lat,region)
    code, coord = recherche_ville(lon,lat,departement)
    liste_ville = [code]
    liste_coord = [coord]
    villepolygon = Polygon(coord)
    centroid = villepolygon.centroid
    cx, cy = centroid.x, centroid.y
    coord2 = [ (cx + (x - cx) * 1.2, cy + (y - cy) * 1.2)
                        for x, y in coord ]
    for (lon,lat) in coord2:
        region = recherche_region(lon,lat)
        departement = recherche_departement(lon,lat,region)
        code, coord = recherche_ville(lon,lat,departement)
        if not code in liste_ville:
            liste_ville.append(code)
            liste_coord.append(coord)
    return liste_ville, liste_coord

# PRIX ET COULEUR

def recherche_prix(liste_code):
    """Renvoie le prix moyen associé au code communale de la ville"""
    
    liste_prix = []

    for feature in datacommunes["features"]:
        for code in liste_code:
            if feature['properties']['code'] == code:
                liste_prix.append(feature['properties']['prixm2'])

    return liste_prix

def prix_couleur(prix):
    """Renvoie la couleure associé au prix"""
    if prix <= 1000:
        return "0x030565"
    elif prix > 1000 and prix <= 1250:
        return "0x1135F8"
    elif prix > 1250 and prix <= 1600:
        return "0x12C8EF"
    elif prix > 1600 and prix <= 2500:
        return "0x22C219"
    elif prix > 2500 and prix <= 4000:
        return "0xE0D618"
    elif prix > 4000 and prix <= 6500:
        return "0xF55906"
    elif prix > 6500 and prix <= 10000:
        return "0xA90101"
    elif prix > 10000:
        return "0x4E0000"

# RECHERCHE FINALE

def recherche_globale(lon, lat, distance_sncf=0, distance_metro=0, distance_ecole=0,
                                distance_universite=0, distance_crous=0, distance_parc=0,
                                distance_pharmacie=0, distance_boulangerie=0, distance_medecin=0,
                                distance_bus=0, distance_supermarche=0, distance_piscine=0,
                                distance_sport=0, distance_cinema=0):
    """Fonction finale"""

    liste_ville, liste_coord_ville = recherche_liste_ville(lon, lat) # Recherche les villes à partir de l'entrée utilisateur

    liste_ville_idf, liste_ville_hidf = [], [] # Sépare la liste des ville en 2
    for ville in liste_ville:
        if testidf(ville):
            liste_ville_idf.append(ville) # Liste des villes en Ile de France
        else:
            liste_ville_hidf.append(ville) # Liste des villes hors Ile de France

    liste_coord_sortie = liste_coord_ville

    Rayon = Rayonrecherche(lon,lat, liste_coord_ville)

    if distance_sncf > 0:
        liste_sncf = recherche_sncf(liste_ville)
        if len(liste_sncf) > 0:
            liste_surface_sncf = liste_surface(liste_sncf,distance_sncf)
            liste_coord_sortie = liste_intersection_zone(liste_surface_sncf, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)

    if distance_metro > 0:
        liste_metro = recherche_metro(liste_ville_idf, liste_ville_hidf, lon, lat, Rayon)
        if len(liste_metro) > 0:
            liste_surface_metro = liste_surface(liste_metro,distance_metro)
            liste_coord_sortie = liste_intersection_zone(liste_surface_metro, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)    

    if distance_ecole != 0:
        liste_ecole = recherche_ecole(liste_ville)
        if len(liste_ecole) > 0:
            liste_surface_ecole = liste_surface(liste_ecole,distance_ecole)
            liste_coord_sortie = liste_intersection_zone(liste_surface_ecole, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)

    if len(liste_coord_sortie) == 0:
        return []       # Pas de résultat renvoie une liste nulle et ne calcul pas les autres critères

    if distance_universite > 0:
        liste_universite = recherche_universite(liste_ville)
        if len(liste_universite) > 0:
            liste_surface_universite = liste_surface(liste_universite,distance_universite)
            liste_coord_sortie = liste_intersection_zone(liste_surface_universite, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)

    if distance_crous > 0:
        liste_crous = recherche_crous(liste_ville)
        if len(liste_crous) > 0:
            liste_surface_crous = liste_surface(liste_crous,distance_crous)
            liste_coord_sortie = liste_intersection_zone(liste_surface_crous, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)

    if distance_parc > 0:
        liste_parc = recherche_parc(lon, lat, Rayon)
        if len(liste_parc) > 0:
            liste_surface_parc = liste_surface(liste_parc,distance_parc)
            liste_coord_sortie = liste_intersection_zone(liste_surface_parc, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)

    if len(liste_coord_sortie) == 0:
        return []       # Pas de résultat renvoie une liste nulle et ne calcul pas les autres critères

    if distance_pharmacie > 0:
        liste_pharmacie = recherche_pharmacie(lon, lat, Rayon)
        if len(liste_pharmacie) > 0:
            liste_surface_pharmacie = liste_surface(liste_pharmacie,distance_pharmacie)
            liste_coord_sortie = liste_intersection_zone(liste_surface_pharmacie, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)

    if distance_boulangerie > 0:
        liste_boulangerie = recherche_boulangerie(lon, lat, Rayon)
        if len(liste_boulangerie) > 0:
            liste_surface_boulangerie = liste_surface(liste_boulangerie,distance_boulangerie)
            liste_coord_sortie = liste_intersection_zone(liste_surface_boulangerie, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)

    if distance_medecin > 0:
        liste_medecin = recherche_medecin(lon, lat, Rayon)
        if len(liste_medecin) > 0:
            liste_surface_medecin = liste_surface(liste_medecin,distance_medecin)
            liste_coord_sortie = liste_intersection_zone(liste_surface_medecin, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)
    
    if len(liste_coord_sortie) == 0:
        return []       # Pas de résultat renvoie une liste nulle et ne calcul pas les autres critères

    if distance_bus > 0:
        liste_bus = recherche_bus(liste_ville_idf, liste_ville_hidf, lon, lat, Rayon)
        if len(liste_bus) > 0:
            liste_surface_bus = liste_surface(liste_bus,distance_bus)
            liste_coord_sortie = liste_intersection_zone(liste_surface_bus, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)
    
    if distance_supermarche > 0:
        liste_supermarche = recherche_supermarche(lon, lat, Rayon)
        if len(liste_supermarche) > 0:
            liste_surface_supermarche = liste_surface(liste_supermarche,distance_supermarche)
            liste_coord_sortie = liste_intersection_zone(liste_surface_supermarche, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)
   
    if distance_piscine > 0:
        liste_piscine = recherche_piscine(lon, lat, Rayon)
        if len(liste_piscine) > 0:
            liste_surface_piscine = liste_surface(liste_piscine,distance_piscine)
            liste_coord_sortie = liste_intersection_zone(liste_surface_piscine, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)

    if len(liste_coord_sortie) == 0:
        return []       # Pas de résultat renvoie une liste nulle et ne calcul pas les autres critères

    if distance_sport > 0:
        liste_sport = recherche_sport(lon, lat, Rayon)
        if len(liste_sport) > 0:
            liste_surface_sport = liste_surface(liste_sport,distance_sport)
            liste_coord_sortie = liste_intersection_zone(liste_surface_sport, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)
    
    if distance_cinema > 0:
        liste_cinema = recherche_cinema(lon, lat, Rayon)
        if len(liste_cinema) > 0:
            liste_surface_cinema = liste_surface(liste_cinema,distance_cinema)
            liste_coord_sortie = liste_intersection_zone(liste_surface_cinema, liste_coord_sortie)
            liste_coord_sortie = simplification_coord(liste_coord_sortie)

    liste_coord_sortie = liste_intersection_zone(liste_coord_ville, liste_coord_sortie)

    liste_finale = []
    prix = recherche_prix(liste_ville) # Recherche le prix correspondant à la zone

    for i in range( len(liste_coord_sortie) ):
        test = 1
        for j in range( len(liste_coord_ville) ):
            Point1 = Point(liste_coord_sortie[i][0])
            Point2 = Point(liste_coord_sortie[i][1])
            Point3 = Point(liste_coord_sortie[i][2])
            polyville = Polygon(liste_coord_ville[j]) # Permet d'obtenir des objets polygones à partir des zones

            if test == 1:
                if polyville.contains(Point1):  # Si Polyville contient totalement Point1
                    liste_finale.append( [ prix_couleur(prix[j]), liste_coord_sortie[i], prix[j] ] )
                    test = 0
                elif polyville.contains(Point2):  # Si Polyville contient totalement Point2
                    liste_finale.append( [ prix_couleur(prix[j]), liste_coord_sortie[i], prix[j] ] )
                    test = 0
                elif polyville.contains(Point3):  # Si Polyville contient totalement Point3
                    liste_finale.append( [ prix_couleur(prix[j]), liste_coord_sortie[i], prix[j] ] )
                    test = 0
    for i in range(len(liste_finale)):
        liste_finale[i][1] = [[point[1], point[0]] for point in liste_finale[i][1]]

    return liste_finale # Renvoie la liste voulue

# print( recherche_globale(2.0608,49.0354,distance_sncf=2000,distance_universite=2000,distance_crous=2000,distance_bus=2000,distance_ecole=2000,distance_metro=2000, distance_boulangerie=2000, distance_cinema=2000, distance_medecin=2000, distance_sport=2000, distance_piscine=2000, distance_pharmacie=2000) )
print( recherche_globale(2.0608,49.0354,distance_sncf=2000,distance_ecole=2000)[0] )
