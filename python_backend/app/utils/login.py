from flask import session, request, jsonify
from app.models.user import User
import logging

# Login utility functions
# Note: The main user_loader function is now in __init__.py

def verify_session_token(user):
    """Verify that a user's session token is valid"""
    if not user or not user.is_authenticated:
        return False
        
    # Additional session validation could be added here
    return True
    
def get_current_user_from_header():
    """Get the current user based on the X-User-ID header"""
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return None
        
    return User.get_by_id(user_id)
    
def update_session_consistency(user_id):
    """Make sure session user ID matches the currently logged in user"""
    if not user_id:
        return False
        
    if 'user_id' not in session or session['user_id'] != str(user_id):
        session['user_id'] = str(user_id)
        print(f"Updated session user ID: {user_id}")
        return True
    
    return False