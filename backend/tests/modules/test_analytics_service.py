import pytest
from app.services.analytics_service import AnalyticsService
from datetime import datetime

class TestAnalyticsService:
    
    def test_get_spending_forecast(self, session, sample_transaction):
        result = AnalyticsService.get_spending_forecast(
            sample_transaction.profile_id,
            target_month='2024-02',
            categories=['Shopping']
        )
        assert result is not None
    
    def test_calculate_savings_potential(self, session, sample_transaction):
        result = AnalyticsService.calculate_savings_potential(
            sample_transaction.profile_id,
            category='Shopping',
            budget_limit=300.00
        )
        assert result is not None
        assert 'current_spending' in result
        assert 'savings' in result
    
    def test_get_category_trends(self, session, sample_transaction):
        result = AnalyticsService.get_category_trends(
            sample_transaction.profile_id,
            category='Shopping',
            months=3
        )
        assert result is not None
    
    def test_predict_next_month_spending(self, session, sample_transaction):
        result = AnalyticsService.predict_next_month_spending(
            sample_transaction.profile_id
        )
        assert result is not None
