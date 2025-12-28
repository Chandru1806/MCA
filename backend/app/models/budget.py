from app import db
from datetime import datetime
import uuid

class Budget(db.Model):
    __tablename__ = 'budgets'
    
    budget_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = db.Column(db.String(36), db.ForeignKey('users.profile_id'), nullable=False)
    category_name = db.Column(db.String(50), nullable=False)
    budget_limit = db.Column(db.Numeric(12, 2), nullable=False)
    budget_month = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
