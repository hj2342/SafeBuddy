import { useState } from 'react';
import UserLogin from './components/userlogin';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <div className="app-container">
      {isLoggedIn ? (
        <p>You are logged in!</p>
      ) : (
        <UserLogin onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;