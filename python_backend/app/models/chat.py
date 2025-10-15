from datetime import datetime
from bson.objectid import ObjectId
from app import db
import json
from app.models.post import JSONEncoder

class Chat:
    collection = db.chats
    
    @staticmethod
    def create_chat(friend_id, friend_profile_pic=None):
        chat_data = {
            'friendId': ObjectId(friend_id),
            'friendProfilePic': friend_profile_pic,
            'messages': [],
            'timeUpdated': datetime.utcnow().isoformat()
        }
        result = Chat.collection.insert_one(chat_data)
        chat_data['_id'] = result.inserted_id
        return json.loads(json.dumps(chat_data, cls=JSONEncoder))
    
    @staticmethod
    def get_by_id(chat_id):
        try:
            chat = Chat.collection.find_one({'_id': ObjectId(chat_id)})
            return json.loads(json.dumps(chat, cls=JSONEncoder)) if chat else None
        except Exception as e:
            print(f"Error getting chat by id: {e}")
            raise
    
    @staticmethod
    def add_message(chat_id, from_user, text):
        try:
            message = {
                'from': from_user,
                'text': text,
                'time': datetime.utcnow().isoformat()
            }
            result = Chat.collection.update_one(
                {'_id': ObjectId(chat_id)},
                {
                    '$push': {'messages': message},
                    '$set': {'timeUpdated': datetime.utcnow().isoformat()}
                }
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error adding message to chat: {e}")
            raise
    
    @staticmethod
    def get_user_chats(user_id):
        try:
            chats = list(Chat.collection.find({'friendId': ObjectId(user_id)}).sort('timeUpdated', -1))
            return json.loads(json.dumps(chats, cls=JSONEncoder))
        except Exception as e:
            print(f"Error getting user chats: {e}")
            raise