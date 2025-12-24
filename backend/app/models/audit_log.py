from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
import uuid
from app import db

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    log_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.profile_id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    table_name = db.Column(db.String(50), nullable=False)
    record_id = db.Column(UUID(as_uuid=True), nullable=True)
    old_values = db.Column(JSONB, nullable=True)
    new_values = db.Column(JSONB, nullable=True)
    ip_address = db.Column(INET, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
