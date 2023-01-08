'use strict'


let mapOptions = {
    center: [50.958, 17],   // KOHTA, mihin map zoomautuu sivun auetessa. pelin tapauksessa lähtökenttä/player location?
    zoom: 13,                    // Kuinka paljon se on zoomautunut tähän kohtaan. (PIDÄ ALUSSA ISONA ZOOMINA JOTTA CLUSTERAUS TOIMII)
}

let home = {       // players current location:
    lat: mapOptions.center[0],
    lng: mapOptions.center[1],
    zoom: mapOptions.zoom
  };

const map = new L.map('map', mapOptions);

let layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //updateWhenZooming: false,
    //updateWhenIdle: true,

});

map.addLayer(layer);

const planeIcon = L.icon({
    iconUrl: 'map/planecircle.png', //483x707 // circle version 483x500
    iconSize: [16.1, 16.667], // size of the icon  divided by 30 atm
    //iconAnchor: [16.0667,42.667] //241,640 (not with circle) // coordinates of the original image | point of the icon which will correspond to marker's location (bottom of the marker)
    popupAnchor: [-0.5, -17]

})

//Päivitä pelaajan lokaation
function updatePlayerPos(){
    const pos = user.location.pos
    home.lat = pos[0]
    home.lng = pos[1]
}

let currLoc

// Markkerin luonti + popup ominaisuus
function addMarker(airport) {
    let marker = new L.marker(airport.pos, {icon: planeIcon}).addTo(map)
    marker.icao = airport.icao
    marker.on('mouseover', function (ev){
        let msg=`${airport.name} [${airport.icao}] <br>Fuelprice: ${airport.fuelprice} €/l<br>`
        airport.icao==currLoc?msg+='Current location':msg+='Click to fly'
        marker.bindPopup(msg)
        this.openPopup();
    })
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

fetch('http://127.0.0.1:3000/load')
  .then((response) => response.json())
  .then((data) => {
    console.log('starting load...')
    for (let i of data.content) {
        const marker = addMarker(i)  //addMarker(airports[x].latitude, airports[x]
        marker.on('click', function (ev) {
            console.log(user.location.icao)
            if(user.location.icao!=marker.icao){
                console.log(marker.icao)
                flyMenu(marker.icao)
            }// update location
        });
        markers.addLayer(marker)
    }
    map.addLayer(markers)
    console.log('Airports loaded')
    addHandlers()
  });

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
// const OpenWeatherMap_Clouds = L.tileLayer('http://{s}.tile.openweathermap.org/map/clouds/{z}/{x}/{y}.png?appid={apiKey}', {
//     maxZoom: 19,
//     attribution: 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>',
//     apiKey: 'f3e0b30bb708435af79fa709d74b0750',
//     opacity: 0.7,
//     //updateWhenZooming: false,
//     //updateWhenIdle: true,
// });

// Live tuuli ( ei käytössä nyt )
// const OpenWeatherMap_Wind = L.tileLayer('http://{s}.tile.openweathermap.org/map/wind/{z}/{x}/{y}.png?appid={apiKey}', {
//     maxZoom: 19,
//     attribution: 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>',
//     apiKey: 'f3e0b30bb708435af79fa709d74b0750',
//     opacity: 0.5,
//     //updateWhenZooming: false,
//     //updateWhenIdle: true,
// });

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
// const Stamen_Watercolor = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
//     attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
//     subdomains: 'abcd',
//     minZoom: 1,
//     maxZoom: 16,
//     ext: 'jpg',
//     //updateWhenZooming: false,
//     //updateWhenIdle: true,
// });
// Stamen_Watercolor.addTo(map)


// MAP LAYERS CONTROL
const mixed = {
    "Simple": CartoDB_VoyagerNoLabels,
    "Satellite": Esri_WorldImagery,
    "Labels and borders": Stamen_TonerHybrid,
}

L.control.layers(null, mixed,{collapsed:true}).addTo(map);

    // button to reset view to the players location
L.easyButton('<img src="map/locationjpg.jpg" alt="current location">',function(btn,map){

    //Get players updated place
    updatePlayerPos()

  map.setView([home.lat, home.lng], 8);
},'Zoom To Current Location').addTo(map);

