import pytest
from app.services.transaction_service import TransactionService
from app.models.transaction import Transaction
from datetime import datetime

class TestTransactionService:
    
    def test_get_transactions_by_statement(self, session, sample_transaction):
        result = TransactionService.get_transactions_by_statement(
            sample_transaction.statement_id
        )
        assert result is not None
        assert len(result) > 0
    
    def test_get_transaction_by_id(self, session, sample_transaction):
        result = TransactionService.get_transaction_by_id(
            sample_transaction.transaction_id
        )
        assert result is not None
        assert result['description'] == sample_transaction.description
    
    def test_get_transactions_by_date_range(self, session, sample_transaction):
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 31)
        result = TransactionService.get_transactions_by_date_range(
            sample_transaction.profile_id, start_date, end_date
        )
        assert result is not None
    
    def test_get_debit_transactions(self, session, sample_transaction):
        result = TransactionService.get_debit_transactions(
            sample_transaction.profile_id
        )
        assert result is not None
        assert all(txn['debit_amount'] > 0 for txn in result)
    
    def test_get_credit_transactions(self, session, sample_user):
        result = TransactionService.get_credit_transactions(
            sample_user.profile_id
        )
        assert result is not None
