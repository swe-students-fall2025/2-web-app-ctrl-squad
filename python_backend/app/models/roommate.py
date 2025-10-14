from datetime import datetime
from bson.objectid import ObjectId
from app import db

class Roommate:
    collection = db.roommates
    
    @staticmethod
    def create_roommate_post(user_id, title, description, preferences=None, location=None):
        roommate_data = {
            'user_id': ObjectId(user_id),
            'title': title,
            'description': description,
            'preferences': preferences or {},
            'location': location,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = db.roommates.insert_one(roommate_data)
        roommate_data['_id'] = result.inserted_id
        return roommate_data
    
    @staticmethod
    def get_by_id(roommate_id):
        return db.roommates.find_one({'_id': ObjectId(roommate_id)})
    
    @staticmethod
    def get_all_roommate_posts():
        return list(db.roommates.find().sort('created_at', -1))
    
    @staticmethod
    def get_user_roommate_posts(user_id):
        return list(db.roommates.find({'user_id': ObjectId(user_id)}).sort('created_at', -1))
    
    @staticmethod
    def update_roommate_post(roommate_id, title=None, description=None, preferences=None, location=None):
        update_data = {'updated_at': datetime.utcnow()}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if preferences is not None:
            update_data['preferences'] = preferences
        if location is not None:
            update_data['location'] = location
        
        result = db.roommates.update_one(
            {'_id': ObjectId(roommate_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete_roommate_post(roommate_id):
        result = db.roommates.delete_one({'_id': ObjectId(roommate_id)})
        return result.deleted_count > 0