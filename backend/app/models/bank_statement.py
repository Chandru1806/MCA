from app import db
from datetime import datetime

class BankStatement(db.Model):
    __tablename__ = 'bank_statements'
    
    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_id = db.Column(db.String(36), db.ForeignKey('users.profile_id'), nullable=False)
    bank_name = db.Column(db.String(50), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500))
    file_size_bytes = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    processing_status = db.Column(db.String(20), default='PENDING')
    error_message = db.Column(db.Text)
    extracted_csv_path = db.Column(db.String(500))
    normalized_csv_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
