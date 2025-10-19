from flask import Flask, jsonify, session, request
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

# Handle proper HTTPS detection for secure cookies
@app.before_request
def handle_https():
    # Check if we're running behind a proxy that terminates HTTPS
    x_forwarded_proto = request.headers.get('X-Forwarded-Proto')
    x_forwarded_ssl = request.headers.get('X-Forwarded-Ssl')
    
    if x_forwarded_proto == 'https' or x_forwarded_ssl == 'on':
        # Force Flask to consider this a secure connection for cookie purposes
        request.environ['wsgi.url_scheme'] = 'https'

# Development mode flag
DEV_MODE = os.getenv('FLASK_ENV') == 'development' or os.getenv('DEV_MODE') == 'true'

# Configure app and session handling
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-key-please-change'),
    MONGO_URI=os.getenv('MONGODB_URI'),
    
    # Session configuration
    SESSION_COOKIE_NAME='casaconnect_session',
    SESSION_COOKIE_SECURE=not DEV_MODE,  # Set to False in development (HTTP), True in production
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax' if DEV_MODE else 'None',  # Use Lax in development, None in production
    SESSION_COOKIE_DOMAIN=None,  # Allow all domains in development
    PERMANENT_SESSION_LIFETIME=timedelta(days=1),  # One day session lifetime
    SESSION_TYPE='filesystem',  # Use filesystem session storage
    
    # Remember me cookie configuration
    REMEMBER_COOKIE_NAME='casaconnect_remember',
    REMEMBER_COOKIE_SECURE=not DEV_MODE,  # Set to False in development (HTTP), True in production
    REMEMBER_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_SAMESITE='Lax' if DEV_MODE else 'None',  # Use Lax in development, None in production
    REMEMBER_COOKIE_DURATION=timedelta(days=7)  # Reduced from 14 days to 7 days
)

# Force development mode for now
os.environ['FLASK_ENV'] = 'development'
os.environ['DEV_MODE'] = 'true'

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"  # Enable strong session protection
login_manager.refresh_view = "auth.login"    # Redirect to login for session refresh

@login_manager.user_loader
def load_user(user_id):
    print(f"Attempting to load user with ID: {user_id}")
    
    # Skip validation if no user_id
    if not user_id:
        print("No user ID provided")
        return None
    
    try:
        # Get the user from database
        print(f"Looking up user with ObjectId: {user_id}")
        from app.models.user import User
        user = User.get_by_id(user_id)
        
        if user:
            print(f"Found user data: {user.username} (ID: {user.id})")
            
            # Check if X-User-ID header is present
            user_id_header = request.headers.get('X-User-ID')
            if user_id_header:
                if user_id_header == 'undefined' or user_id_header == 'null' or not user_id_header.strip():
                    print(f"Invalid X-User-ID header value: {user_id_header}")
                    print("Using session user ID instead")
                elif user_id_header != str(user.id):
                    # Log mismatch but don't reject - session user takes precedence
                    print(f"User ID mismatch: header={user_id_header}, session={user.id}")
                    print(f"Prioritizing session user_id")
            else:
                print(f"No X-User-ID header present, using session user")
                
            # Store user ID in session for consistency
            if 'user_id' not in session or session['user_id'] != str(user.id):
                session['user_id'] = str(user.id)
                print(f"Updated session user ID: {session['user_id']}")
                
            return user
        else:
            print(f"No user found for ID: {user_id}")
            return None
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

# Configure CORS to handle cross-origin requests
CORS(app, 
     resources={r"/*": {
         # Allow all origins for development (consider restricting in production)
         "origins": ["http://127.0.0.1:5500", "http://localhost:5500", "http://localhost:5000", 
                    "http://127.0.0.1:5501", "http://localhost:5501"],
         "allow_credentials": True,
         "expose_headers": ["Set-Cookie", "X-User-ID", "Content-Type", "Authorization"],
         "allow_headers": ["Content-Type", "Cookie", "Accept", "Origin", "X-User-ID", 
                          "X-Requested-With", "Authorization", "Cache-Control"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "max_age": 3600,
         "supports_credentials": True
     }},
     supports_credentials=True)
     
# Make sessions permanent by default
@app.before_request
def make_session_permanent():
    session.permanent = True

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
    print("Unauthorized access attempt - login_required failed")
    
    # Debug info to help diagnose the issue
    print(f"Request path: {request.path}")
    print(f"Request method: {request.method}")
    print(f"Session: {session}")
    print(f"Headers: {dict(request.headers)}")
    
    # Add CORS headers for better browser handling
    response = jsonify({'error': 'Authentication required'})
    origin = request.headers.get('Origin')
    if origin:
        response.headers.update({
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        })
    
    return response, 401

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