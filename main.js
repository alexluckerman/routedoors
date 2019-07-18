let map, dirDisplay, dirService, geocoder;
const webEndpoint = "https://us-central1-maps-react-220002.cloudfunctions.net/routedoors_handler";

// Initializes the map, called by the Google Maps API script once it has loaded
function initMap() {
    console.log("Map script has been loaded");
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 39.83, // this is like the center of the US or something
            lng: -98.58
        },
        zoom: 4
    });
    geocoder = new google.maps.Geocoder();
    dirService = new google.maps.DirectionsService();
    dirDisplay = new google.maps.DirectionsRenderer();
    dirDisplay.setMap(map);
    $("#locationButton").click(getLocation);
    $("#routingButton").click(getRoutes);
}

// Handles getting location
function getLocation() {
    $("origin").text("Loading current location...");
    navigator.geolocation.getCurrentPosition(getAddressFromLocation, function () {
        alert("We need permission to get your location. Please reload and try again.");
    });
}


// Takes user position data and calls the Google Maps Geocoder API to output a human-readable address
function getAddressFromLocation(posData) {
    const pos = new google.maps.LatLng(posData.coords.latitude, posData.coords.longitude);
    geocoder.geocode({ location: pos }, response => {
        $("#origin").val(response[0].formatted_address);
    });
    map.setCenter(pos);
    new google.maps.Marker({
        position: pos,
        map: map
    });
}

function toggleLoading() {
    $("#header").toggle();
    $("#map").toggle();
    $(".loading").toggleClass('hidden');
}

// Finds a route starting and ending at the provided origin of the desired distance
function getRoutes() {
    // The web page to be fetched
    const reqParams = webEndpoint + "?origin=" + $("#origin").val() + "&dist=" + $("#dist").val();

    toggleLoading();
    // Make a request to the server to get the rout
    fetch(new Request(reqParams, {
            method: "POST"
        }))
        .then(response => {
            if (!response.ok) {
                throw response;
            }
            return response.json();
        }).then(response => {
            console.log(response);

            // Takes the returned link to Google Maps and displays it in the header
            const href = response.pop(); // The final item in the response array is the URL for Google Maps directions
            $("#mapUrl").attr('href', href).text("Open route in Google Maps"); // feels jank but okay

            // Translate response of waypoints into an array DirectionsService can handle
            const waypoints = response.map(elem => {
                return {
                    location: new google.maps.LatLng(elem[0], elem[1]),
                    stopover: false
                };
            }); 

            // All of the parameters that make up the request to the DirectionsService
            const pos = new google.maps.LatLng(response[0][0], response[0][1]);
            const request = {
                origin: pos,
                destination: pos,
                travelMode: "WALKING",
                waypoints: waypoints,
                optimizeWaypoints: false,
                provideRouteAlternatives: false
            };
            // Calls to the DirectionsService, takes the response and sends it to DirectionsRenderer
            dirService.route(request, function (response, status) {
                if (status === "OK") {
                    dirDisplay.setDirections(response);
                    console.log(response);
                } else {
                    console.log("Directions request failed: " + status);
                }
            });
            toggleLoading();
        }).catch((err) => {
            alert("An error occured. Please try again later");
            toggleLoading();
            console.log(err);
        });
}