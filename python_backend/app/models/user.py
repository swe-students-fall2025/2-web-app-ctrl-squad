from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from bson.objectid import ObjectId
from datetime import datetime, timedelta

class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
    
    def get_id(self):
        return str(self.user_data.get('_id'))
    
    @property
    def is_authenticated(self):
        return bool(self.user_data and self.user_data.get('_id'))
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def id(self):
        return str(self.user_data.get('_id'))
    
    @property
    def email(self):
        return self.user_data.get('email')
    
    @property
    def username(self):
        return self.user_data.get('username')
    
    @property
    def nyu_id(self):
        return self.user_data.get('nyu_id')
    
    def check_password(self, password):
        return check_password_hash(self.user_data.get('password'), password)
    
    @staticmethod
    def create_user(email, username, password, nyu_id=None):
        user_data = {
            'email': email,
            'username': username,
            'password': generate_password_hash(password),
            'nyu_id': nyu_id,
            'posts': [],
            'roommates': [],
            'trades': [],
            'is_active': True
        }
        result = db.users.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return User(user_data)
        
    @staticmethod
    def get_by_id(user_id):
        try:
            if not user_id:
                print("Warning: Attempted to load user with empty ID")
                return None
                
            # Handle string IDs properly
            if isinstance(user_id, str):
                if not ObjectId.is_valid(user_id):
                    print(f"Warning: Invalid ObjectId format: {user_id}")
                    return None
                user_id = ObjectId(user_id)
                
            user_data = db.users.find_one({'_id': user_id})
            if not user_data:
                print(f"Warning: No user found with ID {user_id}")
                return None
                
            return User(user_data)
        except Exception as e:
            print(f"Error in get_by_id: {str(e)}")
            return None
    
    @staticmethod
    def get_by_email(email):
        user_data = db.users.find_one({'email': email})
        return User(user_data) if user_data else None

    def set_reset_token(self, token, expiry):
        """Set a password reset token and its expiry time"""
        db.users.update_one(
            {'_id': ObjectId(self.id)},
            {'$set': {
                'reset_token': token,
                'reset_token_expiry': expiry
            }}
        )
    
    def clear_reset_token(self):
        """Clear the password reset token"""
        db.users.update_one(
            {'_id': ObjectId(self.id)},
            {'$unset': {
                'reset_token': '',
                'reset_token_expiry': ''
            }}
        )
    
    @staticmethod
    def get_by_reset_token(token):
        """Get a user by their reset token"""
        user_data = db.users.find_one({
            'reset_token': token,
            'reset_token_expiry': {'$gt': datetime.utcnow()}
        })
        return User(user_data) if user_data else None
    
    def set_password(self, password):
        """Update user's password"""
        db.users.update_one(
            {'_id': ObjectId(self.id)},
            {'$set': {'password': generate_password_hash(password)}}
        )
        
    @staticmethod
    def get_by_nyu_id(nyu_id):
        user_data = db.users.find_one({'nyu_id': nyu_id})
        return User(user_data) if user_data else None