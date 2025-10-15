from datetime import datetime
from bson.objectid import ObjectId
from app import db
import json
from app.models.post import JSONEncoder

class Message:
    collection = db.messages
    
    @staticmethod
    def create_message(sender_id, receiver_id, message):
        message_data = {
            'senderId': ObjectId(sender_id),
            'receiverId': ObjectId(receiver_id),
            'message': message,
            'timeSent': datetime.utcnow().isoformat()
        }
        result = Message.collection.insert_one(message_data)
        message_data['_id'] = result.inserted_id
        return json.loads(json.dumps(message_data, cls=JSONEncoder))
    
    @staticmethod
    def get_conversation(user1_id, user2_id, limit=50):
        try:
            # Get messages where either user is sender and the other is receiver
            messages = list(Message.collection.find({
                '$or': [
                    {'senderId': ObjectId(user1_id), 'receiverId': ObjectId(user2_id)},
                    {'senderId': ObjectId(user2_id), 'receiverId': ObjectId(user1_id)}
                ]
            }).sort('timeSent', -1).limit(limit))
            return json.loads(json.dumps(messages, cls=JSONEncoder))
        except Exception as e:
            print(f"Error getting conversation: {e}")
            raise
    
    @staticmethod
    def get_user_messages(user_id, limit=50):
        try:
            # Get messages where user is either sender or receiver
            messages = list(Message.collection.find({
                '$or': [
                    {'senderId': ObjectId(user_id)},
                    {'receiverId': ObjectId(user_id)}
                ]
            }).sort('timeSent', -1).limit(limit))
            return json.loads(json.dumps(messages, cls=JSONEncoder))
        except Exception as e:
            print(f"Error getting user messages: {e}")
            raise