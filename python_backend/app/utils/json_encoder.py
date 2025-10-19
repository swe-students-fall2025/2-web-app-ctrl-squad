from bson import ObjectId
from datetime import datetime

class MongoJSONEncoder:
    @staticmethod
    def encode_document(document):
        """Convert MongoDB document to JSON serializable format"""
        if document is None:
            return None
        
        if isinstance(document, list):
            return [MongoJSONEncoder.encode_document(item) for item in document]
        
        if isinstance(document, dict):
            result = {}
            for key, value in document.items():
                result[key] = MongoJSONEncoder.encode_document(value)
            return result
        
        if isinstance(document, ObjectId):
            return str(document)
        
        if isinstance(document, datetime):
            return document.isoformat()
        
        return document