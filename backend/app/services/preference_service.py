from app import db
from app.models.user import User
from app.models.audit_log import AuditLog
from datetime import datetime

class PreferenceService:
    
    @staticmethod
    def get_preferences(profile_id):
        user = User.query.filter_by(profile_id=profile_id).first()
        
        if not user:
            return None, "User not found", "USER_NOT_FOUND"
        
        return {
            'profile_id': str(user.profile_id),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            # 'password_hash': user.password_hash,
            'email': user.email,
            'phone': user.phone,
            'address_line_1': user.address_line_1,
            'address_line_2': user.address_line_2,
            'city': user.city,
            'state': user.state,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat(),
            'is_active': user.is_active
        }, None, None
    
    @staticmethod
    def update_preferences(profile_id, preference_data):
        user = User.query.filter_by(profile_id=profile_id).first()
        
        if not user:
            return None, "User not found", "USER_NOT_FOUND"
        
        if user.is_active != 'A':
            return None, "Account is inactive", "ACCOUNT_INACTIVE"
        
        old_values = user.to_dict()
        
        if 'phone' in preference_data:
            user.phone = preference_data['phone']
        if 'address_line_1' in preference_data:
            user.address_line_1 = preference_data['address_line_1']
        if 'address_line_2' in preference_data:
            user.address_line_2 = preference_data['address_line_2']
        if 'city' in preference_data:
            user.city = preference_data['city']
        if 'state' in preference_data:
            user.state = preference_data['state']
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        audit_log = AuditLog(
            profile_id=user.profile_id,
            action="UPDATE",
            table_name="users",
            record_id=user.profile_id,
            old_values=old_values,
            new_values=user.to_dict()
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return {
            'profile_id': str(user.profile_id),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            # 'password_hash': user.password_hash,
            'email': user.email,
            'phone': user.phone,
            'address_line_1': user.address_line_1,
            'address_line_2': user.address_line_2,
            'city': user.city,
            'state': user.state,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat(),
            'is_active': user.is_active
        }, None, None
