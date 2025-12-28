from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.preference_controller import PreferenceController

preference_bp = Blueprint('preference', __name__, url_prefix='/api/preference')

@preference_bp.route('', methods=['GET'])
@jwt_required()
def get_preferences():
    return PreferenceController.get_preferences()

@preference_bp.route('', methods=['PUT'])
@jwt_required()
def update_preferences():
    return PreferenceController.update_preferences()
