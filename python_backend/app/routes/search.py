from flask import Blueprint, request, jsonify
from app import db
from bson.objectid import ObjectId
from flask_cors import cross_origin
from bson import json_util
import json

bp = Blueprint('search', __name__, url_prefix='/api')

@bp.route('/search', methods=['GET', 'OPTIONS'])
@bp.route('/search/', methods=['GET', 'OPTIONS'])
@cross_origin(origins=["http://127.0.0.1:5500", "http://localhost:5500"], 
              supports_credentials=True,
              allow_headers=["Content-Type", "Authorization", "X-Requested-With"])
def search():
    if request.method == 'OPTIONS':
        return '', 200
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'success': True,
            'results': []
        })

    # Search in posts collection using a case-insensitive regex
    results = list(db.posts.find({
        '$or': [
            {'title': {'$regex': query, '$options': 'i'}},
            {'description': {'$regex': query, '$options': 'i'}},
            {'type': {'$regex': query, '$options': 'i'}}
        ]
    }).sort('created_at', -1).limit(20))  # Limit to 20 results and sort by newest first

    formatted_results = []
    
    try:
        for result in results:
            formatted_post = {
                '_id': str(result.get('_id')),
                'title': result.get('title', 'Untitled'),
                'description': result.get('description', ''),
                'image_url': result.get('image_url') if result.get('image_url') else None,
                'images': result.get('images', []),  # Include all images if available
                'type': result.get('type', 'item'),
                'created_at': result.get('created_at', None),
                'favorites_count': len(result.get('favorites', [])),
                'favorites': [str(fav) if isinstance(fav, ObjectId) else fav for fav in result.get('favorites', [])]
            }
            
            # Handle author information
            # Handle author information
            try:
                user_id = result.get('user_id')  # Changed from author_id to user_id
                if user_id:
                    if isinstance(user_id, ObjectId):
                        author = db.users.find_one({'_id': user_id})
                    else:
                        author = db.users.find_one({'_id': ObjectId(str(user_id))})
                    
                    if author:
                        formatted_post['author_name'] = author.get('username', 'Unknown')
                        formatted_post['author_id'] = str(user_id)
                        # Include author profile image if available
                        formatted_post['author_image'] = author.get('profile_image')
                    else:
                        formatted_post['author_name'] = 'User not found'
                        formatted_post['author_id'] = str(user_id)
                        formatted_post['author_image'] = None
                else:
                    formatted_post['author_name'] = 'No author specified'
                    formatted_post['author_id'] = None
                    formatted_post['author_image'] = None
            except Exception as e:
                print(f"Error fetching author information: {str(e)}")
                formatted_post['author_name'] = 'Error fetching user'
                formatted_post['author_id'] = None
                formatted_post['author_image'] = None
            
            # Format date if it exists
            if formatted_post['created_at']:
                try:
                    formatted_post['created_at'] = formatted_post['created_at'].isoformat()
                except:
                    formatted_post['created_at'] = None
            
            formatted_results.append(formatted_post)
            
        return jsonify({
            'success': True,
            'results': formatted_results
        })
        
    except Exception as e:
        print(f"Error formatting search results: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing search results'
        }), 500