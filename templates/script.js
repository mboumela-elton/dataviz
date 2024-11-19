// Initialisation de la carte
const map = L.map('map').setView([48.8566, 2.3522], 13); // Coordonnées de Paris

// Ajout d'une couche de tuiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

// Ajout d'un marqueur
const marker = L.marker([48.8566, 2.3522]).addTo(map);
marker.bindPopup('Bonjour, Paris !').openPopup();