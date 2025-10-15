from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.user import User
from app import db

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/')
@bp.route('')
def list_users():
    users = list(db.users.find())
    # Convert ObjectId to string for JSON serialization
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

@bp.route('/collections')
def list_collections():
    collections = db.list_collection_names()
    return jsonify(collections)

@bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify({
        'success': True,
        'data': {
            'id': str(current_user.id),
            'email': current_user.email,
            'username': current_user.username,
            'account_name': current_user.account_name,
            'nyu_id': current_user.nyu_id,
            'bio': current_user.bio
        }
    })

@bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()
    
    # Validate email format
    if 'email' in data and not data['email'].endswith('@nyu.edu'):
        return jsonify({'error': 'Email must be an NYU email address'}), 400
    
    # Validate NYU ID format
    if 'nyu_id' in data and not (data['nyu_id'].startswith('N') and len(data['nyu_id']) == 8):
        return jsonify({'error': 'NYU ID must be in format N1234567'}), 400
    
    try:
        success = User.update_user(
            user_id=current_user.id,
            account_name=data.get('account_name'),
            email=data.get('email'),
            nyu_id=data.get('nyu_id'),
            bio=data.get('bio')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully'
            })
        else:
            return jsonify({'error': 'Failed to update profile'}), 500
            
    except Exception as e:
        print(f"Error updating profile: {e}")
        return jsonify({'error': str(e)}), 500