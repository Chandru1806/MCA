from flask import Blueprint, jsonify
from app.services.categorization_service import CategorizationService
from app.models.transaction_category import TransactionCategory
from app.models.transaction import Transaction
from app import db
from flask_jwt_extended import jwt_required

categorization_bp = Blueprint('categorization', __name__)

@categorization_bp.route('/categorize/<int:statement_id>', methods=['POST'])
@jwt_required()
def categorize_statement(statement_id):
    """Categorize all transactions for a statement"""
    try:
        service = CategorizationService()
        count = service.categorize_transactions(statement_id)
        
        return jsonify({
            'success': True,
            'message': f'{count} transactions categorized successfully',
            'count': count
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Internal error: {str(e)}'}), 500

@categorization_bp.route('/categories/<int:statement_id>', methods=['GET'])
@jwt_required()
def get_categories(statement_id):
    """Get categorized transactions"""
    try:
        categories = db.session.query(
            TransactionCategory, Transaction
        ).join(
            Transaction, TransactionCategory.transaction_id == Transaction.transaction_id
        ).filter(
            Transaction.statement_id == statement_id
        ).all()
        
        return jsonify({
            'success': True,
            'count': len(categories),
            'data': [{
                'transaction_id': t.transaction_id,
                'date': str(t.transaction_date),
                'description': t.description,
                'merchant': t.merchant_name,
                'category': c.category_name,
                'confidence': float(c.confidence_score),
                'method': c.classification_method,
                'rule_prediction': c.rule_based_prediction,
                'ml_prediction': c.ml_prediction,
                'debit': float(t.debit_amount) if t.debit_amount else None,
                'credit': float(t.credit_amount) if t.credit_amount else None
            } for c, t in categories]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
