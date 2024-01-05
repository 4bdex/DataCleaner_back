from pymongo import MongoClient
from flask_bcrypt import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from flask import current_app

try:
    client = MongoClient('mongodb+srv://guest:Anaguest@bdcc.ltvlqmq.mongodb.net/')
    db = client['DataCleaner']
    collection = db['users']
except Exception as e:
    print("error while connecting to mongoDB Atlas")
class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def save_to_db(self):
        user_data = {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        collection.insert_one(user_data)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': self.email
            }
            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
            return token
        except Exception as e:
            return str(e)
