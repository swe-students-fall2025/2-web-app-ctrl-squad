from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
import os
import pymongo
from bson.objectid import ObjectId

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
         "supports_credentials": True,
         "allow_headers": ["Content-Type", "Authorization"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
     }})

# Configure app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGODB_URI')

# Set up MongoDB connection
try:
    client = pymongo.MongoClient(os.getenv('MONGODB_URI'))
    client.server_info()  # Test connection
    db = client.get_default_database()
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None

# Enable debug mode
app.debug = True

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Import routes
from app.routes import auth, posts, roommates, trades, users
app.register_blueprint(auth.bp)  # Auth routes (using url_prefix from blueprint)
app.register_blueprint(posts.bp, url_prefix='/api')  # Posts under /api
app.register_blueprint(roommates.bp, url_prefix='/api')  # Roommates under /api
app.register_blueprint(trades.bp, url_prefix='/api')  # Trades under /api
app.register_blueprint(users.bp)  # Users routes (already has url_prefix in blueprint)

from flask import Blueprint, jsonify

base = Blueprint("base", __name__)

@base.get("/")
def root():
    return "Backend running", 200

@base.get("/health")
def health():
    return jsonify(ok=True), 200

app.register_blueprint(base)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT', 5000))