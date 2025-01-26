import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

// Google Maps API Loader
const loadGoogleMapsScript = () => {
  if (!window.google) {
    const script = document.createElement("script");
    script.src =
      "https://maps.googleapis.com/maps/api/js?key=AIzaSyCGvm2rH9fER_jvy7pl9pVz_u8anxESMuM";
    script.async = true;
    document.head.appendChild(script);
  }
};

const App = () => {
  const [userLocation, setUserLocation] = useState(null); // User's current location
  const [selectedBuilding, setSelectedBuilding] = useState(null); // Selected building
  const [nearbyBuildings, setNearbyBuildings] = useState([]); // Nearby buildings
  const [floorPlans, setFloorPlans] = useState([]); // Floor plans for the selected building
  const [currentFloor, setCurrentFloor] = useState(0); // Current floor number
  const [map, setMap] = useState(null); // Google Maps instance
  const [userMarker, setUserMarker] = useState(null); // Marker for the user's location

  // Step 1: Load Google Maps script
  useEffect(() => {
    if (!window.google) {
      loadGoogleMapsScript();
    }
  }, []);

  // Step 2: Fetch user's current location and initialize the map
  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        setUserLocation({ lat: latitude, lng: longitude });

        // Initialize the map
        const mapInstance = new window.google.maps.Map(
          document.getElementById("map"),
          {
            center: { lat: latitude, lng: longitude },
            zoom: 18,
          }
        );

        // Place the user marker
        const marker = new window.google.maps.Marker({
          position: { lat: latitude, lng: longitude },
          map: mapInstance,
          title: "Your Location",
        });

        setMap(mapInstance);
        setUserMarker(marker);
      },
      (error) => {
        console.error("Error fetching user's location:", error);
      }
    );
  }, []);

  // Step 3: Fetch nearby buildings
  useEffect(() => {
    if (userLocation) {
      axios
        .get("http://127.0.0.1:5000/buildings/near", {
          params: { lat: userLocation.lat, lng: userLocation.lng },
        })
        .then((response) => {
          setNearbyBuildings(response.data);
          setSelectedBuilding(response.data[0]); // Select the first building by default
        })
        .catch((error) =>
          console.error("Error fetching nearby buildings:", error)
        );
    }
  }, [userLocation]);

  // Step 4: Fetch floor plans for the selected building
  useEffect(() => {
    if (selectedBuilding) {
      axios
        .get(
          `http://127.0.0.1:5000/buildings/${selectedBuilding.name}/floorplans`
        )
        .then((response) => {
          setFloorPlans(response.data.floor_maps);
          setCurrentFloor(0); // Reset to the first floor
        })
        .catch((error) => console.error("Error fetching floor plans:", error));
    }
  }, [selectedBuilding]);

  // Update the user's location on the map (if already initialized)
  const updateUserLocation = (latitude, longitude) => {
    if (map && userMarker) {
      map.setCenter({ lat: latitude, lng: longitude });
      userMarker.setPosition({ lat: latitude, lng: longitude });
    }
  };

  // Handle "Location" button click to re-fetch user's location
  const handleLocationClick = () => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        console.log("User's location:", { lat: latitude, lng: longitude });
        setUserLocation({ lat: latitude, lng: longitude });
        updateUserLocation(latitude, longitude);
      },
      (error) => {
        console.error("Error fetching user's location:", error);
      }
    );
  };

  // Render map with the selected building's marker
  useEffect(() => {
    if (map && selectedBuilding) {
      new window.google.maps.Marker({
        position: {
          lat: selectedBuilding.coordinates.coordinates[1],
          lng: selectedBuilding.coordinates.coordinates[0],
        },
        map,
        title: selectedBuilding.name,
      });
    }
  }, [map, selectedBuilding]);

  return (
    <div className="app">
      <header className="header">
        <img
          src="https://assets-sports-gcp.thescore.com/football/team/534/logo.png"
          alt="Logo"
          style={{ width: 50, height: 50 }}
        />
        <h1>Fire Evacuation Hub</h1>
        <nav>
          <a href="#alerts">Live Alerts</a>
          <a href="#resources">Resources</a>
          <a href="#contact">Contact</a>
        </nav>
      </header>

      <main>
        <section className="map-section">
          <h2>{selectedBuilding ? selectedBuilding.name : "Loading..."}</h2>
          <div id="map" style={{ height: "300px", marginTop: "20px" }}></div>
          <button
            className="sos-button"
            onClick={() => alert("Personnel is notified and is coming.")}
          >
            SOS: Disabled, Preg, Elderly
          </button>
          <button onClick={handleLocationClick}>
            Show My Current Location
          </button>
          {nearbyBuildings.length > 0 ? (
            <select
              onChange={(e) =>
                setSelectedBuilding(
                  nearbyBuildings.find((b) => b._id === e.target.value)
                )
              }
            >
              {nearbyBuildings.map((building) => (
                <option key={building._id} value={building._id}>
                  {building.name}
                </option>
              ))}
            </select>
          ) : (
            <p>Loading nearby buildings...</p>
          )}
        </section>

        <section className="floor-plan-section">
          {floorPlans.length > 0 ? (
            <>
              <img
                src={`http://127.0.0.1:5000/floorplans/${floorPlans[currentFloor]}`}
                alt={`Floor ${currentFloor + 1}`}
                style={{ width: "100%", maxHeight: "400px" }}
              />
              <div className="floor-navigation">
                <button
                  onClick={() =>
                    setCurrentFloor((prev) => Math.max(prev - 1, 0))
                  }
                  disabled={currentFloor === 0}
                >
                  ← Previous
                </button>
                <span>Floor {currentFloor + 1}</span>
                <button
                  onClick={() =>
                    setCurrentFloor((prev) =>
                      Math.min(prev + 1, floorPlans.length - 1)
                    )
                  }
                  disabled={currentFloor === floorPlans.length - 1}
                >
                  Next →
                </button>
              </div>
            </>
          ) : (
            <p>Loading floor plans...</p>
          )}
        </section>
      </main>
    </div>
  );
};

export default App;
