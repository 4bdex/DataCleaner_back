from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from flask_bcrypt import generate_password_hash
from models.user_model import User


try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['DataCleaner']
    collection = db['users']
except Exception as e:
    print("error while connecting to mongoDB Atlas")

def signup():
    try:
        data = request.get_json()
        if not data or not data['username'] or not data['email'] or not data['password']:
            return jsonify({'message': 'Please provide all required fields'}), 400
        user = User(username=data['username'],email=data['email'], password=generate_password_hash(data['password']).decode('utf-8'))
        user.save_to_db()
        return jsonify({'message': 'User registered successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
def login():
    data = request.get_json()
    if not data or not data['email'] or not data['password']:
        return jsonify({'message': 'Please provide your email and password'}), 400
    user = collection.find_one({'email': data['email']})
    if user and User(user['username'],user['email'], user['password']).check_password(data['password']):
        token = User(user['username'],user['email'], user['password']).generate_auth_token()
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401