from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.roommate import Roommate

bp = Blueprint('roommates', __name__)

def _bad(msg): return jsonify({"error": msg}), 400

# GET /api/roommates?page=&limit=
@bp.route("/roommates", methods=["GET"])
def get_roommate_posts():
    # Optional pagination
    page = request.args.get("page")
    limit = request.args.get("limit")
    if page or limit:
        try:
            page = int(page or 1)
            limit = int(limit or 20)
        except ValueError:
            return _bad("page and limit must be integers")
        docs, total = Roommate.get_all_roommate_posts_paginated(page=page, limit=limit)
        return jsonify({"roommates": docs, "page": max(1, page), "limit": max(1, min(limit, 100)), "total": total}), 200

    # Backward-compatible: no pagination query → return all
    posts = Roommate.get_all_roommate_posts()
    return jsonify(posts), 200

# POST /api/roommates
@bp.route("/roommates", methods=["POST"])
@login_required
def create_roommate_post():
    # --- Handle CORS preflight without auth ---
    if request.method == 'OPTIONS':
        return ('', 200)
        
    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()
    preferences = data.get("preferences")
    location = data.get("location")
    images = data.get("images")

    if not title or not description:
        return _bad("Fields 'title' and 'description' are required.")
    if preferences is not None and not isinstance(preferences, list):
        return _bad("'preferences' must be a list of strings.")
    if images is not None and not isinstance(images, list):
        return _bad("'images' must be a list of base64 strings or URLs.")

    post = Roommate.create_roommate_post(
        user_id=current_user.id,
        title=title,
        description=description,
        preferences=preferences,
        location=location,
        images=images,
    )
    return jsonify(post), 201

# GET /api/roommates/<id>
@bp.route("/roommates/<post_id>", methods=["GET"])
def get_roommate_post(post_id):
    post = Roommate.get_by_id(post_id)
    if not post:
        return jsonify({"error": "Roommate post not found"}), 404
    return jsonify(post), 200

# PUT /api/roommates/<id>
@bp.route("/roommates/<post_id>", methods=["PUT"])
@login_required
def update_roommate_post(post_id):
    existing = Roommate.get_by_id(post_id)
    if not existing:
        return jsonify({"error": "Roommate post not found"}), 404
    if str(existing["user_id"]) != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json(silent=True) or {}
    success = Roommate.update_roommate_post(
        roommate_id=post_id,
        title=data.get("title"),
        description=data.get("description"),
        preferences=data.get("preferences"),
        location=data.get("location"),
    )
    if success:
        return jsonify({"message": "Roommate post updated successfully"}), 200
    return jsonify({"error": "Failed to update roommate post"}), 500

# DELETE /api/roommates/<id>
@bp.route("/roommates/<post_id>", methods=["DELETE"])
@login_required
def delete_roommate_post(post_id):
    existing = Roommate.get_by_id(post_id)
    if not existing:
        return jsonify({"error": "Roommate post not found"}), 404
    if str(existing["user_id"]) != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    if Roommate.delete_roommate_post(post_id):
        return jsonify({"message": "Roommate post deleted successfully"}), 200
    return jsonify({"error": "Failed to delete roommate post"}), 500

# GET /api/users/<user_id>/roommates
@bp.route("/users/<user_id>/roommates", methods=["GET"])
def get_user_roommate_posts(user_id):
    posts = Roommate.get_user_roommate_posts(user_id)
    return jsonify(posts), 200