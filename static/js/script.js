// Initialiser la carte
var map = L.map("map").setView([latitude, longitude], 13); // Coordonnées de Paris
var currentCircle = null; // Variable to hold the circle for updating

// Ajouter une couche de tuiles (OpenStreetMap)
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// Vérification et ajout du marqueur
L.marker([latitude, longitude])
  .bindPopup(`<b>${display_name}</b>`)
  .addTo(map);
// Radius options
const radiusOptions = [0.5, 1, 5, 10, 25, 35, 50];

// Update radius value display when slider changes
const radiusSlider = document.getElementById("radiusSlider");
const radiusSlider2 = document.getElementById("radiusSlider2");
const radiusValueDisplay = document.getElementById("radiusValue");
const radiusValueDisplay2 = document.getElementById("radiusValue2");
radiusValueDisplay.textContent = radiusOptions[radiusSlider.value];
radiusValueDisplay2.textContent = radiusOptions[radiusSlider2.value];

radiusSlider.addEventListener("input", function () {
  radiusValueDisplay.textContent = radiusOptions[this.value];
});

const searchBox = document.getElementById('searchBox');
    const autocompleteContainer = document.getElementById('autocompleteContainer');

    searchBox.addEventListener('input', function() {
        const query = this.value;

        if (query.length > 2) { // Démarre l'autocomplétion après 3 caractères
            fetch(`https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    autocompleteContainer.innerHTML = ''; // Vide le conteneur d'autocomplétion
                    data.forEach(item => {
                        const div = document.createElement('div');
                        div.classList.add('autocomplete-item');
                        div.innerText = item.display_name;
                        div.addEventListener('click', () => {
                            searchBox.value = item.display_name; // Mettre à jour le champ de recherche
                            autocompleteContainer.innerHTML = ''; // Vider les suggestions
                        });
                        autocompleteContainer.appendChild(div);
                    });
                })
                .catch(error => console.error('Error fetching autocomplete data:', error));
        } else {
            autocompleteContainer.innerHTML = ''; // Vider les suggestions si la requête est trop courte
        }
    });

    // Fermer la liste d'autocomplétion si on clique à l'extérieur
    document.addEventListener('click', function(event) {
        if (!searchBox.contains(event.target) && !autocompleteContainer.contains(event.target)) {
            autocompleteContainer.innerHTML = '';
        }
    });