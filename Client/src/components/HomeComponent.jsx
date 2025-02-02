import React from 'react';
import "./CSS/HomeComponent.css";

const HomeComponent = () => {
  const menuItems = [
    { id: 1, label: "Emergency Contacts", icon: "📞", className: "emergency" },
    { id: 2, label: "Safe Walk", icon: "🚶‍♂️", className: "safewalk" },
    { id: 3, label: "Check-In Feature", icon: "✅", className: "checkin" },
    { id: 4, label: "Incident Report", icon: "📑", className: "incident" },
    { id: 5, label: "Travel Assistance", icon: "🛫", className: "travel" },
    { id: 6, label: "Wellness Support", icon: "❤️", className: "wellness" },
    { id: 7, label: "Neighborhood Watch", icon: "👀", className: "watch" },
    { id: 8, label: "Safety Guidelines", icon: "⚠️", className: "guidelines" },
    { id: 9, label: "Personal Safety Tools", icon: "🛠", className: "tools" },
  ];

  return (
    <div className="home-container">
      <header className="header">
        <h1><span className="safe">Safe</span><span className="buddy">Buddy</span></h1>
      </header>

      <section className="info-feed">
        <h2>Safety Alerts & Updates</h2>
        <p>Feb 2 - Stay alert! Recent weather conditions have increased road hazards. Drive safely and follow all emergency precautions.</p>
      </section>

      <div className="grid-container">
        {menuItems.map(({ id, label, icon, className }) => (
          <div key={id} className={`grid-item ${className}`}>
            <span className="icon">{icon}</span>
            <span className="label">{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomeComponent;
