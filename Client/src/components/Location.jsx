import React, { useState, useEffect } from 'react';

const UserLocation = () => {
  const [location, setLocation] = useState({ lat: null, lon: null });
  const [address, setAddress] = useState('');
  const [error, setError] = useState('');

  // Function to fetch address from coordinates
  const fetchAddress = async (lat, lon) => {
    try {
      const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
      const data = await response.json();
      if (data.display_name) {
        setAddress(data.display_name);
      } else {
        setAddress('Address not found');
      }
    } catch (error) {
      console.error('Error fetching address:', error);
      setAddress('Unable to retrieve address');
    }
  };

  // Get user's location on page load
  useEffect(() => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setLocation({ lat: latitude, lon: longitude });
          fetchAddress(latitude, longitude); // Fetch address immediately after getting coordinates
        },
        (error) => {
          setError('Location permission denied. Please enable location services.');
          console.error('Geolocation Error:', error);
        }
      );
    } else {
      setError('Geolocation is not supported by this browser.');
    }
  }, []);

  return (
    <div className="location-container">
      <h2>User Location</h2>
      {location.lat && location.lon ? (
        <>
          <p>📍 <strong>Latitude:</strong> {location.lat}</p>
          <p>📍 <strong>Longitude:</strong> {location.lon}</p>
          <p>🏠 <strong>Address:</strong> {address || 'Retrieving address...'}</p>
        </>
      ) : (
        <p className="error">{error || 'Retrieving location...'}</p>
      )}
    </div>
  );
};

export default UserLocation;
