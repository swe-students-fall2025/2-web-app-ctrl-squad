from flask import Blueprint, jsonify, request
from datetime import datetime
from database.db import get_db

search_bp = Blueprint('search', __name__)

@search_bp.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Search query is required'
        }), 400

    try:
        # Create a case-insensitive regex pattern
        db = get_db()
        
        # Search in title and description with case-insensitive regex
        posts = list(db.posts.find({
            '$or': [
                {'title': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}}
            ]
        }).sort('created_at', -1).limit(20))  # Sort by newest first, limit to 20 results
        
        # Get author information for each post
        for post in posts:
            post['_id'] = str(post['_id'])  # Convert ObjectId to string
            
            # Get author info if available
            if 'author_id' in post:
                author = db.users.find_one({'_id': post['author_id']})
                post['author_name'] = author['username'] if author else 'Anonymous'
            else:
                post['author_name'] = 'Anonymous'

            # Format date
            if 'created_at' in post:
                post['created_at'] = post['created_at'].isoformat()

            # Format favorites count
            post['favorites_count'] = len(post.get('favorites', []))

        return jsonify({
            'success': True,
            'results': posts
        })

    except Exception as e:
        print(f'Search error: {e}')
        return jsonify({
            'success': False,
            'error': 'Failed to perform search'
        }), 500