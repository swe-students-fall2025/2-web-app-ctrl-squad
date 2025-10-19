from flask import Blueprint, request, jsonify, session
from app.models.trade import Trade
from app.utils.json_encoder import MongoJSONEncoder
from app.utils.header_auth import header_auth_required

bp = Blueprint('trades', __name__)

@bp.route('/trades', methods=['GET'])
def get_trades():
    trades = Trade.get_all_trades()
    # Convert MongoDB documents to JSON serializable format
    serialized_trades = MongoJSONEncoder.encode_document(trades)
    return jsonify(serialized_trades), 200

@bp.route('/trades', methods=['POST'])
def create_trade():
    # Debug information
    print("***** TRADE REQUEST RECEIVED *****")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request data: {request.get_json()}")
    print(f"Session: {session if 'session' in globals() else 'Session not available'}")
    
    # Get the user ID from the X-User-ID header
    user_id = request.headers.get('X-User-ID')
    if not user_id or user_id == 'undefined' or user_id == 'null' or not user_id.strip():
        print("Missing or invalid X-User-ID header")
        return jsonify({'error': 'Valid X-User-ID header is required'}), 400
    
    print(f"Using user ID: {user_id}")
    
    # Process the request
    try:
        data = request.get_json()
        
        if not all(k in data for k in ('item_name', 'description')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create the trade directly without further checks
        trade = Trade.create_trade(
            user_id=user_id,
            item_name=data['item_name'],
            description=data['description'],
            images=data.get('images'),
            trade_preferences=data.get('trade_preferences')
        )
        
        print("Trade created successfully:", trade)
        
        # Convert MongoDB document to JSON serializable format
        serialized_trade = MongoJSONEncoder.encode_document(trade)
        
        # Return success with the trade data
        response = jsonify({
            'success': True,
            'message': 'Trade request created successfully',
            'trade': serialized_trade,
            'trade_id': str(trade.get('_id'))
        })
        
        return response, 201
        
    except Exception as e:
        print(f"Error creating trade: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/trades/<trade_id>', methods=['GET'])
def get_trade(trade_id):
    trade = Trade.get_by_id(trade_id)
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    # Convert MongoDB document to JSON serializable format
    serialized_trade = MongoJSONEncoder.encode_document(trade)
    
    return jsonify(serialized_trade), 200

@bp.route('/trades/user/<user_id>', methods=['GET'])
def get_user_trades(user_id):
    trades = Trade.get_user_trades(user_id)
    # Convert MongoDB documents to JSON serializable format
    serialized_trades = MongoJSONEncoder.encode_document(trades)
    return jsonify(serialized_trades), 200

@bp.route('/trades/<trade_id>', methods=['PUT'])
def update_trade(trade_id):
    trade = Trade.get_by_id(trade_id)
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    # Get user ID from X-User-ID header
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({'error': 'X-User-ID header is required'}), 400
    
    # Check if the current user is either the trade owner or the buyer
    data = request.get_json()
    trade_preferences = trade.get('trade_preferences', {})
    buyer_id = trade_preferences.get('buyer_id')
    
    if (str(trade['user_id']) != user_id and 
        (not buyer_id or str(buyer_id) != user_id)):
        return jsonify({'error': 'Unauthorized'}), 403
    
    success = Trade.update_trade(
        trade_id=trade_id,
        item_name=data.get('item_name'),
        description=data.get('description'),
        images=data.get('images'),
        trade_preferences=data.get('trade_preferences'),
        status=data.get('status')
    )
    
    if success:
        return jsonify({'message': 'Trade updated successfully'}), 200
    return jsonify({'error': 'Failed to update trade'}), 500

@bp.route('/trades/<trade_id>', methods=['DELETE'])
def delete_trade(trade_id):
    trade = Trade.get_by_id(trade_id)
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    # Get user ID from X-User-ID header
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({'error': 'X-User-ID header is required'}), 400
    
    if str(trade['user_id']) != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if Trade.delete_trade(trade_id):
        return jsonify({'message': 'Trade deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete trade'}), 500

@bp.route('/trades/<trade_id>/interest', methods=['POST'])
def express_interest(trade_id):
    trade = Trade.get_by_id(trade_id)
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    # Get user ID from X-User-ID header
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({'error': 'X-User-ID header is required'}), 400
    
    if str(trade['user_id']) == user_id:
        return jsonify({'error': 'Cannot express interest in your own trade'}), 400
    
    if Trade.express_interest(trade_id, user_id):
        return jsonify({'message': 'Interest expressed successfully'}), 200
    return jsonify({'error': 'Failed to express interest'}), 500

@bp.route('/trades/<trade_id>/interest', methods=['DELETE'])
def remove_interest(trade_id):
    trade = Trade.get_by_id(trade_id)
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    # Get user ID from X-User-ID header
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return jsonify({'error': 'X-User-ID header is required'}), 400
    
    if Trade.remove_interest(trade_id, user_id):
        return jsonify({'message': 'Interest removed successfully'}), 200
    return jsonify({'error': 'Failed to remove interest'}), 500

@bp.route('/users/<user_id>/trades', methods=['GET'])
def get_trades_by_user(user_id):
    trades = Trade.get_user_trades(user_id)
    # Convert MongoDB documents to JSON serializable format
    serialized_trades = MongoJSONEncoder.encode_document(trades)
    return jsonify(serialized_trades), 200