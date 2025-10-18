from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
import sys
from pprint import pformat
from app.models.user import User
import secrets
from datetime import datetime, timedelta

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
            
            # Clear any existing session data first
            session.clear()
            
            # Mark session as permanent
            session.permanent = True
            print(f"Session before login: {session}")
            
            # Log out any existing user first
            logout_user()
            
            # Log in the new user
            success = login_user(user, remember=True, force=True)
            if not success:
                return jsonify({'error': 'Failed to log in user'}), 500
                
            print(f"Login success: {success}, User ID: {user.id}")
            
            # Set new session data
            session['user_id'] = str(user.id)
            session['email'] = user.email
            session.modified = True
            
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

    logout_user()  # Clear Flask-Login's session
    session.clear()  # Clear all session data
    
    response = jsonify({'message': 'Logged out successfully'})
    
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