import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UserLogin from './components/userlogin';
import Location from './components/Location';
import Navigation from './components/Navigation';
import HomeComponent from './components/HomeComponent';
import Inbox from './components/Inbox';
import Profile from './components/Profile';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
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
            </Routes>
          </>
        ) : (
          <UserLogin onLogin={handleLogin} />
        )}
      </div>
    </Router>
  );
}

export default App;
