from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.budget_service import BudgetService

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_budgets():
    """Get all budgets for the logged-in user"""
    try:
        profile_id = get_jwt_identity()
        budgets = BudgetService.get_all_budgets(profile_id)
        
        return jsonify({
            'success': True,
            'data': budgets
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@budget_bp.route('/<category_name>', methods=['GET'])
@jwt_required()
def get_budget_by_category(category_name):
    """Get budget for specific category"""
    try:
        profile_id = get_jwt_identity()
        budget_month = request.args.get('budget_month')
        
        budget = BudgetService.get_budget_by_category(
            profile_id, category_name, budget_month
        )
        
        if not budget:
            return jsonify({
                'success': False,
                'error': 'Budget not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': budget
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@budget_bp.route('/<budget_id>', methods=['DELETE'])
@jwt_required()
def delete_budget(budget_id):
    """Delete a budget"""
    try:
        profile_id = get_jwt_identity()
        deleted = BudgetService.delete_budget(profile_id, budget_id)
        
        if not deleted:
            return jsonify({
                'success': False,
                'error': 'Budget not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Budget deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
