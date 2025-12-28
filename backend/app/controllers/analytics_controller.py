from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.analytics_service import AnalyticsService
from datetime import datetime

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/forecast', methods=['POST'])
@jwt_required()
def forecast_savings():
    """Generate savings forecast for selected categories"""
    try:
        profile_id = get_jwt_identity()
        data = request.get_json()
        
        budget_limit = data.get('budget_limit')
        target_month = data.get('target_month')
        categories = data.get('categories', [])
        
        if not budget_limit or budget_limit <= 0:
            return jsonify({
                'success': False,
                'error': 'Budget limit must be greater than 0'
            }), 400
        
        if not target_month:
            return jsonify({
                'success': False,
                'error': 'Target month is required'
            }), 400
        
        try:
            datetime.strptime(target_month, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }), 400
        
        if not categories or len(categories) == 0:
            return jsonify({
                'success': False,
                'error': 'At least one category must be selected'
            }), 400
        
        results = AnalyticsService.generate_forecast(
            profile_id, budget_limit, target_month, categories
        )
        
        save_budget = data.get('save_budget', False)
        if save_budget:
            AnalyticsService.save_budgets(
                profile_id, budget_limit, target_month, categories
            )
        
        return jsonify({
            'success': True,
            'data': results,
            'budget_saved': save_budget
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
