from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.roommate import Roommate
from bson import ObjectId

bp = Blueprint('roommates', __name__)

def _error(msg, code=400):
    return jsonify({"success": False, "error": msg}), code

def _present_roommate(doc):
    if not doc:
        return None
    return {
        "id": str(doc.get("_id")) if doc.get("_id") is not None else None,
        "user_id": str(doc.get("user_id")) if doc.get("user_id") is not None else None,
        "title": doc.get("title", ""),
        "description": doc.get("description", ""),
        "preferences": doc.get("preferences", []),
        "location": doc.get("location", ""),
        "images": doc.get("images", []),
        "created_at": doc.get("created_at"),
        "updated_at": doc.get("updated_at"),
        "type": doc.get("type", "roommate"),
    }

# ---------------------------
# OPTIONS (no auth, for CORS preflight)
# ---------------------------
@bp.route("/roommates", methods=["OPTIONS"])
def roommates_collection_options():
    return ("", 200)

@bp.route("/roommates/<post_id>", methods=["OPTIONS"])
def roommates_item_options(post_id):
    return ("", 200)

@bp.route("/users/<user_id>/roommates", methods=["OPTIONS"])
def roommates_user_options(user_id):
    return ("", 200)


# GET /api/roommates?page=&limit=
@bp.route("/roommates", methods=["GET"])
def get_roommate_posts():
    try:
        page = request.args.get('page')
        limit = request.args.get('limit')

        if page or limit:
            try:
                page = int(page or 1)
                limit = int(limit or 20)
            except ValueError:
                return _error("page and limit must be integers", 400)

            docs, total = Roommate.get_all_roommate_posts_paginated(page=page, limit=limit)
            docs = [_present_roommate(d) for d in docs]
            return jsonify({
                "success": True,
                "roommates": docs,
                "page": max(1, page),
                "limit": max(1, min(limit, 100)),
                "total": total
            }), 200

        posts = Roommate.get_all_roommate_posts()
        posts = [_present_roommate(p) for p in posts]
        return jsonify({"success": True, "roommates": posts}), 200

    except Exception as e:
        print(f"[roommates.get] error: {e}")
        return _error(str(e), 500)

# POST /api/roommates
@bp.route("/roommates", methods=["POST"])
@login_required
def create_roommate_post():
    try:
        print("Creating new roommate post...")
        data = request.get_json(silent=True) or {}
        print("Received data:", data)

        title = (data.get("title") or "").strip()
        description = (data.get("description") or "").strip()
        if not title or not description:
            return _error("Missing required fields: 'title' and 'description'", 400)

        preferences = data.get("preferences")
        location = (data.get("location") or "").strip()
        images = data.get("images")

        if isinstance(preferences, str):
            preferences = [p.strip() for p in preferences.split(",") if p.strip()]
        if preferences is not None and not isinstance(preferences, list):
            return _error("'preferences' must be a list of strings or a comma-separated string.", 400)

        if images is not None and not isinstance(images, list):
            return _error("'images' must be a list of base64 strings or URLs.", 400)

        uid = current_user.id
        if not isinstance(uid, ObjectId):
            try:
                uid = ObjectId(uid)
            except Exception:
                return _error("Invalid user id.", 500)

        post = Roommate.create_roommate_post(
            user_id=uid,
            title=title,
            description=description,
            preferences=preferences,
            location=location,
            images=images,
        )

        if post and isinstance(post, dict) and post.get("_id"):
            presented = post 
        else:
            inserted_id = getattr(post, "inserted_id", None)
            if inserted_id:
                presented = Roommate.get_by_id(str(inserted_id))
            else:
                presented = {
                    "title": title,
                    "description": description,
                    "preferences": preferences or [],
                    "location": location,
                    "images": images or []
                }

        print("Roommate post created:", presented)
        return jsonify({
            "success": True,
            "post": _present_roommate(presented),
            "message": "Roommate post created successfully"
        }), 201

    except Exception as e:
        print(f"[roommates.create] error: {e}")
        return _error(str(e), 500)

# GET /api/roommates/<id>
@bp.route("/roommates/<post_id>", methods=["GET"])
def get_roommate_post(post_id):
    try:
        post = Roommate.get_by_id(post_id)
        if not post:
            return _error("Roommate post not found", 404)
        return jsonify({"success": True, "post": _present_roommate(post)}), 200
    except Exception as e:
        print(f"[roommates.get_one] error: {e}")
        return _error(str(e), 500)

# PUT /api/roommates/<id>
@bp.route("/roommates/<post_id>", methods=["PUT"])
@login_required
def update_roommate_post(post_id):
    try:
        existing = Roommate.get_by_id(post_id)
        if not existing:
            return _error("Roommate post not found", 404)
        if str(existing["user_id"]) != current_user.id:
            return _error("Not authorized to edit this post", 403)

        data = request.get_json(silent=True) or {}
        success = Roommate.update_roommate_post(
            roommate_id=post_id,
            title=data.get("title"),
            description=data.get("description"),
            preferences=data.get("preferences"),
            location=data.get("location"),
            images=data.get("images")
        )

        if success:
            return jsonify({"success": True, "message": "Roommate post updated successfully"}), 200
        return _error("Failed to update roommate post", 500)

    except Exception as e:
        print(f"[roommates.update] error: {e}")
        return _error(str(e), 500)

# DELETE /api/roommates/<id>
@bp.route("/roommates/<post_id>", methods=["DELETE"])
@login_required
def delete_roommate_post(post_id):
    try:
        existing = Roommate.get_by_id(post_id)
        if not existing:
            return _error("Roommate post not found", 404)
        if str(existing["user_id"]) != current_user.id:
            return _error("Not authorized to delete this post", 403)

        if Roommate.delete_roommate_post(post_id):
            return jsonify({"success": True, "message": "Roommate post deleted successfully"}), 200
        return _error("Failed to delete roommate post", 500)

    except Exception as e:
        print(f"[roommates.delete] error: {e}")
        return _error(str(e), 500)

# GET /api/users/<user_id>/roommates
@bp.route("/users/<user_id>/roommates", methods=["GET"])
def get_user_roommate_posts(user_id):
    try:
        posts = Roommate.get_user_roommate_posts(user_id)
        posts = [_present_roommate(p) for p in posts]
        return jsonify({"success": True, "roommates": posts}), 200
    except Exception as e:
        print(f"[roommates.user_list] error: {e}")
        return _error(str(e), 500)