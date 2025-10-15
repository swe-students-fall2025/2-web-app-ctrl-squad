from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
    
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
            'trades': []
        }
        result = db.users.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return User(user_data)
    
    @staticmethod
    def get_by_id(user_id):
        user_data = db.users.find_one({'_id': ObjectId(user_id)})
        return User(user_data) if user_data else None
    
    @staticmethod
    def get_by_email(email):
        user_data = db.users.find_one({'email': email})
        return User(user_data) if user_data else None
        
    @staticmethod
    def get_by_nyu_id(nyu_id):
        user_data = db.users.find_one({'nyu_id': nyu_id})
        return User(user_data) if user_data else None