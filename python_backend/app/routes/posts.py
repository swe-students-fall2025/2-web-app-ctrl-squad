from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.post import Post

bp = Blueprint('posts', __name__)

@bp.route('/posts', methods=['GET'])
def get_posts():
    try:
        # Parse and validate query params
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 20))
        except ValueError:
            return jsonify({"error": "page and limit must be integers"}), 400

      # call model
        posts, total = Post.get_all_posts(page=page, limit=limit)

        return jsonify({
            "posts": posts,
            "page": max(1, page),
            "limit": max(1, min(limit, 100)),
            "total": total
        }), 200
    except Exception as e:
        print(f"Error getting posts: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route('/posts', methods=['POST'])
@login_required
def create_post():
    print("Creating new post...")
    data = request.get_json()
    print("Received data:", data)
    
    if not all(k in data for k in ('title', 'description')):
        print("Missing required fields")
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    try:
        print(f"Creating post for user: {current_user.id}")
        post = Post.create_post(
            user_id=current_user.id,
            title=data['title'],
            description=data['description'],
            type=data.get('type', 'item'),
            category=data.get('category'),
            condition=data.get('condition'),
            images=data.get('images'),
            price=data.get('price'),
            status=data.get('status', 'Available')
        )
        print("Post created successfully:", post)
        
        response_data = {
            'success': True,
            'post': post,
            'message': 'Post created successfully'
        }
        print("Sending response:", response_data)
        return jsonify(response_data), 201
    except Exception as e:
        print(f"Error creating post: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    return jsonify(post), 200

@bp.route('/users/profile/posts', methods=['GET'])
@login_required
def get_user_posts():
    try:
        if not current_user.is_authenticated:
            return jsonify({'error': 'User not authenticated'}), 401

        if not current_user.id:
            return jsonify({'error': 'Invalid user session'}), 401

        print(f"Fetching posts for user: {current_user.id}")
        # Get posts for the current logged-in user
        posts = Post.get_posts_by_user(current_user.id)
        return jsonify({
            "success": True,
            "posts": posts
        }), 200
    except Exception as e:
        print(f"Error getting user posts: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@bp.route('/posts/<post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    try:
        # First get the post to verify ownership
        post = Post.get_by_id(post_id)
        if not post:
            return jsonify({
                'success': False,
                'error': 'Post not found'
            }), 404

        # Verify that the current user owns this post
        if str(post['user_id']) != current_user.id:
            return jsonify({
                'success': False,
                'error': 'Not authorized to delete this post'
            }), 403

        # Delete the post
        if Post.delete_post(post_id):
            return jsonify({
                'success': True,
                'message': 'Post deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete post'
            }), 500
    except Exception as e:
        print(f"Error deleting post: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/posts/<post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    try:
        post = Post.get_by_id(post_id)
        if not post:
            return jsonify({
                'success': False,
                'error': 'Post not found'
            }), 404
        
        if str(post['user_id']) != current_user.id:
            return jsonify({
                'success': False,
                'error': 'Not authorized to edit this post'
            }), 403
        
        data = request.get_json()
        success = Post.update_post(
            post_id=post_id,
            title=data.get('title'),
            description=data.get('description'),
            images=data.get('images'),
            price=data.get('price')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Post updated successfully'
            }), 200
        return jsonify({
            'success': False,
            'error': 'Failed to update post'
        }), 500
    except Exception as e:
        print(f"Error updating post: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/users/<user_id>/posts', methods=['GET'])
def get_posts_by_user_id(user_id):
    try:
        posts = Post.get_posts_by_user(user_id)
        return jsonify({
            'success': True,
            'posts': posts
        }), 200
    except Exception as e:
        print(f"Error getting user posts: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500