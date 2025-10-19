from functools import wraps
from flask import request, jsonify
from bson import ObjectId
from app.models.user import User

def header_auth_required(f):
    """
    Decorator that checks for X-User-ID header and authenticates the user.
    Use this instead of login_required for endpoints that should use header-based auth.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get user ID from X-User-ID header
        user_id = request.headers.get('X-User-ID')
        
        # Check if X-User-ID is present and valid
        if not user_id or user_id == 'undefined' or user_id == 'null' or not user_id.strip():
            print(f"Missing or invalid X-User-ID header: {user_id}")
            return jsonify({'error': 'X-User-ID header is required for authentication'}), 401
        
        # Try to validate the user ID
        try:
            # Verify it's a valid ObjectId
            object_id = ObjectId(user_id)
            
            # Optional: Check if the user exists
            # user = User.get_by_id(user_id)
            # if not user:
            #     print(f"User with ID {user_id} not found")
            #     return jsonify({'error': 'User not found'}), 404
            
            print(f"Authenticated request using X-User-ID: {user_id}")
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Error validating user ID from header: {e}")
            return jsonify({'error': 'Invalid user ID'}), 401
    
    return decorated