'use strict'
let mapOptions = {
    center: [50.958, 17],   // KOHTA, mihin map zoomautuu sivun auetessa. pelin tapauksessa lähtökenttä/player location?
    zoom: 13,                    // Kuinka paljon se on zoomautunut tähän kohtaan. (PIDÄ ALUSSA ISONA ZOOMINA JOTTA CLUSTERAUS TOIMII)
}


const map = new L.map('map', mapOptions);

let layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //updateWhenZooming: false,
    //updateWhenIdle: true,

});

map.addLayer(layer);

const planeIcon = L.icon({
    iconUrl: 'planecircle.png', //483x707 // circle version 483x500
    iconSize: [16.1, 16.667], // size of the icon  divided by 30 atm
    //iconAnchor: [16.0667,42.667] //241,640 (not with circle) // coordinates of the original image | point of the icon which will correspond to marker's location (bottom of the marker)
    popupAnchor: [-0.5, -17]

})

//Random numero funktio devausvaiheessa markkereiden luontiin.
function getRandom(min, max) {
    return Math.random() * (max - min) + min;
}

// Markkerin luonti + popup ominaisuus
function addMarker(lat, lng) {
    let marker = new L.marker([lat, lng], {icon: planeIcon}).addTo(map) //.bindPopup(`Airport name from python `).openPopup();
    marker.bindPopup(`Airport name from python <br> Click to travel`);
    marker.on('mouseover', function (e) {
        this.openPopup();
    });
    marker.on('mouseout', function (e) {
        this.closePopup();
    });
    return marker
}


//Marker group properties
const markers = L.markerClusterGroup({
    //spiderfyOnMaxZoom: false,
    //showCoverageOnHover: false,
    //zoomToBoundsOnClick: false,
    removeOutsideVisibleBounds: false,
    //animateAddingMarkers: true,
    //animate: true,
    //maxClusterRadius: 80
    chunkedLoading: true

});

// Adding the markers to the map and markers locations from clicks to console.
// Adding markers to marker group
for (let x = 0; x <= 5000; x++) {
    const marker = addMarker(getRandom(85, -85), getRandom(-190, 189.9))  //addMarker(airports[x].latitude, airports[x]
    marker.on('click', function (ev) {
        let latlng = map.mouseEventToLatLng(ev.originalEvent);
        console.log(latlng.lat + ', ' + latlng.lng); // update location

    });
    markers.addLayer(marker)
}
map.addLayer(markers)


// Satellite map
const Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
   //updateWhenZooming: false,
    //updateWhenIdle: true,
});

Esri_WorldImagery.addTo(map)


// Labels and borders
const Stamen_TonerHybrid = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner-hybrid/{z}/{x}/{y}{r}.{ext}', {
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    subdomains: 'abcd',
    minZoom: 0,
    maxZoom: 20,
    ext: 'png',
    //updateWhenZooming: false,
    //updateWhenIdle: true,
});

Stamen_TonerHybrid.addTo(map)


// Live pilvet (ei käytössä nyt)
const OpenWeatherMap_Clouds = L.tileLayer('http://{s}.tile.openweathermap.org/map/clouds/{z}/{x}/{y}.png?appid={apiKey}', {
    maxZoom: 19,
    attribution: 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>',
    apiKey: 'f3e0b30bb708435af79fa709d74b0750',
    opacity: 0.7,
    //updateWhenZooming: false,
    //updateWhenIdle: true,
});

// Live tuuli ( ei käytössä nyt )
const OpenWeatherMap_Wind = L.tileLayer('http://{s}.tile.openweathermap.org/map/wind/{z}/{x}/{y}.png?appid={apiKey}', {
    maxZoom: 19,
    attribution: 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>',
    apiKey: 'f3e0b30bb708435af79fa709d74b0750',
    opacity: 0.5,
    //updateWhenZooming: false,
    //updateWhenIdle: true,
});

//OpenWeatherMap_Clouds.addTo(map)
//OpenWeatherMap_Wind.addTo(map)

const CartoDB_VoyagerNoLabels = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20,
    //updateWhenZooming: false,
    //updateWhenIdle: true,
});
CartoDB_VoyagerNoLabels.addTo(map)

// Drawn map
const Stamen_Watercolor = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    subdomains: 'abcd',
    minZoom: 1,
    maxZoom: 16,
    ext: 'jpg',
    //updateWhenZooming: false,
    //updateWhenIdle: true,
});
Stamen_Watercolor.addTo(map)


// MAP LAYERS CONTROL
const mixed = {
    "Simple": CartoDB_VoyagerNoLabels,
    "Drawn": Stamen_Watercolor,
    "Satellite": Esri_WorldImagery,
    "Labels and borders": Stamen_TonerHybrid,
}

L.control.layers(null, mixed,{collapsed:true}).addTo(map);


const home = {       // players current location:
  lat: mapOptions.center[0],
  lng: mapOptions.center[1],
  zoom: mapOptions.zoom
};

    // button to reset view to the players location
L.easyButton('<img src="locationjpg.jpg" alt="current location">',function(btn,map){
  map.setView([home.lat, home.lng], home.zoom);
},'Zoom To Current Location').addTo(map);

