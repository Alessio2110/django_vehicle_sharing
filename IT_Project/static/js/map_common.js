

my_marker = null; // Initialise red marker
location_id = null; // initialise location_id
current_markers = []; //initialise markers
location_address = null;
mapboxgl.accessToken = access_token; // Access token for mapbox




// Create map
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [-4.25, 55.865], // starting position, Glasgow City Centre
    zoom: 14 // starting zoom
});

// geocoder for address search
geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    zoom: 15,
    placeholder: 'Your current address',
    mapboxgl: mapboxgl,
    reverseGeocode: true,
    minLength: 3,
    marker: false,
    proximity: { // Glasgow University Address, search around it
        longitude: -4.24,
        latitude: 55.86
    }
})

// On address search
geocoder.on('result', e => {
    // Remove previous marker if it exists
    if (my_marker) {
        my_marker.remove();
    }
    // Create new marker at given address
    my_marker = new mapboxgl.Marker({
            draggable: true,
            color: 'red',
            symbol: 'bicycle'
        })
        .setLngLat(e.result.center)
        .addTo(map);

    // Update marker coordinates after dragging it
    my_marker.on('dragend', function (e) {
        var lngLat = e.target.getLngLat();
    });
});

function find_closest() {
    // If marker has not been initialised, cannot find the closest point to it
    if (my_marker == null)
        return;
    // Get marker coordinates
    lngLat = my_marker.getLngLat()
    // Big number so that anything can be smaller than this
    smallest_distance = 100000
    coordinates = null
    for (var i = 0; i < locations.length; i++) {
        var loc = locations[i];
        var distance = turf.distance([loc.longitude, loc.latitude], [lngLat.lng, lngLat.lat]);
        if (distance.toFixed(2) < smallest_distance) {
            smallest_distance = distance.toFixed(2);
            coordinates = [loc.longitude, loc.latitude];
            location_address = loc.address
            loc_id = loc.id
            console.log(loc_id)
        }
    }
    map.setZoom(18)
    console.log(coordinates)
    map.setCenter(coordinates)
    map.setZoom(16)
}

map.addControl(geocoder)
map.on('load', function () {
    // Get the geocoder instance
    const geocoder = document.querySelector('.mapboxgl-ctrl-geocoder input');

    // Add a listener for when a place is selected
    geocoder.addEventListener('change', function () {
        // Get the selected place
        const place = document.querySelector('.mapboxgl-ctrl-geocoder--suggestion-title')
            .textContent;

        // Get the coordinates of the selected place
        const coordinates = map.getCenter();

        // Log the place and coordinates
        console.log(place, coordinates);
    });
});

// Only show Glasgow and nearby area
const bounds = [
    [-4.29, 55.855], // Bottom left
    [-4.225, 55.88] // Top right
];
// Set the map's max bounds.
map.setMaxBounds(bounds);

// Add markers
function addMarkers(){
    console.log("Adding markers" + locations.length)
    for (var i = 0; i < locations.length; i++) {
        var loc = locations[i];
        var marker = new mapboxgl.Marker()
            .setLngLat([
                loc.longitude, loc.latitude
            ])
            .setPopup(new mapboxgl.Popup().setHTML("<h2>" +  loc.address + " </h2>"))
            .addTo(map)
        current_markers.push(marker)
    }
}
addMarkers()
// Remove all markers
function removeMarkers(){
    if (current_markers!==null) {
        for (var i = current_markers.length - 1; i >= 0; i--) {
            current_markers[i].remove();
        }
    }
}

const myButton = document.getElementById('search');
myButton.addEventListener('click', find_closest);


// {% comment %} var directions = new MapboxDirections({
//     accessToken: '{{mapbox_access_token}}',
//     unit: 'metric',
//     profile: 'mapbox/cycling'
//   });
//   map.addControl(directions, 'top-left'); {% endcomment %}

// JavaScript function to get cookie by name; retrieved from https://docs.djangoproject.com/en/3.1/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}