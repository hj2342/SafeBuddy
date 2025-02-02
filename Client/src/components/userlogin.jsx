import React, { useState } from 'react';
import { LucideUser, LucideKey, LucideMail, LucideMapPin, LucideCalendar } from 'lucide-react';
import './CSS/UserLogin.css';

const API = import.meta.env.VITE_BACKEND_URL;

const UserLogin = ({ onLoginOrSignup }) => {
  const [isNewUser, setIsNewUser] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    address: '',
    date_of_birth: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const endpoint = isNewUser ? `${API}/register` : `${API}/login`;
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      console.log('Response:', data);

      if (response.ok) {
        if (isNewUser) {
          setSuccessMessage('Registration successful! Redirecting to login...');
          setError('');
          setTimeout(() => {
            setIsNewUser(false);
            setFormData({ username: '', email: '', address: '', date_of_birth: '', password: '' });
            setSuccessMessage('');
          }, 2000);
        } else {
          setSuccessMessage('Login successful!');
          setError('');
          localStorage.setItem('username', formData.username);
          onLoginOrSignup(data);
        }
      } else {
        setError(data.error || 'Something went wrong');
        setSuccessMessage('');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
      setSuccessMessage('');
      console.error(err);
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
            <div className="relative">
              <LucideUser className="absolute top-1/2 transform -translate-y-1/2 left-3 text-gray-400" />
              <input
                type="text"
                id="username"
                name="username"
                className="pl-10 pr-4 py-2 border rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your username"
                value={formData.username}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>

          {isNewUser && (
            <>
              <div className="mb-4">
                <label htmlFor="email" className="block font-medium text-gray-700 mb-1">
                  Email
                </label>
                <div className="relative">
                  <LucideMail className="absolute top-1/2 transform -translate-y-1/2 left-3 text-gray-400" />
                  <input
                    type="email"
                    id="email"
                    name="email"
                    className="pl-10 pr-4 py-2 border rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter your email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>

              <div className="mb-4">
                <label htmlFor="address" className="block font-medium text-gray-700 mb-1">
                  Emergency Contact
                </label>
                <div className="relative">
                  <LucideMapPin className="absolute top-1/2 transform -translate-y-1/2 left-3 text-gray-400" />
                  <input
                    type="text"
                    id="address"
                    name="address"
                    className="pl-10 pr-4 py-2 border rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter your address"
                    value={formData.address}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>

              <div className="mb-4">
                <label htmlFor="date_of_birth" className="block font-medium text-gray-700 mb-1">
                  Date of Birth
                </label>
                <div className="relative">
                  <LucideCalendar className="absolute top-1/2 transform -translate-y-1/2 left-3 text-gray-400" />
                  <input
                    type="date"
                    id="date_of_birth"
                    name="date_of_birth"
                    className="pl-10 pr-4 py-2 border rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={formData.date_of_birth}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>
            </>
          )}

          <div className="mb-4">
            <label htmlFor="password" className="block font-medium text-gray-700 mb-1">
              Password
            </label>
            <div className="relative">
              <LucideKey className="absolute top-1/2 transform -translate-y-1/2 left-3 text-gray-400" />
              <input
                type="password"
                id="password"
                name="password"
                className="pl-10 pr-4 py-2 border rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>

          {error && <p className="text-red-500 mb-4">{error}</p>}
          {successMessage && <p className="text-green-500 mb-4">{successMessage}</p>}

          <button
            type="submit"
            className={`w-full py-2 px-4 bg-blue-500 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              isSubmitting ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            disabled={isSubmitting}
          >
            {isNewUser ? 'Register' : 'Login'}
          </button>

          <div className="text-center mt-4">
            <p className="text-blue-500 cursor-pointer" onClick={() => setIsNewUser(!isNewUser)}>
              {isNewUser ? 'Already have an account? Login' : 'Don’t have an account? Register'}
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserLogin;
