mapboxgl.accessToken = 'pk.eyJ1IjoiYWxlc3NpbzIxIiwiYSI6ImNsOWgzOXBiejBtamIzb284bGJjejY2ZjQifQ.l9i3VHeSTLEL0hsjQcz6tA';
const map = new mapboxgl.Map({
    container: 'map', // container ID
    // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
    //style: 'mapbox://styles/mapbox/streets-v12', // style URL
    style: 'mapbox://styles/mapbox/navigation-night-v1',
    //style: 'mapbox://styles/mapbox/dark-v11',
    center: [-74.5, 40], // starting position [lng, lat]
    zoom: 9 // starting zoom
});
