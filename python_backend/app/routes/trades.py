from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.trade import Trade

bp = Blueprint('trades', __name__)

@bp.route('/trades', methods=['GET'])
def get_trades():
    trades = Trade.get_all_trades()
    return jsonify(trades), 200

@bp.route('/trades', methods=['POST'])
@login_required
def create_trade():
    data = request.get_json()
    
    if not all(k in data for k in ('item_name', 'description')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    trade = Trade.create_trade(
        user_id=current_user.id,
        item_name=data['item_name'],
        description=data['description'],
        images=data.get('images'),
        trade_preferences=data.get('trade_preferences')
    )
    
    return jsonify(trade), 201

@bp.route('/trades/<trade_id>', methods=['GET'])
def get_trade(trade_id):
    trade = Trade.get_by_id(trade_id)
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    return jsonify(trade), 200

@bp.route('/trades/<trade_id>', methods=['PUT'])
@login_required
def update_trade(trade_id):
    trade = Trade.get_by_id(trade_id)
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    if str(trade['user_id']) != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
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
@login_required
def delete_trade(trade_id):
    trade = Trade.get_by_id(trade_id)
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    if str(trade['user_id']) != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if Trade.delete_trade(trade_id):
        return jsonify({'message': 'Trade deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete trade'}), 500

@bp.route('/trades/<trade_id>/interest', methods=['POST'])
@login_required
def express_interest(trade_id):
    trade = Trade.get_by_id(trade_id)
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    if str(trade['user_id']) == current_user.id:
        return jsonify({'error': 'Cannot express interest in your own trade'}), 400
    
    if Trade.express_interest(trade_id, current_user.id):
        return jsonify({'message': 'Interest expressed successfully'}), 200
    return jsonify({'error': 'Failed to express interest'}), 500

@bp.route('/trades/<trade_id>/interest', methods=['DELETE'])
@login_required
def remove_interest(trade_id):
    trade = Trade.get_by_id(trade_id)
    if not trade:
        return jsonify({'error': 'Trade not found'}), 404
    
    if Trade.remove_interest(trade_id, current_user.id):
        return jsonify({'message': 'Interest removed successfully'}), 200
    return jsonify({'error': 'Failed to remove interest'}), 500

@bp.route('/users/<user_id>/trades', methods=['GET'])
def get_user_trades(user_id):
    trades = Trade.get_user_trades(user_id)
    return jsonify(trades), 200