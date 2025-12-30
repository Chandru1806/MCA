import bcrypt
from app import db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.auth.token_manager import generate_tokens
from datetime import datetime

class AuthService:
    
    @staticmethod
    def signup(first_name, last_name, username, email, password):
        if User.query.filter_by(username=username).first():
            return None, "Username already taken", "DUPLICATE_USERNAME"
        
        if User.query.filter_by(email=email).first():
            return None, "Email already registered", "DUPLICATE_EMAIL"
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password_hash=password_hash,
            is_active='A'
        )
        
        db.session.add(user)
        db.session.commit()
        
        audit_log = AuditLog(
            profile_id=user.profile_id,
            action="INSERT",
            table_name="users",
            record_id=user.profile_id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        access_token, refresh_token = generate_tokens(user.profile_id)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': 900,
            'user': user.to_dict()
        }, None, None
    
    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return None, "Invalid credentials", "INVALID_CREDENTIALS"
        
        if user.is_active != 'A':
            return None, "Account is inactive", "ACCOUNT_INACTIVE"
        
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return None, "Invalid credentials", "INVALID_CREDENTIALS"
        
        audit_log = AuditLog(
            profile_id=user.profile_id,
            action="INSERT",
            table_name="users",
            record_id=user.profile_id
        )
        db.session.add(audit_log)
        db.session.commit()
        
        access_token, refresh_token = generate_tokens(user.profile_id)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': 900,
            'user': user.to_dict()
        }, None, None
    
    @staticmethod
    def get_user_by_id(profile_id):
        user = User.query.filter_by(profile_id=profile_id).first()
        
        if not user:
            return None, "User not found", "USER_NOT_FOUND"
        
        return {'user': user.to_dict()}, None, None
    
    @staticmethod
    def update_user(profile_id, update_data):
        user = User.query.filter_by(profile_id=profile_id).first()
        
        if not user:
            return None, "User not found", "USER_NOT_FOUND"
        
        if user.is_active != 'A':
            return None, "Account is inactive", "ACCOUNT_INACTIVE"
        
        old_values = user.to_dict()
        
        # Handle password change separately
        if 'password' in update_data:
            password_hash = bcrypt.hashpw(update_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password_hash = password_hash
            update_data.pop('password')  # Remove from update_data to avoid duplicate processing
        
        # Update other allowed fields
        for key, value in update_data.items():
            if hasattr(user, key) and key not in ['profile_id', 'username', 'password_hash', 'created_at', 'is_active', 'phone', 'city', 'state']:
                setattr(user, key, value)
        
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
        
        return {'user': user.to_dict()}, None, None
    
    @staticmethod
    def delete_user(profile_id):
        user = User.query.filter_by(profile_id=profile_id).first()
        
        if not user:
            return None, "User not found", "USER_NOT_FOUND"
        
        if user.is_active == 'I':
            return None, "Account already inactive", "ALREADY_INACTIVE"
        
        old_values = user.to_dict()
        user.is_active = 'I'
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        audit_log = AuditLog(
            profile_id=user.profile_id,
            action="DELETE",
            table_name="users",
            record_id=user.profile_id,
            old_values=old_values,
            new_values=user.to_dict()
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return {'message': 'User deactivated successfully'}, None, None
    
    @staticmethod
    def refresh_access_token(profile_id):
        access_token, _ = generate_tokens(profile_id)
        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': 900
        }
    
    @staticmethod
    def verify_email(email):
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return None, "Email not found", "EMAIL_NOT_FOUND"
        
        return {'exists': True, 'username': user.username}, None, None
