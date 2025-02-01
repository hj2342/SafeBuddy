from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import certifi

# Authentication and password hashing
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
)

# Initialize Flask app
app = Flask(__name__)
# app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this in production!
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
# jwt = JWTManager(app)

# Enable CORS (adjust origins as needed)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Connect to MongoDB Atlas (update the connection string with your credentials)
client = MongoClient(
    "mongodb+srv://NYUADHackathon:<NYUADHackathon>@cluster0.x3t1u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    tlsCAFile=certifi.where()
)

# Use a new database for the safety app
db = client.NYUADHackathon

@app.route('/')
def home():
    return "Connected to Safety App Backend!"

# -------------------------
#  User Authentication Routes
# -------------------------

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    Expected JSON fields: username, password, email
    """
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    required_fields = ['username', 'password', 'email']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Check if the username already exists
    if db.users.find_one({"username": data['username']}):
        return jsonify({"error": "Username already exists"}), 409

    # Hash the password for security
    hashed_password = generate_password_hash(data['password'])
    user = {
        "username": data['username'],
        "password": hashed_password,
        "email": data['email'],
        "created_at": datetime.utcnow(),
        # Additional user fields can be added here (e.g., phone number, emergency contacts)
    }
    db.users.insert_one(user)
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    """
    Log in an existing user.
    Expected JSON fields: username, password
    Returns a JWT access token on success.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = db.users.find_one({"username": username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Log out the current user. In JWT-based systems, logout is often handled client side
    by deleting the stored token. Here we also unset JWT cookies if they were set.
    """
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200

# -------------------------
#  Danger Zone Endpoints
# -------------------------

@app.route('/danger_zones', methods=['POST'])
@jwt_required()
def add_danger_zone():
    """
    Add a new danger zone.
    Expected JSON fields: name, description, coordinates, active_from, active_to
    - coordinates: could be a list of coordinate pairs that define the area
    - active_from and active_to: times (e.g., "23:00") when the danger zone is active
    """
    data = request.json
    required_fields = ["name", "description", "coordinates", "active_from", "active_to"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    danger_zone = {
        "name": data["name"],
        "description": data["description"],
        "coordinates": data["coordinates"],
        "active_from": data["active_from"],
        "active_to": data["active_to"],
        "created_at": datetime.utcnow()
    }
    db.danger_zones.insert_one(danger_zone)
    return jsonify({"message": "Danger zone added successfully!"}), 201

@app.route('/danger_zones', methods=['GET'])
def get_danger_zones():
    """
    Get all defined danger zones.
    Later you can add filters (for time or proximity) as needed.
    """
    zones = list(db.danger_zones.find())
    for zone in zones:
        zone['_id'] = str(zone['_id'])
    return jsonify(zones), 200

# -------------------------
#  User Location & Safety Check
# -------------------------

# @app.route('/update_location', methods=['POST'])
# @jwt_required()
# def update_location():
#     """
#     Update the current user's location.
#     Expected JSON fields: latitude, longitude
#     """
#     username = get_jwt_identity()
#     data = request.json
#     if not data or "latitude" not in data or "longitude" not in data:
#         return jsonify({"error": "latitude and longitude are required"}), 400

#     db.users.update_one(
#         {"username": username},
#         {"$set": {
#             "location": {"latitude": data["latitude"], "longitude": data["longitude"]},
#             "location_updated_at": datetime.utcnow()
#         }}
#     )
#     return jsonify({"message": "Location updated successfully!"}), 200

# @app.route('/check_danger', methods=['GET'])
# @jwt_required()
# def check_danger():
#     """
#     A dummy endpoint to check if the user might be within a danger zone.
#     A real implementation would use geospatial queries.
#     """
#     username = get_jwt_identity()
#     user = db.users.find_one({"username": username})
#     if not user or "location" not in user:
#         return jsonify({"error": "User location not available"}), 400

#     user_location = user["location"]
#     danger_zones = list(db.danger_zones.find())
#     alerts = []

#     # Dummy geofencing logic:
#     # Replace this with a proper geospatial check using MongoDB’s geospatial queries or a library.
#     for zone in danger_zones:
#         # For demonstration, suppose any user with latitude > 40 is "in danger" for one or more zones.
#         if user_location["latitude"] > 40.0:
#             alerts.append(zone["name"])
    
#     if alerts:
#         return jsonify({
#             "message": "User is in or near danger zones.",
#             "zones": alerts
#         }), 200
#     else:
#         return jsonify({"message": "User is in a safe area."}), 200

# -------------------------
#  Additional Suggestions for Backend Endpoints
# -------------------------
#
# 1. Friend/Emergency Contact Management:
#    - Endpoints to add, update, or remove friends/emergency contacts.
#    - Endpoint to send the current location to a friend or contact.
#
# 2. Alerts & Notifications:
#    - Endpoint to record that an alert has been triggered.
#    - Integration with an SMS/email API (e.g., Twilio) to notify emergency contacts.
#
# 3. Safe Routes:
#    - Endpoint to get safe route recommendations (using an external mapping API).
#
# 4. Reporting:
#    - Endpoint for users to report incidents, which can later be used to update danger zone data.
#
# 5. AI Integration:
#    - Endpoint that calls an external AI service to analyze the current danger levels in a given area.
#
# You can build these endpoints step by step as you expand your app's functionality.

if __name__ == "__main__":
    app.run(debug=True)
