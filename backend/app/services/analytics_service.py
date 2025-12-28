from sqlalchemy import func, extract
from app import db
from app.models.transaction import Transaction
from app.models.transaction_category import TransactionCategory
from app.models.budget import Budget
from datetime import datetime

class AnalyticsService:
    
    @staticmethod
    def calculate_monthly_average_spending(profile_id, category_name):
        """Calculate historical average monthly spending for a category"""
        monthly_totals = db.session.query(
            extract('year', Transaction.transaction_date).label('year'),
            extract('month', Transaction.transaction_date).label('month'),
            func.sum(Transaction.debit_amount).label('monthly_total')
        ).join(
            TransactionCategory,
            Transaction.transaction_id == TransactionCategory.transaction_id
        ).filter(
            Transaction.profile_id == profile_id,
            TransactionCategory.category_name == category_name,
            Transaction.debit_amount.isnot(None)
        ).group_by(
            extract('year', Transaction.transaction_date),
            extract('month', Transaction.transaction_date)
        ).all()
        
        if not monthly_totals:
            return 0.0
        
        total_sum = sum(float(row.monthly_total) for row in monthly_totals)
        avg_monthly_spending = total_sum / len(monthly_totals)
        
        return round(avg_monthly_spending, 2)
    
    @staticmethod
    def generate_forecast(profile_id, budget_limit, target_month, categories):
        """Generate savings forecast for selected categories"""
        results = []
        
        for category in categories:
            current_spending = AnalyticsService.calculate_monthly_average_spending(
                profile_id, category
            )
            
            savings = current_spending - budget_limit
            
            message = (
                f"If you reduce spending in {category} to ₹{budget_limit:.2f}, "
                f"you'll save ₹{savings:.2f}"
            )
            
            results.append({
                'category': category,
                'current_spending': current_spending,
                'budget_limit': float(budget_limit),
                'savings': round(savings, 2),
                'message': message
            })
        
        return results
    
    @staticmethod
    def save_budgets(profile_id, budget_limit, target_month, categories):
        """Save or update budgets for selected categories"""
        budget_date = datetime.strptime(target_month, '%Y-%m-%d').date()
        
        for category in categories:
            existing_budget = Budget.query.filter_by(
                profile_id=profile_id,
                category_name=category,
                budget_month=budget_date
            ).first()
            
            if existing_budget:
                existing_budget.budget_limit = budget_limit
                existing_budget.updated_at = datetime.utcnow()
            else:
                new_budget = Budget(
                    profile_id=profile_id,
                    category_name=category,
                    budget_limit=budget_limit,
                    budget_month=budget_date
                )
                db.session.add(new_budget)
        
        db.session.commit()
        return len(categories)
