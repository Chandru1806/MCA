import pytest
from app.services.budget_service import BudgetService
from app.models.budget import Budget

class TestBudgetService:
    
    def test_create_budget(self, session, sample_user):
        result = BudgetService.create_budget(
            profile_id=sample_user.profile_id,
            category='Shopping',
            budget_limit=5000.00,
            month='2024-02'
        )
        assert result is not None
        assert result['category'] == 'Shopping'
    
    def test_get_budgets_by_user(self, session, sample_user):
        BudgetService.create_budget(
            sample_user.profile_id, 'Shopping', 5000.00, '2024-02'
        )
        result = BudgetService.get_budgets_by_user(sample_user.profile_id)
        assert len(result) > 0
    
    def test_update_budget(self, session, sample_user):
        budget = BudgetService.create_budget(
            sample_user.profile_id, 'Shopping', 5000.00, '2024-02'
        )
        updated = BudgetService.update_budget(
            budget['budget_id'], {'budget_limit': 6000.00}
        )
        assert updated['budget_limit'] == 6000.00
    
    def test_delete_budget(self, session, sample_user):
        budget = BudgetService.create_budget(
            sample_user.profile_id, 'Shopping', 5000.00, '2024-02'
        )
        result = BudgetService.delete_budget(budget['budget_id'])
        assert result is not None
    
    def test_check_budget_exceeded(self, session, sample_user, sample_transaction):
        BudgetService.create_budget(
            sample_user.profile_id, 'Shopping', 100.00, '2024-01'
        )
        result = BudgetService.check_budget_status(
            sample_user.profile_id, '2024-01'
        )
        assert result is not None
