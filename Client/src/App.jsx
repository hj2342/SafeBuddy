import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import UserLogin from './components/userlogin';
import Location from './components/Location';
import Navigation from './components/Navigation';
import HomeComponent from './components/HomeComponent';
import Inbox from './components/Inbox';
import Profile from './components/Profile';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Sync login state from localStorage
  useEffect(() => {
    const storedLoginState = localStorage.getItem('isLoggedIn') === 'true';
    setIsLoggedIn(storedLoginState);
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true);
    localStorage.setItem('isLoggedIn', 'true');
  };

  return (
    <Router>
      <div className="app-container">
        <Location />
        {isLoggedIn ? (
          <>
            <Navigation />
            <Routes>
              <Route path="/home" element={<HomeComponent />} />
              <Route path="/inbox" element={<Inbox />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="*" element={<Navigate to="/home" />} /> {/* Redirect to home */}
            </Routes>
          </>
        ) : (
          <Routes>
            <Route path="/" element={<UserLogin onLogin={handleLogin} />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        )}
      </div>
    </Router>
  );
}

export default App;
