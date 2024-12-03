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

// Variables pour stocker les critères et le moyen de déplacement
let criteria = '';
let transport = '';

// Fonction pour ajouter des critères
function addCriteria() { 
    criteria = document.getElementById('criteriaInput').value;
    if (criteria) { 
        alert("Critères ajoutés : " + criteria + "\nMoyen de déplacement : " + transport); 
        // Vous pouvez ajouter ici le code pour enregistrer les critères dans la base de données
        // Exemple de code pour envoyer les critères à un serveur
        fetch('/save_criteria', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ criteria, transport }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });

        // Afficher les zones recherchées sur la carte
        showZones(criteria);
    } 
}

// Fonction pour afficher les zones recherchées sur la carte
function showZones(criteria) {
    // Exemple de données de zones
    const zones = [
        { name: 'Zone 1', lat: 48.8566, lng: 2.3522 },
        { name: 'Zone 2', lat: 48.8584, lng: 2.2945 },
    ];

    zones.forEach(zone => {
        L.marker([zone.lat, zone.lng]).addTo(map)
            .bindPopup(zone.name + '<br>Critères: ' + criteria)
            .openPopup();
    });
}

// Fonction pour afficher le champ de saisie des critères
function showCriteriaInput(iconId) {
    var criteriaInput = document.getElementById('criteriaInput');
    criteriaInput.style.display = 'block';
    criteriaInput.placeholder = 'Entrez vos critères pour ' + iconId;
}

// Ajouter des événements aux icônes de transport 
document.getElementById('bikeIcon').addEventListener('click', () => { 
    transport = 'vélo'; 
    alert("Moyen de déplacement sélectionné : Vélo"); 
    showCriteriaInput('vélo');
});
document.getElementById('carIcon').addEventListener('click', () => { 
    transport = 'voiture'; 
    alert("Moyen de déplacement sélectionné : Voiture"); 
    showCriteriaInput('voiture');
});
document.getElementById('busIcon').addEventListener('click', () => { 
    transport = 'bus'; 
    alert("Moyen de déplacement sélectionné : Bus"); 
    showCriteriaInput('bus');
}); 
document.getElementById('feethIcon').addEventListener('click', () => { 
    transport = 'pieds'; 
    alert("Moyen de déplacement sélectionné : pieds"); 
    showCriteriaInput('pieds');
}); 

// Ajouter un événement au bouton 
document.getElementById('saveCriteriaBtn').addEventListener('click', addCriteria);
