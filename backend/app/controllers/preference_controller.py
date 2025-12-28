from flask import request
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError
from app.services.preference_service import PreferenceService
from app.validators.preference_validator import PreferenceSchema
from app.utils.response import success_response, error_response
import logging

logger = logging.getLogger(__name__)

class PreferenceController:
    
    @staticmethod
    def get_preferences():
        try:
            profile_id = get_jwt_identity()
            result, error_msg, error_code = PreferenceService.get_preferences(profile_id)
            
            if error_msg:
                return error_response(error_msg, code=error_code, status=404)
            
            return success_response(result, "Preferences retrieved successfully", 200)
        
        except Exception as e:
            logger.error(f"Get preferences error: {str(e)}")
            return error_response("Server error", code="SERVER_ERROR", status=500)
    
    @staticmethod
    def update_preferences():
        try:
            profile_id = get_jwt_identity()
            schema = PreferenceSchema()
            data = schema.load(request.get_json())
            
            result, error_msg, error_code = PreferenceService.update_preferences(profile_id, data)
            
            if error_msg:
                status = 404 if error_code == "USER_NOT_FOUND" else 400
                return error_response(error_msg, code=error_code, status=status)
            
            return success_response(result, "Preferences updated successfully", 200)
        
        except ValidationError as e:
            return error_response("Invalid input data", code="INVALID_INPUT", details=e.messages, status=400)
        except Exception as e:
            logger.error(f"Update preferences error: {str(e)}")
            return error_response("Server error", code="SERVER_ERROR", status=500)
