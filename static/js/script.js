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
const radiusOptions = [50, 100, 250, 500, 1000, 2500, 5000];

// Update radius value display when slider changes
const radiusSlider = document.getElementById("radiusSlider");
const radiusValueDisplay = document.getElementById("radiusValue");
radiusValueDisplay.textContent = radiusOptions[radiusSlider.value];

radiusSlider.addEventListener("input", function () {
  radiusValueDisplay.textContent = radiusOptions[this.value];
});

// Function to search for a location using Nominatim
// async function searchLocation(query) {
//   const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
//     query
//   )}`;
//   try {
//     const response = await fetch(url);
//     const data = await response.json();
//     if (data && data.length > 0) {
//       const { lat, lon } = data[0];
//       map.setView([lat, lon], 13); // Center map on found location

//       // Remove previous circle if it exists
//       if (currentCircle) {
//         map.removeLayer(currentCircle);
//       }

//       L.marker([lat, lon])
//         .addTo(map) // Place marker at location
//         .bindPopup(`<b>${query}</b>`);
//       currentCircle = L.circle([lat, lon], { radius }).addTo(map);
//       currentCircle
//         .bindPopup(`<b>${query}</b><br>Radius: ${radius} meters`)
//         .openPopup();
//     } else {
//       alert("Location not found.");
//     }
//   } catch (error) {
//     console.error("Error fetching location data:", error);
//   }
// }

// Ajouter un marqueur
//       var circle = L.circle([51.508, -0.11], {
//         color: "red",
//         fillColor: "#f03",
//         fillOpacity: 0.5,
//         radius: 5000,
//       }).addTo(map);
//       var circle2 = L.circle([51.51, -0.047], {
//         color: "yellow",
//         fillColor: "yellow",
//         fillOpacity: 0.5,
//         radius: 5000,
//       }).addTo(map);

// Search functionality (example)
// document.getElementById("searchButton").addEventListener("click", function () {
//   const query = document.getElementById("searchBox").value;
//   const selectedRadius = radiusOptions[radiusSlider.value]; // Get radius from slider
//   if (query) {
//     searchLocation(query, selectedRadius);
//   } else {
//     alert("Please enter a location to search.");
//   }
// });
