// Initialize the map
var map = L.map("map").setView([latitude, longitude], 13); // Coordinates of Paris
var currentCircle = null; // Variable to hold the circle for updating

// Add a tile layer (OpenStreetMap)
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// Draw zones if any exist
if (zones.length > 0) {
    drawZones(zones);
}

// Add a marker for the location
L.marker([latitude, longitude]).bindPopup(`<b>${display_name}</b>`).addTo(map);

// Radius options
const radiusOptions = [100, 250, 500, 750, 1000, 1500, 3000];

// Update radius value display when slider changes
var radiusSlider = document.getElementById("radiusSlider");
var radiusSlider2 = document.getElementById("radiusSlider2");
var radiusValueDisplay = document.getElementById("radiusValue");
var radiusValueDisplay2 = document.getElementById("radiusValue2");

// Set initial radius display values
radiusValueDisplay.textContent = radiusOptions[radiusSlider.value];
radiusValueDisplay2.textContent = radiusOptions[radiusSlider2.value];

// Event listener for the first radius slider
radiusSlider.addEventListener("input", function () {
    radiusValueDisplay.textContent = radiusOptions[this.value];
});

// Event listener for the second radius slider
radiusSlider2.addEventListener("input", function () {
    radiusValueDisplay2.textContent = radiusOptions[this.value];
});

// Set up the search box for location autocomplete
const searchBox = document.getElementById("searchBox");
const autocompleteContainer = document.getElementById("autocompleteContainer");

searchBox.addEventListener("input", function () {
    const query = this.value;

    if (query.length > 2) {
        // Start autocomplete after 3 characters
        fetch(`https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&q=${encodeURIComponent(query)}`)
            .then((response) => response.json())
            .then((data) => {
                autocompleteContainer.innerHTML = ""; // Clear the autocomplete container
                data.forEach((item) => {
                    const div = document.createElement("div");
                    div.classList.add("autocomplete-item");
                    div.innerText = item.display_name;
                    div.addEventListener("click", () => {
                        searchBox.value = item.display_name; // Update the search box with the selected item
                        autocompleteContainer.innerHTML = ""; // Clear suggestions
                    });
                    autocompleteContainer.appendChild(div);
                });
            })
            .catch((error) => console.error("Error fetching autocomplete data:", error));
    } else {
        autocompleteContainer.innerHTML = ""; // Clear suggestions if query is too short
    }
});

// Close the autocomplete list if clicking outside
document.addEventListener("click", function (event) {
    if (!searchBox.contains(event.target) && !autocompleteContainer.contains(event.target)) {
        autocompleteContainer.innerHTML = "";
    }
});

// Function to draw zones
function drawZones(pairs) {
    pairs.forEach((pair) => {
        console.log(pair);
        
        // Check for undefined values
        if (
            pair.school_lat === undefined ||
            pair.school_lon === undefined ||
            pair.station_lat === undefined ||
            pair.station_lon === undefined ||
            pair.intersection1_lat === undefined ||
            pair.intersection1_lon === undefined ||
            pair.intersection2_lat === undefined ||
            pair.intersection2_lon === undefined
        ) {
            console.warn(`One of the coordinates is undefined for school: ${pair.school_name} or station: ${pair.station_name}`);
            return; // Skip to the next pair if a value is undefined
        }

        // Draw circles for the station and school
        L.circle([pair.station_lat, pair.station_lon], {
            color: "blue", 
            fillColor: "blue", 
            fillOpacity: 0.3, 
            weight: 0,
            radius: r1, // Assuming r1 is defined elsewhere in your code
        }).addTo(map);

        L.circle([pair.school_lat, pair.school_lon], {
            color: "yellow",
            fillColor: "yellow",
            fillOpacity: 0.3,
            weight: 0,
            radius: r2, // Assuming r2 is defined elsewhere in your code
        }).addTo(map);
    });
}