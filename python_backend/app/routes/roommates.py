from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.roommate import Roommate

bp = Blueprint('roommates', __name__)

@bp.route('/roommates', methods=['GET'])
def get_roommate_posts():
    posts = Roommate.get_all_roommate_posts()
    return jsonify(posts), 200

@bp.route('/roommates', methods=['POST'])
@login_required
def create_roommate_post():
    data = request.get_json()
    
    if not all(k in data for k in ('title', 'description')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    post = Roommate.create_roommate_post(
        user_id=current_user.id,
        title=data['title'],
        description=data['description'],
        preferences=data.get('preferences'),
        location=data.get('location')
    )
    
    return jsonify(post), 201

@bp.route('/roommates/<post_id>', methods=['GET'])
def get_roommate_post(post_id):
    post = Roommate.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Roommate post not found'}), 404
    
    return jsonify(post), 200

@bp.route('/roommates/<post_id>', methods=['PUT'])
@login_required
def update_roommate_post(post_id):
    post = Roommate.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Roommate post not found'}), 404
    
    if str(post['user_id']) != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    success = Roommate.update_roommate_post(
        roommate_id=post_id,
        title=data.get('title'),
        description=data.get('description'),
        preferences=data.get('preferences'),
        location=data.get('location')
    )
    
    if success:
        return jsonify({'message': 'Roommate post updated successfully'}), 200
    return jsonify({'error': 'Failed to update roommate post'}), 500

@bp.route('/roommates/<post_id>', methods=['DELETE'])
@login_required
def delete_roommate_post(post_id):
    post = Roommate.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Roommate post not found'}), 404
    
    if str(post['user_id']) != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if Roommate.delete_roommate_post(post_id):
        return jsonify({'message': 'Roommate post deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete roommate post'}), 500

@bp.route('/users/<user_id>/roommates', methods=['GET'])
def get_user_roommate_posts(user_id):
    posts = Roommate.get_user_roommate_posts(user_id)
    return jsonify(posts), 200