from flask import request
from marshmallow import ValidationError
from app.services.auth_service import AuthService
from app.validators.auth_validator import SignupSchema, LoginSchema, UpdateUserSchema
from app.utils.response import success_response, error_response
import logging

logger = logging.getLogger(__name__)

class AuthController:
    
    @staticmethod
    def signup():
        try:
            schema = SignupSchema()
            data = schema.load(request.get_json())
            
            result, error_msg, error_code = AuthService.signup(
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            
            if error_msg:
                return error_response(error_msg, code=error_code, status=409)
            
            return success_response(result, "Profile created successfully", 201)
        
        except ValidationError as e:
            return error_response("Invalid input data", code="INVALID_INPUT", details=e.messages, status=400)
        except Exception as e:
            logger.error(f"Signup error: {str(e)}")
            return error_response("Server error", code="SERVER_ERROR", status=500)
    
    @staticmethod
    def login():
        try:
            schema = LoginSchema()
            data = schema.load(request.get_json())
            
            result, error_msg, error_code = AuthService.login(
                username=data['username'],
                password=data['password']
            )
            
            if error_msg:
                return error_response(error_msg, code=error_code, status=401)
            
            return success_response(result, "Login successful", 200)
        
        except ValidationError as e:
            return error_response("Username and password required", code="INVALID_INPUT", details=e.messages, status=400)
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return error_response("Server error", code="SERVER_ERROR", status=500)
    
    @staticmethod
    def get_user(profile_id):
        try:
            result, error_msg, error_code = AuthService.get_user_by_id(profile_id)
            
            if error_msg:
                return error_response(error_msg, code=error_code, status=404)
            
            return success_response(result, "User retrieved successfully", 200)
        
        except Exception as e:
            logger.error(f"Get user error: {str(e)}")
            return error_response("Server error", code="SERVER_ERROR", status=500)
    
    @staticmethod
    def update_user(profile_id):
        try:
            schema = UpdateUserSchema()
            data = schema.load(request.get_json())
            
            result, error_msg, error_code = AuthService.update_user(profile_id, data)
            
            if error_msg:
                status = 404 if error_code == "USER_NOT_FOUND" else 400
                return error_response(error_msg, code=error_code, status=status)
            
            return success_response(result, "User updated successfully", 200)
        
        except ValidationError as e:
            return error_response("Invalid input data", code="INVALID_INPUT", details=e.messages, status=400)
        except Exception as e:
            logger.error(f"Update user error: {str(e)}")
            return error_response("Server error", code="SERVER_ERROR", status=500)
    
    @staticmethod
    def delete_user(profile_id):
        try:
            result, error_msg, error_code = AuthService.delete_user(profile_id)
            
            if error_msg:
                status = 404 if error_code == "USER_NOT_FOUND" else 400
                return error_response(error_msg, code=error_code, status=status)
            
            return success_response(result, "User deactivated successfully", 200)
        
        except Exception as e:
            logger.error(f"Delete user error: {str(e)}")
            return error_response("Server error", code="SERVER_ERROR", status=500)
