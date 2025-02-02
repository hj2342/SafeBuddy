#import libraries to be used
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId
from datetime import datetime
import certifi

# added for file upload
# added to test PDF implementation
from werkzeug.utils import secure_filename
import os

# for password hashing
from werkzeug.security import generate_password_hash, check_password_hash

# for JWT authentication
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    unset_jwt_cookies
)

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# using mongodb atlas
client = MongoClient(
    "mongodb+srv://NYUADHackathon:NYUADHackathon@cluster0.x3t1u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    tlsCAFile=certifi.where()
)

# main database
db = client.Security

@app.route('/')
def home():
    return "connected to MongoDB Atlas"

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    Expected JSON fields: username, email, address, date_of_birth, password
    """
    data = request.json
    required_fields = ["username", "email", "address", "date_of_birth", "password"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Check if the username already exists
    if db.users.find_one({"username": data["username"]}):
        return jsonify({"error": "Username already exists"}), 409

    # Validate date_of_birth (expecting format "YYYY-MM-DD")
    try:
        datetime.strptime(data["date_of_birth"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Incorrect date format for date_of_birth. Use YYYY-MM-DD."}), 400

    # Hash the password
    hashed_password = generate_password_hash(data["password"])
    user = {
        "username": data["username"],
        "email": data["email"],
        "address": data["address"],
        "date_of_birth": data["date_of_birth"],
        "password": hashed_password,
        "created_at": datetime.utcnow()
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
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = db.users.find_one({"username": username})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Log out the current user.
    """
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200

@app.route('/delete_user/<username>', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    """
    Remove a user account.
    Only allow deletion if the logged-in user matches the username.
    """
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify({"error": "Unauthorized: can only delete your own account"}), 403

    result = db.users.delete_one({"username": username})
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted successfully!"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# -------------------------
# Danger Endpoints
# -------------------------

@app.route('/add_danger', methods=['POST'])
def add_danger():
    """
    Add a new danger.
    Expected JSON fields: location, description, date
    """
    data = request.json
    required_fields = ["location", "description", "date"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Validate date (expecting format "YYYY-MM-DD")
    try:
        datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Incorrect date format for date. Use YYYY-MM-DD."}), 400

    danger = {
        "location": data["location"],
        "description": data["description"],
        "date": data["date"],
        "created_at": datetime.utcnow()
    }
    db.dangers.insert_one(danger)
    return jsonify({"message": "Danger added successfully!"}), 201

@app.route('/get_dangers', methods=['GET'])
def get_dangers():
    """
    Retrieve all dangers.
    """
    dangers = list(db.dangers.find())
    for danger in dangers:
        danger['_id'] = str(danger['_id'])
    return jsonify(dangers), 200

@app.route('/get_users', methods=['GET'])
def get_users():
    """
    Retrieve all users.
    This endpoint returns a list of all users without their password hashes.
    """
    users = list(db.users.find())
    for user in users:
        user['_id'] = str(user['_id'])
        if 'password' in user:
            del user['password']
    return jsonify(users), 200
locations = []

@app.route('/api/location', methods=['POST'])
def save_location():
    try:
        data = request.get_json()  # Get JSON data from frontend
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is None or longitude is None:
            return jsonify({"error": "Missing latitude or longitude"}), 400

        # Save to "database" (for now, just append to a list)
        location_entry = {"latitude": latitude, "longitude": longitude}
        locations.append(location_entry)

        print(f"Received location: {latitude}, {longitude}")

        return jsonify({"message": "Location saved successfully!", "location": location_entry}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True)
