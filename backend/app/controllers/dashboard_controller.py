from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.dashboard_service import DashboardService
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/spending', methods=['GET'])
@jwt_required()
def get_category_spending():
    """Get category-wise spending totals"""
    try:
        profile_id = get_jwt_identity()
        data = DashboardService.get_category_spending(profile_id)
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/trends', methods=['GET'])
@jwt_required()
def get_spending_trends():
    """Get monthly spending trends by category"""
    try:
        profile_id = get_jwt_identity()
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        data = DashboardService.get_spending_trends(profile_id, start_date, end_date)
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid date format. Use YYYY-MM-DD'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
