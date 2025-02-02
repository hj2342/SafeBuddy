import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './CSS/UserLogin.css';

const API = import.meta.env.VITE_BACKEND_URL;

const UserLogin = ({ onLogin }) => {
  const navigate = useNavigate();
  const [isNewUser, setIsNewUser] = useState(false); // Toggle between login and register
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    address: '',
    date_of_birth: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Handle input change
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({ ...prevData, [name]: value }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      if (isNewUser) {
        // Register a new user
        const registerEndpoint = `${API}/register`;
        let response = await fetch(registerEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData),
        });

        let data = await response.json();

        if (response.ok) {
          localStorage.setItem('username', formData.username);
          localStorage.setItem('isLoggedIn', 'true');
          onLogin();
          navigate('/home'); // Redirect to home
        } else {
          setError(data.error || 'Registration failed.');
        }
      } else {
        // Login existing user
        const loginEndpoint = `${API}/login`;
        let response = await fetch(loginEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: formData.username, password: formData.password }),
        });

        let data = await response.json();

        if (response.ok) {
          localStorage.setItem('username', formData.username);
          localStorage.setItem('isLoggedIn', 'true');
          onLogin();
          navigate('/home'); // Redirect to home
        } else {
          setError(data.error || 'Login failed.');
        }
      }
    } catch (err) {
      console.error(err);
      setError('An error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="outer-wrapper">
      <div className="white-box">
        <h2 className="text-2xl font-bold mb-6">
          {isNewUser ? 'Create an Account' : 'Welcome Back!'}
        </h2>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="username" className="block font-medium text-gray-700 mb-1">
              Username
            </label>
            <input
              type="text"
              id="username"
              name="username"
              className="border rounded-md w-full p-2"
              placeholder="Enter your username"
              value={formData.username}
              onChange={handleInputChange}
              required
            />
          </div>

          {isNewUser && (
            <>
              <div className="mb-4">
                <label htmlFor="email" className="block font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  className="border rounded-md w-full p-2"
                  placeholder="Enter your email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="mb-4">
                <label htmlFor="address" className="block font-medium text-gray-700 mb-1">
                  Address
                </label>
                <input
                  type="text"
                  id="address"
                  name="address"
                  className="border rounded-md w-full p-2"
                  placeholder="Enter your address"
                  value={formData.address}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="mb-4">
                <label htmlFor="date_of_birth" className="block font-medium text-gray-700 mb-1">
                  Date of Birth
                </label>
                <input
                  type="date"
                  id="date_of_birth"
                  name="date_of_birth"
                  className="border rounded-md w-full p-2"
                  value={formData.date_of_birth}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </>
          )}

          <div className="mb-4">
            <label htmlFor="password" className="block font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              className="border rounded-md w-full p-2"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleInputChange}
              required
            />
          </div>

          {error && <p className="text-red-500">{error}</p>}

          <button
            type="submit"
            className="w-full py-2 px-4 bg-blue-500 text-white rounded-md"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Processing...' : isNewUser ? 'Register' : 'Login'}
          </button>
        </form>

        <p className="mt-4 text-blue-500 cursor-pointer" onClick={() => setIsNewUser(!isNewUser)}>
          {isNewUser ? 'Already have an account? Login' : 'Don’t have an account? Register'}
        </p>
      </div>
    </div>
  );
};

export default UserLogin;
