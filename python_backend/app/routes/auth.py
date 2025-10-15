from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    data = request.get_json()
    print("Received registration data:", data)  # Debug print
    
    if not all(k in data for k in ('email', 'username', 'password', 'NetID')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate NYU email
    if not data['email'].endswith('@nyu.edu'):
        return jsonify({'error': 'Must use an NYU email address'}), 400
    
    # Validate NetID format
    if not (data['NetID'].startswith('N') and len(data['NetID']) == 8):
        return jsonify({'error': 'NetID must be in format N1234567'}), 400
    
    if User.get_by_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User.create_user(
        email=data['email'],
        username=data['username'],
        password=data['password'],
        nyu_id=data['NetID']
    )
    
    login_user(user)
    return jsonify({'message': 'Registration successful', 'user': {'id': user.id, 'email': user.email, 'username': user.username}}), 201

@bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
        
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
            login_user(user)
            return jsonify({'message': 'Login successful', 'user': {'id': user.id, 'email': user.email, 'username': user.username}})
        else:
            print("Password check failed")
    
    if not user:
        print("User not found")  # Debug print
        return jsonify({'error': 'Invalid email or password'}), 401
    
    print("Password incorrect")  # Debug print
    return jsonify({'error': 'Invalid email or password'}), 401

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify({
        'id': current_user.id,
        'email': current_user.email,
        'username': current_user.username
    })