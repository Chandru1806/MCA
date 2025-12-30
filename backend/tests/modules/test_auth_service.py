import pytest
import bcrypt
from app.services.auth_service import AuthService
from app.models.user import User

class TestAuthService:
    
    def test_signup_success(self, session):
        result, error, code = AuthService.signup(
            'FirstName', 'LastName', f'username_{id(session)}', f'email_{id(session)}@test.com', 'testpass'
        )
        assert error is None
        assert result['user']['username'] == f'username_{id(session)}'
        assert 'access_token' in result
    
    def test_signup_duplicate_username(self, session, sample_user):
        result, error, code = AuthService.signup(
            'New', 'User', sample_user.username, f'new_{id(session)}@test.com', 'testpass'
        )
        assert error == "Username already taken"
        assert code == "DUPLICATE_USERNAME"
    
    def test_signup_duplicate_email(self, session, sample_user):
        result, error, code = AuthService.signup(
            'New', 'User', f'newuser_{id(session)}', sample_user.email, 'testpass'
        )
        assert error == "Email already registered"
        assert code == "DUPLICATE_EMAIL"
    
    def test_login_success(self, session):
        username = f'loginuser_{id(session)}'
        password = 'testpass'
        AuthService.signup('First', 'Last', username, f'{username}@test.com', password)
        result, error, code = AuthService.login(username, password)
        assert error is None
        assert 'access_token' in result
    
    def test_login_invalid_credentials(self, session):
        result, error, code = AuthService.login(f'nonexistent_{id(session)}', 'wrongpass')
        assert error == "Invalid credentials"
        assert code == "INVALID_CREDENTIALS"
    
    def test_get_user_by_id(self, session, sample_user):
        result, error, code = AuthService.get_user_by_id(sample_user.profile_id)
        assert error is None
        assert result['user']['username'] == sample_user.username
    
    def test_update_user(self, session, sample_user):
        result, error, code = AuthService.update_user(
            sample_user.profile_id, {'first_name': 'UpdatedName'}
        )
        assert error is None
        assert result['user']['first_name'] == 'UpdatedName'
    
    def test_delete_user(self, session, sample_user):
        result, error, code = AuthService.delete_user(sample_user.profile_id)
        assert error is None
        user = User.query.get(sample_user.profile_id)
        assert user.is_active == 'I'
