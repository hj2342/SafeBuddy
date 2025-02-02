import { useState } from 'react';
import UserLogin from './components/userlogin';
import './App.css';
const API_URL = import.meta.env.VITE_BACKEND_URL;

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentLocation, setCurrentLocation] = useState(null);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const sendLocationToBackend = async (location) => {
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(location),
      });

      const data = await response.json();
      console.log("Location saved to backend:", data);
    } catch (error) {
      console.error("Error sending location to backend:", error);
    }
  };

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const location = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          };
          setCurrentLocation(location);
          console.log("Current Location:", location);

          // Send to backend
          sendLocationToBackend(location);
        },
        (error) => console.error("Error getting location:", error)
      );
    } else {
      alert("Geolocation is not supported by this browser.");
    }
  }, []);

  return (
    <div className="app-container">
      {isLoggedIn ? (
        <div>
          <p>You are logged in!</p>
          {currentLocation ? (
            <p>📍 Latitude: {currentLocation.latitude}, Longitude: {currentLocation.longitude}</p>
          ) : (
            <p>Fetching location...</p>
          )}
        </div>
      ) : (
        <UserLogin onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;