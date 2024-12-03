// Function to search for a location using Nominatim
async function searchLocation(query) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`;
    console.log(url);
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        if (data && data.length > 0) {
            const { lat, lon } = data[0];
            // Ici, vous pouvez centrer la carte sur la localisation trouvée
            // map.setView([lat, lon], 13); // Exemple de centrage de la carte
            return { latitude: lat, longitude: lon };
        } else {
            console.log("Location not found.");
            return null;
        }
    } catch (error) {
        console.error('Error fetching location data:', error);
        return null;
    }
}

// Exemple d'utilisation
const query = "Paris";
searchLocation(query).then(location => {
    if (location) {
        console.log(`Location found: Latitude: ${location.latitude}, Longitude: ${location.longitude}`);
        // Code pour centrer la carte ici, par exemple :
        // map.setView([location.latitude, location.longitude], 13);
    }
});