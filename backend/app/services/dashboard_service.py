from sqlalchemy import func, extract
from app import db
from app.models.transaction import Transaction
from app.models.transaction_category import TransactionCategory

class DashboardService:
    
    @staticmethod
    def get_category_spending(profile_id):
        """Aggregate spending by category for a user"""
        results = db.session.query(
            TransactionCategory.category_name,
            func.sum(Transaction.debit_amount).label('total_amount'),
            func.count(Transaction.transaction_id).label('transaction_count')
        ).join(
            Transaction, 
            TransactionCategory.transaction_id == Transaction.transaction_id
        ).filter(
            Transaction.profile_id == profile_id,
            Transaction.debit_amount.isnot(None)
        ).group_by(
            TransactionCategory.category_name
        ).order_by(
            func.sum(Transaction.debit_amount).desc()
        ).all()
        
        return [{
            'category': r.category_name,
            'total_amount': float(r.total_amount),
            'transaction_count': r.transaction_count
        } for r in results]
    
    @staticmethod
    def get_spending_trends(profile_id, start_date=None, end_date=None):
        """Get monthly spending trends by category"""
        query = db.session.query(
            extract('year', Transaction.transaction_date).label('year'),
            extract('month', Transaction.transaction_date).label('month'),
            TransactionCategory.category_name,
            func.sum(Transaction.debit_amount).label('amount')
        ).join(
            TransactionCategory,
            Transaction.transaction_id == TransactionCategory.transaction_id
        ).filter(
            Transaction.profile_id == profile_id,
            Transaction.debit_amount.isnot(None)
        )
        
        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)
        
        results = query.group_by(
            extract('year', Transaction.transaction_date),
            extract('month', Transaction.transaction_date),
            TransactionCategory.category_name
        ).order_by(
            extract('year', Transaction.transaction_date),
            extract('month', Transaction.transaction_date)
        ).all()
        
        return [{
            'year': int(r.year),
            'month': int(r.month),
            'category': r.category_name,
            'amount': float(r.amount)
        } for r in results]
