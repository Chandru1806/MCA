from flask import Blueprint, jsonify
from app.services.transaction_service import TransactionService
from app.models.transaction import Transaction
from flask_jwt_extended import jwt_required

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('/import/<int:statement_id>', methods=['POST'])
@jwt_required()
def import_transactions(statement_id):
    """Import transactions from CSV to database"""
    try:
        count = TransactionService.import_from_csv(statement_id)
        return jsonify({
            'success': True,
            'message': f'{count} transactions imported successfully',
            'count': count
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Internal error: {str(e)}'}), 500

@transaction_bp.route('/<int:statement_id>', methods=['GET'])
@jwt_required()
def get_transactions(statement_id):
    """Get all transactions for a statement"""
    try:
        transactions = Transaction.query.filter_by(statement_id=statement_id).all()
        
        return jsonify({
            'success': True,
            'count': len(transactions),
            'transactions': [{
                'transaction_id': t.transaction_id,
                'date': str(t.transaction_date),
                'description': t.description,
                'debit': float(t.debit_amount) if t.debit_amount else None,
                'credit': float(t.credit_amount) if t.credit_amount else None,
                'balance': float(t.balance) if t.balance else None,
                'merchant': t.merchant_name,
                'is_repaired': t.is_repaired
            } for t in transactions]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
