from app import db
from datetime import datetime
import uuid

class TransactionCategory(db.Model):
    __tablename__ = 'transaction_categories'
    
    category_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = db.Column(db.String(36), db.ForeignKey('users.profile_id'), nullable=False)
    transaction_id = db.Column(db.String(36), db.ForeignKey('transactions.transaction_id'), nullable=False)
    category_name = db.Column(db.String(50), nullable=False)
    confidence_score = db.Column(db.Numeric(3, 2))
    classification_method = db.Column(db.String(20), nullable=False)
    rule_based_prediction = db.Column(db.String(50))
    ml_prediction = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
