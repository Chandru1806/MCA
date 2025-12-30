import pytest
from datetime import datetime
from app.models.user import User
from app.models.bank_statement import BankStatement
from app.models.transaction import Transaction
from app.models.transaction_category import TransactionCategory
from app.models.budget import Budget

class TestUserModel:
    
    def test_user_creation(self, session):
        user = User(
            first_name='FirstName',
            last_name='LastName',
            username=f'user_{id(session)}',
            email=f'user_{id(session)}@test.com',
            password_hash='hashed',
            is_active='A'
        )
        session.add(user)
        session.commit()
        assert user.profile_id is not None
    
    def test_user_to_dict(self, sample_user):
        data = sample_user.to_dict()
        assert data['username'] == sample_user.username
        assert 'password_hash' not in data

class TestBankStatementModel:
    
    def test_statement_creation(self, session, sample_user):
        statement = BankStatement(
            profile_id=sample_user.profile_id,
            bank_name='SBI',
            statement_period='2024-01',
            upload_date=datetime.utcnow(),
            file_path=f'/test_{id(session)}.pdf',
            status='PROCESSED'
        )
        session.add(statement)
        session.commit()
        assert statement.statement_id is not None

class TestTransactionModel:
    
    def test_transaction_creation(self, session, sample_user, sample_statement):
        txn = Transaction(
            profile_id=sample_user.profile_id,
            statement_id=sample_statement.statement_id,
            transaction_date=datetime.utcnow(),
            description='PAYMENT TRANSACTION',
            debit_amount=100.0,
            credit_amount=0.0,
            balance=1000.0
        )
        session.add(txn)
        session.commit()
        assert txn.transaction_id is not None

class TestTransactionCategoryModel:
    
    def test_category_creation(self, session, sample_user, sample_transaction):
        category = TransactionCategory(
            profile_id=sample_user.profile_id,
            transaction_id=sample_transaction.transaction_id,
            category_name='Shopping',
            confidence_score=0.95,
            classification_method='RULE_BASED'
        )
        session.add(category)
        session.commit()
        assert category.category_id is not None

class TestBudgetModel:
    
    def test_budget_creation(self, session, sample_user):
        budget = Budget(
            profile_id=sample_user.profile_id,
            category='Shopping',
            budget_limit=5000.00,
            month='2024-02'
        )
        session.add(budget)
        session.commit()
        assert budget.budget_id is not None
