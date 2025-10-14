from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all(k in data for k in ('email', 'username', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.get_by_email(data['email']):
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User.create_user(
        email=data['email'],
        username=data['username'],
        password=data['password']
    )
    
    login_user(user)
    return jsonify({'message': 'Registration successful', 'user': {'id': user.id, 'email': user.email, 'username': user.username}}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.get_by_email(data['email'])
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Login successful', 'user': {'id': user.id, 'email': user.email, 'username': user.username}})
    
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