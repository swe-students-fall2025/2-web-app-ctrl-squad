from flask import Flask, jsonify, session
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

# Clean up any existing sessions in the database on server start
def cleanup_sessions():
    try:
        from app.models.user import User
        User.cleanup_sessions()  # This is a new method we'll add
        print("Successfully cleaned up all sessions on server start")
    except Exception as e:
        print(f"Error cleaning up sessions: {e}")

# Configure app and session handling
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-key-please-change'),
    MONGO_URI=os.getenv('MONGODB_URI'),
    
    # Session configuration
    SESSION_COOKIE_NAME='casaconnect_session',
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',  # Changed from None to Lax for better security
    SESSION_COOKIE_DOMAIN=None,  # Allow all domains in development
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),  # Reduced from 7 days to 1 day
    
    # Remember me cookie configuration
    REMEMBER_COOKIE_NAME='casaconnect_remember',
    REMEMBER_COOKIE_SECURE=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_SAMESITE='Lax',  # Changed from None to Lax for better security
    REMEMBER_COOKIE_DURATION=timedelta(days=7)  # Reduced from 14 days to 7 days
)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"  # Enable strong session protection
login_manager.refresh_view = "auth.login"    # Redirect to login for session refresh

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    if not user_id:
        print("Attempt to load user with empty ID")
        return None
        
    try:
        # Check if there's a mismatch between session user and requested user
        if 'user_id' in session and session['user_id'] != str(user_id):
            print(f"Session user mismatch: session={session['user_id']}, requested={user_id}")
            session.clear()
            return None
            
        user = User.get_by_id(user_id)
        if not user:
            print(f"No user found for ID: {user_id}")
            session.clear()
            return None
            
        # Validate session freshness
        if not session.get('_fresh', False):
            print(f"Stale session detected for user: {user_id}")
            session.clear()
            return None
            
        return user
        
    except Exception as e:
        print(f"Error loading user {user_id}: {e}")
        session.clear()
        return None

# Configure CORS
CORS(app, 
     resources={r"/*": {
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
    
    # Clean up sessions when server starts
    cleanup_sessions()
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
from app.routes import auth, posts, roommates, trades, users, search
app.register_blueprint(auth.bp)  # Auth routes (using url_prefix from blueprint)
app.register_blueprint(posts.bp, url_prefix='/api')  # Posts under /api
app.register_blueprint(roommates.bp, url_prefix='/api')  # Roommates under /api
app.register_blueprint(trades.bp, url_prefix='/api')  # Trades under /api
app.register_blueprint(users.bp)  # Users routes (already has url_prefix in blueprint)
app.register_blueprint(search.bp)  # Search routes (already has url_prefix in blueprint)

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