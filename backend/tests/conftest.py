import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run import create_app, db
from app.models.user import User
from app.models.bank_statement import BankStatement
from app.models.transaction import Transaction
from app.models.transaction_category import TransactionCategory
from app.models.budget import Budget

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app

@pytest.fixture(scope='session')
def _db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

@pytest.fixture(scope='function')
def session(_db, app):
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()
        session = _db.session
        yield session
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_user(session, request):
    params = getattr(request, 'param', {})
    user = User(
        first_name=params.get('first_name', 'TestFirst'),
        last_name=params.get('last_name', 'TestLast'),
        username=params.get('username', f'user_{datetime.now().timestamp()}'),
        email=params.get('email', f'user_{datetime.now().timestamp()}@test.com'),
        password_hash=params.get('password_hash', '$2b$12$testhash'),
        is_active=params.get('is_active', 'A')
    )
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def sample_statement(session, sample_user, request):
    params = getattr(request, 'param', {})
    statement = BankStatement(
        profile_id=sample_user.profile_id,
        bank_name=params.get('bank_name', 'HDFC'),
        statement_period=params.get('statement_period', '2024-01'),
        upload_date=params.get('upload_date', datetime.utcnow()),
        file_path=params.get('file_path', f'/test/path_{datetime.now().timestamp()}.pdf'),
        status=params.get('status', 'PROCESSED')
    )
    session.add(statement)
    session.commit()
    return statement

@pytest.fixture
def sample_transaction(session, sample_user, sample_statement, request):
    params = getattr(request, 'param', {})
    txn = Transaction(
        profile_id=sample_user.profile_id,
        statement_id=sample_statement.statement_id,
        transaction_date=params.get('transaction_date', datetime(2024, 1, 15)),
        description=params.get('description', 'TEST PAYMENT'),
        debit_amount=params.get('debit_amount', 500.00),
        credit_amount=params.get('credit_amount', 0.00),
        balance=params.get('balance', 10000.00),
        merchant_name=params.get('merchant_name', 'TEST MERCHANT')
    )
    session.add(txn)
    session.commit()
    return txn
