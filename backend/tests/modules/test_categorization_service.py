import pytest
from app.services.categorization_service import CategorizationService
from app.models.transaction_category import TransactionCategory

class TestCategorizationService:
    
    def test_categorize_transactions(self, session, sample_transaction):
        service = CategorizationService()
        count = service.categorize_transactions(sample_transaction.statement_id)
        assert count > 0
    
    def test_categorize_already_categorized(self, session, sample_transaction):
        service = CategorizationService()
        service.categorize_transactions(sample_transaction.statement_id)
        
        with pytest.raises(ValueError, match="already categorized"):
            service.categorize_transactions(sample_transaction.statement_id)
    
    def test_categorize_no_transactions(self, session):
        service = CategorizationService()
        with pytest.raises(ValueError, match="No transactions found"):
            service.categorize_transactions(99999)
    
    def test_food_category_detection(self, session):
        service = CategorizationService()
        category, confidence = service.classifier.predict('RESTAURANT PAYMENT')
        assert category in ['Food', 'Shopping', 'Travel']
        assert confidence > 0.0
    
    def test_travel_category_detection(self, session):
        service = CategorizationService()
        category, confidence = service.classifier.predict('CAB BOOKING')
        assert category in ['Travel', 'Food', 'Shopping']
        assert confidence > 0.0
