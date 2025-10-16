from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
from datetime import timedelta
import os
import pymongo
from bson.objectid import ObjectId

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure app
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-key-please-change'),
    MONGO_URI=os.getenv('MONGODB_URI'),
    SESSION_COOKIE_NAME='casaconnect_session',
    SESSION_COOKIE_SAMESITE='None',  # Required for cross-origin requests
    SESSION_COOKIE_SECURE=True,  # Required when SameSite is None
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_DOMAIN=None,  # Allow all domains in development
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
    REMEMBER_COOKIE_NAME='casaconnect_remember',
    REMEMBER_COOKIE_SAMESITE='None',  # Required for cross-origin requests
    REMEMBER_COOKIE_SECURE=True,  # Required when SameSite is None
    REMEMBER_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_DURATION=timedelta(days=14)
)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = None  # Disable session protection for development

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    print(f"Loading user: {user_id}")
    return User.get_by_id(user_id)

# Configure CORS
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
         "allow_credentials": True,
         "expose_headers": ["Set-Cookie", "Authorization"],
         "allow_headers": ["Content-Type", "Authorization", "Cookie", "Accept"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "max_age": 3600
     }},
     supports_credentials=True)

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

# Custom unauthorized handler for API requests
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error': 'Authentication required'}), 401

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