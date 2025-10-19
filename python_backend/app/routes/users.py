from flask import Blueprint, request, jsonify, session, make_response
from flask_login import login_required, current_user, login_user
from app.models.user import User
from app import db
from bson.objectid import ObjectId
import re

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
            'nyu_id': current_user.nyu_id,
            'bio': current_user.user_data.get('bio', '')
        }
    })

@bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    try:
        print("Headers:", dict(request.headers))
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        print("Raw request data:", request.get_data())
        print("Parsed update data:", data)  # Debug print
        
        # Ensure all required fields are present
        required_fields = ['username', 'email', 'nyu_id']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        # Clean and validate email
        email = str(data.get('email', '')).strip().lower()
        if not email.endswith('@nyu.edu'):
            return jsonify({'error': 'Email must be an NYU email address'}), 400
        
        # Just ensure NYU ID is not empty
        nyu_id = str(data.get('nyu_id', '')).strip()
        if not nyu_id:
            return jsonify({
                'success': False,
                'error': 'NYU ID cannot be empty'
            }), 400

        # Clean other fields
        username = str(data.get('username', '')).strip()
        bio = str(data.get('bio', '')).strip()

        # Update user profile
        update_data = {
            'email': email,
            'username': username,
            'nyu_id': nyu_id,
            'bio': bio
        }
        
        result = db.users.update_one(
            {'_id': ObjectId(current_user.id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No changes were made to the profile'
            }), 400
            
    except Exception as e:
        print(f"Error updating profile: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Server error while updating profile'
        }), 500
        
@bp.route('/profile/posts', methods=['GET', 'OPTIONS'])
@login_required
def get_user_posts():
    """Get all posts by the current user"""
    if request.method == 'OPTIONS':
        response = make_response()
        origin = request.headers.get('Origin')
        response.headers.update({
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, X-User-ID, Origin, Authorization',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '3600'
        })
        return response

    # Debug information
    print(f"Accessing posts endpoint. Method: {request.method}")
    print(f"Session data: {session}")
    print(f"Request cookies: {request.cookies}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Current user authenticated: {current_user.is_authenticated}")
    
    try:
        # Use the current user from the login_required decorator
        active_user_id = str(current_user.id)
        print(f"Active user ID for fetching posts: {active_user_id}")
        
        # Check X-User-ID header for consistency
        header_user_id = request.headers.get('X-User-ID')
        if header_user_id:
            if header_user_id == 'undefined' or header_user_id == 'null':
                print(f"Invalid X-User-ID header: {header_user_id}")
                # Continue using the session user ID
            elif header_user_id != active_user_id:
                print(f"Warning: X-User-ID header ({header_user_id}) doesn't match session user ({active_user_id})")
                # We'll still use the authenticated user from the session
        else:
            print("No X-User-ID header present, using session user")
        
        # Get user's posts from the database
        user_posts = list(db.posts.find({'user_id': active_user_id}))
        print(f"Found {len(user_posts)} posts for user {active_user_id}")
        
        # Convert ObjectId to string for JSON serialization
        for post in user_posts:
            post['_id'] = str(post['_id'])
            if 'user_id' in post:
                post['user_id'] = str(post['user_id'])
        
        response = jsonify({
            'success': True,
            'posts': user_posts
        })
        origin = request.headers.get('Origin')
        if origin:
            response.headers.update({
                'Access-Control-Allow-Origin': origin,
                'Access-Control-Allow-Credentials': 'true'
            })
        return response
    except Exception as e:
        print(f"Error fetching posts: {e}")
        response = jsonify({'error': f'Failed to fetch posts: {str(e)}'})
        origin = request.headers.get('Origin')
        if origin:
            response.headers.update({
                'Access-Control-Allow-Origin': origin,
                'Access-Control-Allow-Credentials': 'true'
            })
        return response, 500

@bp.route('/profile/posts/<post_type>', methods=['GET'])
@login_required
def get_user_posts_by_type(post_type):
    """Get all posts by the current user filtered by type (roommate or item)"""
    if post_type not in ['roommate', 'item']:
        return jsonify({'error': 'Invalid post type'}), 400
        
    try:
        # Get user's posts from the database filtered by type
        posts = list(db.posts.find({
            'user_id': current_user.id,
            'type': post_type
        }))
        
        # Convert ObjectId to string for JSON serialization
        for post in posts:
            post['_id'] = str(post['_id'])
            if 'user_id' in post:
                post['user_id'] = str(post['user_id'])
        
        return jsonify({
            'success': True,
            'data': posts
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        print(f"Error updating profile: {e}")
        return jsonify({'error': str(e)}), 500