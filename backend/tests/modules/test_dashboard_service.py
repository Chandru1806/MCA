import pytest
from app.services.dashboard_service import DashboardService
from app.models.transaction_category import TransactionCategory

class TestDashboardService:
    
    def test_get_category_summary(self, session, sample_transaction):
        # First categorize
        from app.services.categorization_service import CategorizationService
        service = CategorizationService()
        service.categorize_transactions(sample_transaction.statement_id)
        
        # Get summary
        result = DashboardService.get_category_summary(sample_transaction.profile_id)
        assert result is not None
        assert len(result) > 0
    
    def test_get_spending_trends(self, session, sample_transaction):
        result = DashboardService.get_spending_trends(
            sample_transaction.profile_id, period='monthly'
        )
        assert result is not None
    
    def test_get_top_merchants(self, session, sample_transaction):
        result = DashboardService.get_top_merchants(
            sample_transaction.profile_id, limit=5
        )
        assert result is not None
    
    def test_get_total_spending(self, session, sample_transaction):
        result = DashboardService.get_total_spending(sample_transaction.profile_id)
        assert result is not None
        assert 'total_debit' in result
        assert 'total_credit' in result
