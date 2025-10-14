from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.post import Post

bp = Blueprint('posts', __name__)

@bp.route('/posts', methods=['GET'])
def get_posts():
    try:
        print("Attempting to get all posts...")
        posts = Post.get_all_posts()
        print(f"Successfully retrieved {len(posts) if posts else 0} posts")
        return jsonify({"posts": posts}), 200
    except Exception as e:
        print(f"Error getting posts: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/posts', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()
    
    if not all(k in data for k in ('title', 'description')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    post = Post.create_post(
        user_id=current_user.id,
        title=data['title'],
        description=data['description'],
        images=data.get('images'),
        price=data.get('price')
    )
    
    return jsonify(post), 201

@bp.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    return jsonify(post), 200

@bp.route('/posts/<post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    post = Post.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    if str(post['user_id']) != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    success = Post.update_post(
        post_id=post_id,
        title=data.get('title'),
        description=data.get('description'),
        images=data.get('images'),
        price=data.get('price')
    )
    
    if success:
        return jsonify({'message': 'Post updated successfully'}), 200
    return jsonify({'error': 'Failed to update post'}), 500

@bp.route('/posts/<post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = Post.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    if str(post['user_id']) != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if Post.delete_post(post_id):
        return jsonify({'message': 'Post deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete post'}), 500

@bp.route('/users/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    posts = Post.get_user_posts(user_id)
    return jsonify(posts), 200