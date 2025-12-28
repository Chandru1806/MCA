from app import db
from datetime import datetime
import uuid

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    transaction_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = db.Column(db.String(36), db.ForeignKey('users.profile_id'), nullable=False)
    statement_id = db.Column(db.Integer, db.ForeignKey('bank_statements.file_id'), nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    debit_amount = db.Column(db.Numeric(12, 2))
    credit_amount = db.Column(db.Numeric(12, 2))
    balance = db.Column(db.Numeric(12, 2))
    merchant_name = db.Column(db.String(255))
    is_repaired = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
