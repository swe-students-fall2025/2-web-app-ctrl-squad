from datetime import datetime
from bson.objectid import ObjectId
from app import db

class Trade:
    collection = db.trades
    
    @staticmethod
    def create_trade(user_id, item_name, description, images=None, trade_preferences=None):
        trade_data = {
            'user_id': ObjectId(user_id),
            'item_name': item_name,
            'description': description,
            'images': images or [],
            'trade_preferences': trade_preferences or {},
            'status': 'open',  # open, pending, completed, cancelled
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = db.trades.insert_one(trade_data)
        trade_data['_id'] = result.inserted_id
        return trade_data
    
    @staticmethod
    def get_by_id(trade_id):
        return db.trades.find_one({'_id': ObjectId(trade_id)})
    
    @staticmethod
    def get_all_trades():
        return list(db.trades.find({'status': 'open'}).sort('created_at', -1))
    
    @staticmethod
    def get_user_trades(user_id):
        return list(db.trades.find({
            '$or': [
                {'user_id': ObjectId(user_id)},
                {'interested_users': ObjectId(user_id)}
            ]
        }).sort('created_at', -1))
    
    @staticmethod
    def update_trade(trade_id, item_name=None, description=None, images=None, trade_preferences=None, status=None):
        update_data = {'updated_at': datetime.utcnow()}
        if item_name is not None:
            update_data['item_name'] = item_name
        if description is not None:
            update_data['description'] = description
        if images is not None:
            update_data['images'] = images
        if trade_preferences is not None:
            update_data['trade_preferences'] = trade_preferences
        if status is not None:
            update_data['status'] = status
        
        result = db.trades.update_one(
            {'_id': ObjectId(trade_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def express_interest(trade_id, user_id):
        result = db.trades.update_one(
            {'_id': ObjectId(trade_id)},
            {'$addToSet': {'interested_users': ObjectId(user_id)}}
        )
        return result.modified_count > 0
    
    @staticmethod
    def remove_interest(trade_id, user_id):
        result = db.trades.update_one(
            {'_id': ObjectId(trade_id)},
            {'$pull': {'interested_users': ObjectId(user_id)}}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete_trade(trade_id):
        result = db.trades.delete_one({'_id': ObjectId(trade_id)})
        return result.deleted_count > 0