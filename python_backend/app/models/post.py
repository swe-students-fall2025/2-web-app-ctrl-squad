from datetime import datetime
import json
from bson.objectid import ObjectId
from app import db

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

class Post:
    collection = db.posts
    
    @staticmethod
    def create_post(user_id, title, description, type='item', category=None, condition=None, images=None, price=None, status='Available'):
        try:
            post_data = {
                'user_id': ObjectId(user_id),
                'title': title,
                'description': description,
                'type': type,
                'category': category,
                'condition': condition,
                'images': images or [],
                'price': price,
                'status': status,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            result = Post.collection.insert_one(post_data)
            post_data['_id'] = result.inserted_id
            return json.loads(json.dumps(post_data, cls=JSONEncoder))
        except Exception as e:
            print(f"Error creating post: {e}")
            raise
    
    @staticmethod
    def get_by_id(post_id):
        try:
            post = Post.collection.find_one({'_id': ObjectId(post_id)})
            return json.loads(json.dumps(post, cls=JSONEncoder)) if post else None
        except Exception as e:
            print(f"Error getting post by id: {e}")
            raise
    
    @staticmethod
    def get_posts_by_user(user_id):
        try:
            posts = list(Post.collection.find({'user_id': ObjectId(user_id)}).sort('created_at', -1))
            return json.loads(json.dumps(posts, cls=JSONEncoder))
        except Exception as e:
            print(f"Error getting posts by user: {e}")
            raise

    @staticmethod
    def delete_post(post_id):
        try:
            result = Post.collection.delete_one({'_id': ObjectId(post_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting post: {e}")
            raise

    @staticmethod
    def get_all_posts():
        try:
            posts = list(Post.collection.find().sort('created_at', -1))
            return json.loads(json.dumps(posts, cls=JSONEncoder))
        except Exception as e:
            print(f"Error getting all posts: {e}")
            raise
    
    @staticmethod
    def get_user_posts(user_id):
        try:
            posts = list(Post.collection.find({'user_id': ObjectId(user_id)}).sort('created_at', -1))
            return json.loads(json.dumps(posts, cls=JSONEncoder))
        except Exception as e:
            print(f"Error getting user posts: {e}")
            raise
    
    @staticmethod
    def update_post(post_id, title=None, description=None, images=None, price=None):
        try:
            update_data = {'updated_at': datetime.utcnow()}
            if title is not None:
                update_data['title'] = title
            if description is not None:
                update_data['description'] = description
            if images is not None:
                update_data['images'] = images
            if price is not None:
                update_data['price'] = price
            
            result = Post.collection.update_one(
                {'_id': ObjectId(post_id)},
                {'$set': update_data}
            )
            
            if result.modified_count:
                post = Post.get_by_id(post_id)
                return post
            return None
        except Exception as e:
            print(f"Error updating post: {e}")
            raise
        return result.modified_count > 0
    
    @staticmethod
    def delete_post(post_id):
        result = db.posts.delete_one({'_id': ObjectId(post_id)})
        return result.deleted_count > 0