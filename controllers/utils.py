from functools import wraps
from flask import request, jsonify, current_app
import jwt
from pymongo import MongoClient

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_email = payload.get('sub')  # Assuming 'sub' contains the user's email
            
            if not user_email:
                return jsonify({'message': 'Invalid token'}), 401
            
            # Fetch user data based on email from MongoDB or your user database
            client = MongoClient('mongodb+srv://guest:Anaguest@bdcc.ltvlqmq.mongodb.net/')
            db = client['dataset_db']
            users_collection = db['users']
            
            user = users_collection.find_one({'email': user_email})
            
            if not user:
                return jsonify({'message': 'User not found'}), 401

            # Pass user details to the route function
            return f(user, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

    return decorated
