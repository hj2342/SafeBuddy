import React, { useState, useEffect } from "react";
import "./CSS/Inbox.css";

const mockInboxData = [
  { id: 1, sender: "SafeBuddy Team", subject: "Welcome to SafeBuddy!", message: "Thank you for signing up! Stay safe.", time: "10:30 AM", read: false },
  { id: 2, sender: "Emergency Alert", subject: "Weather Warning", message: "Heavy rainfall expected. Stay indoors!", time: "9:00 AM", read: false },
  { id: 3, sender: "Support", subject: "Your Inquiry", message: "We have received your inquiry and will respond soon.", time: "Yesterday", read: true },
];

const Inbox = () => {
  const [messages, setMessages] = useState([]);
  const [selectedMessage, setSelectedMessage] = useState(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    // Replace this with backend fetch logic
    setMessages(mockInboxData);
  }, []);

  const handleMessageClick = (message) => {
    setSelectedMessage(message);
    setMessages(messages.map(m => m.id === message.id ? { ...m, read: true } : m));
  };

  const handleClosePopup = () => {
    setSelectedMessage(null);
  };

  return (
    <div className="inbox-container">
      <h2>Inbox</h2>

      <input
        type="text"
        placeholder="Search messages..."
        className="search-bar"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <div className="message-list">
        {messages
          .filter((msg) => msg.subject.toLowerCase().includes(search.toLowerCase()))
          .map((msg) => (
            <div
              key={msg.id}
              className={`message-item ${msg.read ? "" : "unread"}`}
              onClick={() => handleMessageClick(msg)}
            >
              <span className="sender">{msg.sender}</span>
              <span className="subject">{msg.subject}</span>
              <span className="time">{msg.time}</span>
            </div>
          ))}
      </div>

      {selectedMessage && (
        <div className="message-popup">
          <div className="message-content">
            <h3>{selectedMessage.subject}</h3>
            <p><strong>From:</strong> {selectedMessage.sender}</p>
            <p>{selectedMessage.message}</p>
            <button onClick={handleClosePopup}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Inbox;
