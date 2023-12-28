from flask import Flask
from pymongo import MongoClient
from routes import init_app_routes
from flask_cors import CORS

app = Flask(__name__)


init_app_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
