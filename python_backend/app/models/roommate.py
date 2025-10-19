from datetime import datetime
import json
from bson.objectid import ObjectId
from app import db

# --- JSON helpers so ObjectId/datetime serialize cleanly ---
class _JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

def _dump(o):
    return json.loads(json.dumps(o, cls=_JSONEncoder))

class Roommate:
    collection = db.roommates

    @staticmethod
    def create_roommate_post(user_id, title, description, type='roommate', preferences=None, location=None, images=None, username=None, year=None
    ):

        roommate_data = {
            "user_id": ObjectId(user_id),
            "title": title,
            "description": description,
            "type": type,
            "preferences": preferences or [],
            "location": location,
            "images": images or [],
            "username": (username or ""),
            "year": (year or ""),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        # insert and verify what actually got saved
        result = Roommate.collection.insert_one(roommate_data)
        saved = Roommate.collection.find_one(
            {"_id": result.inserted_id},
            {"username": 1, "year": 1}
        )

        roommate_data["_id"] = result.inserted_id
        return _dump(roommate_data)


    @staticmethod
    def get_by_id(roommate_id):
        doc = Roommate.collection.find_one({"_id": ObjectId(roommate_id)})
        return _dump(doc) if doc else None

    @staticmethod
    def get_all_roommate_posts():
        """Backward-compatible: return ALL posts (no pagination)."""
        docs = list(Roommate.collection.find().sort("created_at", -1))
        return _dump(docs)

    # NEW: paginated list
    @staticmethod
    def get_all_roommate_posts_paginated(page: int = 1, limit: int = 20):
        query = {}
        total = Roommate.collection.count_documents(query)
        page = max(1, int(page))
        limit = max(1, min(int(limit), 100))
        skip = (page - 1) * limit
        cursor = (
            Roommate.collection.find(query)
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )
        docs = list(cursor)
        return _dump(docs), total

    @staticmethod
    def get_user_roommate_posts(user_id):
        docs = list(Roommate.collection.find({"user_id": ObjectId(user_id)}).sort("created_at", -1))
        return _dump(docs)

    @staticmethod
    def update_roommate_post(roommate_id, title=None, description=None, preferences=None, location=None):
        update_data = {"updated_at": datetime.utcnow()}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if preferences is not None:
            update_data["preferences"] = preferences
        if location is not None:
            update_data["location"] = location

        res = Roommate.collection.update_one({"_id": ObjectId(roommate_id)}, {"$set": update_data})
        return res.modified_count > 0

    @staticmethod
    def delete_roommate_post(roommate_id):
        res = Roommate.collection.delete_one({"_id": ObjectId(roommate_id)})
        return res.deleted_count > 0