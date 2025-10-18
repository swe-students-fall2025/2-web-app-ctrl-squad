from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
import sys
from pprint import pformat
from app.models.user import User
import secrets
from datetime import datetime, timedelta
from bson.objectid import ObjectId

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        # Handling preflight request
        response = jsonify({'status': 'ok'})
        return response

    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.get_json()
    print("Received registration data:", data)  # Debug print
    
    if not all(k in data for k in ('email', 'username', 'password', 'NetID')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate NYU email
    if not data['email'].endswith('@nyu.edu'):
        return jsonify({'error': 'Must use an NYU email address'}), 400
    
    # Check if NetID is not empty
    if not data['NetID'].strip():
        return jsonify({'error': 'NetID is required'}), 400
    
    # Check if email is already registered
    if User.get_by_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 400
    
    # Check if NetID is already registered
    if User.get_by_nyu_id(data['NetID']):
        return jsonify({'error': 'NetID already registered'}), 400
        
    # Check if username is already taken
    # Using the db connection from app
    from app import db
    existing_user = db.users.find_one({'username': data['username']})
    if existing_user:
        return jsonify({'error': 'Username already taken'}), 400
    
    user = User.create_user(
        email=data['email'],
        username=data['username'],
        password=data['password'],
        nyu_id=data['NetID']
    )
    
    if user is None:
        return jsonify({'error': 'Failed to create user. Please try again.'}), 400
    
    login_user(user)
    return jsonify({'message': 'Registration successful', 'user': {'id': user.id, 'email': user.email, 'username': user.username}}), 201

@bp.route('/login', methods=['GET', 'POST', 'OPTIONS'])
def login():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return response
        
    # Clear any existing session data
    logout_user()
    session.clear()

    try:
        # Check if user is already authenticated
        if current_user.is_authenticated:
            print(f"User already authenticated: {current_user.id}")
            response = jsonify({
                'success': True,
                'message': 'Already logged in',
                'user': {
                    'id': current_user.id,
                    'email': current_user.email,
                    'username': current_user.username
                }
            })
            response.headers.update({
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Origin': request.headers.get('Origin'),
                'Access-Control-Expose-Headers': 'Set-Cookie'
            })
            return response
    except Exception as e:
        print(f"Error checking authentication: {e}")
        return jsonify({'success': False, 'error': 'Authentication error'}), 500

    if request.method == 'OPTIONS':
        return '', 200
        
    if request.method == 'GET':
        # Return a JSON response for GET requests to /login
        return jsonify({'error': 'Please login'}), 401
        
    data = request.get_json()
    print("Received login data:", data)  # Debug print
    
    if not all(k in data for k in ('email', 'password')):
        print("Missing required fields")  # Debug print
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.get_by_email(data['email'])
    print("Found user:", user.user_data if user else None)  # Debug print
    
    if user:
        print("Stored password hash:", user.user_data.get('password'))
        print("Checking password:", data['password'])
        if user.check_password(data['password']):
            print("Password check succeeded")
            
            print(f"Starting login process for user ID: {user.id}")
            
            # Clear any existing session data
            if current_user.is_authenticated:
                print(f"Found existing authenticated user: {current_user.id}")
                logout_user()
                
            session.clear()
            print("Cleared session")
            
            # Expire all existing cookies in response
            response = jsonify({
                'success': True,
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'username': user.username
                }
            })
            
            for cookie in request.cookies:
                response.delete_cookie(cookie)
            
            # Set up fresh session
            session.permanent = True
            
            # Log in the new user with fresh session
            if not login_user(user, remember=True, fresh=True):
                print(f"Failed to login user: {user.id}")
                return jsonify({'error': 'Failed to log in user'}), 500
            
            # Set minimal session data
            session['user_id'] = str(user.id)
            session['_fresh'] = True
            session.modified = True
            
            print(f"Successfully logged in user: {user.id}")
            
            # Verify the logged-in user
            if current_user.is_authenticated:
                print(f"Verified logged in user: {current_user.id}")
            else:
                print("Warning: User not authenticated after login!")
                
            return response
            
            print(f"Session after setting data: {session}")
            
            # Create response with user data
            response = jsonify({
                'success': True,
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'username': user.username
                }
            })
            
            # Add required CORS and cookie headers
            origin = request.headers.get('Origin')
            response.headers.update({
                'Access-Control-Allow-Origin': origin,
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Expose-Headers': 'Set-Cookie, Authorization',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Content-Type': 'application/json'
            })
            
            # Add secure cookie settings
            response.set_cookie(
                'session',
                session.get('_id'),
                secure=True,
                httponly=True,
                samesite='None',
                max_age=7 * 24 * 3600  # 7 days
            )
            
            print(f"Current user after login: {current_user.id if current_user.is_authenticated else 'Not authenticated'}")
            print(f"Final session state: {session}")
            print(f"Response headers: {dict(response.headers)}")
            
            # Test if the user loader works
            from app import login_manager
            test_user = login_manager.user_callback(user.id)
            print(f"Test user load: {test_user.id if test_user else 'None'}")
            
            return response
        else:
            print("Password check failed")
    
    if not user:
        print("User not found")  # Debug print
        return jsonify({'error': 'Invalid email or password'}), 401
    
    print("Password incorrect")  # Debug print
    return jsonify({'error': 'Invalid email or password'}), 401

