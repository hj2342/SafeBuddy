import React from 'react';
import { Link } from 'react-router-dom';
import { Home, User, Mail } from 'lucide-react';
import '../App.css';
import './CSS/Navigation.css';
function Navigation() {
  const navItems = [
    { id: 'home', icon: Home, label: 'Home', path: '/' },
    { id: 'inbox', icon: Mail, label: 'Inbox', path: '/inbox' },
    { id: 'profile', icon: User, label: 'Profile', path: '/profile' },
  ];

  return (
    <nav className="navigation-container">
      {navItems.map(({ id, icon: Icon, label, path }) => (
        <Link key={id} to={path} className="nav-item">
          <Icon className="icon" />
          <span>{label}</span>
        </Link>
      ))}
    </nav>
  );
}

export default Navigation;
