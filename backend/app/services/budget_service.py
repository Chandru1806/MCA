from app import db
from app.models.budget import Budget
from datetime import datetime

class BudgetService:
    
    @staticmethod
    def get_all_budgets(profile_id):
        """Get all budgets for a user"""
        budgets = Budget.query.filter_by(profile_id=profile_id).order_by(
            Budget.budget_month.desc()
        ).all()
        
        return [{
            'budget_id': b.budget_id,
            'category_name': b.category_name,
            'budget_limit': float(b.budget_limit),
            'budget_month': str(b.budget_month),
            'created_at': str(b.created_at),
            'updated_at': str(b.updated_at)
        } for b in budgets]
    
    @staticmethod
    def get_budget_by_category(profile_id, category_name, budget_month=None):
        """Get budget for specific category and month"""
        query = Budget.query.filter_by(
            profile_id=profile_id,
            category_name=category_name
        )
        
        if budget_month:
            budget_date = datetime.strptime(budget_month, '%Y-%m-%d').date()
            query = query.filter_by(budget_month=budget_date)
        
        budget = query.first()
        
        if not budget:
            return None
        
        return {
            'budget_id': budget.budget_id,
            'category_name': budget.category_name,
            'budget_limit': float(budget.budget_limit),
            'budget_month': str(budget.budget_month),
            'created_at': str(budget.created_at),
            'updated_at': str(budget.updated_at)
        }
    
    @staticmethod
    def delete_budget(profile_id, budget_id):
        """Delete a budget"""
        budget = Budget.query.filter_by(
            budget_id=budget_id,
            profile_id=profile_id
        ).first()
        
        if not budget:
            return False
        
        db.session.delete(budget)
        db.session.commit()
        return True
