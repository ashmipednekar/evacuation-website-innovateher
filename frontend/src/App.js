import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [userLocation, setUserLocation] = useState(null);
  const [nearestBuilding, setNearestBuilding] = useState(null);
  const [floorPlans, setFloorPlans] = useState([]);
  const [currentFloor, setCurrentFloor] = useState(0);

  // Step 1: Get user's geolocation
  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setUserLocation({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        });
      },
      (error) => {
        console.error("Error fetching user location:", error);
        alert("Could not fetch your location. Please allow location access.");
      }
    );
  }, []);

  // Step 2: Fetch the nearest building
  useEffect(() => {
    if (userLocation) {
      console.log("Fetching nearest building for:", userLocation);
      axios
        .get("http://127.0.0.1:5000/buildings/near", {
          params: {
            lat: userLocation.lat,
            lng: userLocation.lng,
            max_distance: 5000,
          },
        })
        .then((response) => {
          console.log("Nearest building response:", response.data);
          setNearestBuilding(response.data[0]);
        })
        .catch((error) => {
          console.error("Error fetching nearest building:", error);
          alert(
            "There was an error fetching the nearest building. Check the console for details."
          );
        });
    }
  }, [userLocation]);

  // Step 3: Fetch floor plans for the confirmed building
  const confirmBuilding = () => {
    if (nearestBuilding) {
      console.log("Fetching floor plans for building:", nearestBuilding.name);
      axios
        .get(
          `http://127.0.0.1:5000/buildings/${nearestBuilding._id}/floorplans`
        )
        .then((response) => {
          console.log("Floor plans response:", response.data);
          setFloorPlans(response.data.floor_maps);
        })
        .catch((error) => {
          console.error("Error fetching floor plans:", error);
          alert(
            "There was an error fetching the floor plans. Check the console for details."
          );
        });
    }
  };

  // Step 4: Navigation between floors
  const goToNextFloor = () => {
    if (currentFloor < floorPlans.length - 1) {
      setCurrentFloor(currentFloor + 1);
    }
  };

  const goToPreviousFloor = () => {
    if (currentFloor > 0) {
      setCurrentFloor(currentFloor - 1);
    }
  };

  // Step 5: Display location confirmation or floor plans
  if (!userLocation) return <div>Fetching your location...</div>;

  if (!floorPlans.length && nearestBuilding) {
    return (
      <div>
        <h2>Is this your location?</h2>
        <p>
          <strong>{nearestBuilding.name}</strong>
        </p>
        <button onClick={confirmBuilding}>Yes</button>
        <button
          onClick={() => alert("You declined the location. Please try again.")}
        >
          No
        </button>
      </div>
    );
  }

  if (floorPlans.length) {
    return (
      <div className="floor-plan-container">
        <h1>{nearestBuilding.name}</h1>
        <h2>Floor {currentFloor + 1}</h2>
        <div className="floor-plan">
          <img
            src={`https://via.placeholder.com/800x600?text=Floor+${
              currentFloor + 1
            }`}
            alt={`Floor ${currentFloor + 1}`}
            draggable
          />
        </div>
        <div className="navigation">
          <button onClick={goToPreviousFloor} disabled={currentFloor === 0}>
            ← Previous Floor
          </button>
          <button
            onClick={goToNextFloor}
            disabled={currentFloor === floorPlans.length - 1}
          >
            Next Floor →
          </button>
        </div>
      </div>
    );
  }

  return <div>Loading nearest building...</div>;
};

export default App;