@bp.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return response

    try:
        # Get user info before logout for logging
        user_id = current_user.get_id() if current_user.is_authenticated else None
        print(f"Starting logout for user: {user_id}")
        
        # If we have a logged-in user, update their record
        if user_id:
            from app import db
            db.users.update_one(
                {'_id': ObjectId(user_id)},
                {'$unset': {
                    'session_token': '',
                    'remember_token': '',
                }}
            )
        
        # Clear Flask-Login's session
        logout_user()
        
        # Clear all session data
        session.clear()
        
        # Create response
        response = jsonify({'message': 'Logged out successfully'})
        
        # Force expire all cookies
        for cookie in request.cookies:
            response.delete_cookie(cookie, path='/', domain=None)
        
        # Explicitly expire our known cookies with all variations
        cookie_names = ['casaconnect_session', 'casaconnect_remember', 'session', 'remember_token']
        paths = ['/', '/api', '/api/auth']
        
        for cookie_name in cookie_names:
            for path in paths:
                response.delete_cookie(cookie_name, path=path, domain=None)
                response.set_cookie(cookie_name, '', expires=0, secure=True,
                                 httponly=True, samesite='Lax', domain=None, path=path)
        
        print(f"Successfully logged out user: {user_id}")
        return response
        
    except Exception as e:
        print(f"Error during logout: {e}")
        # Even if there's an error, try to clear everything
        session.clear()
        response = jsonify({'message': 'Logged out with errors'})
        response.set_cookie('casaconnect_session', '', expires=0)
        response.set_cookie('casaconnect_remember', '', expires=0)
        response.set_cookie('session', '', expires=0)
        return response
    # Clear the session cookie
    response.delete_cookie('session', 
                         secure=True, 
                         httponly=True, 
                         samesite='None',
                         domain=None,
                         path='/')
    
    # Add CORS headers
    origin = request.headers.get('Origin')
    response.headers.update({
        'Access-Control-Allow-Origin': origin,
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    })
    
    return response

@bp.route('/reset-password', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    if 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400
        
    user = User.get_by_email(data['email'])
    if not user:
        # Don't reveal that the user doesn't exist
        return jsonify({'message': 'If your email is registered, you will receive a password reset link'}), 200
        
    # Generate reset token
    token = secrets.token_urlsafe(32)
    expiry = datetime.utcnow() + timedelta(hours=1)
    user.set_reset_token(token, expiry)
    
    # TODO: Send reset email
    # For now, just return the token
    return jsonify({
        'message': 'Password reset link sent',
        'token': token  # Remove this in production
    }), 200

@bp.route('/reset-password/<token>', methods=['GET'])
def verify_reset_token(token):
    user = User.get_by_reset_token(token)
    if not user:
        return jsonify({'error': 'Invalid or expired reset token'}), 400
    return jsonify({'message': 'Valid reset token'}), 200

@bp.route('/reset-password/<token>', methods=['PUT'])
def reset_password(token):
    data = request.get_json()
    if 'password' not in data:
        return jsonify({'error': 'New password is required'}), 400
        
    user = User.get_by_reset_token(token)
    if not user:
        return jsonify({'error': 'Invalid or expired reset token'}), 400
        
    user.set_password(data['password'])
    user.clear_reset_token()
    
    return jsonify({'message': 'Password reset successful'}), 200

@bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify({
        'id': current_user.id,
        'email': current_user.email,
        'username': current_user.username
    })