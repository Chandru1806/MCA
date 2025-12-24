from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/profiles', methods=['POST'])
def signup():
    return AuthController.signup()

@auth_bp.route('/login', methods=['POST'])
def login():
    return AuthController.login()

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    return AuthController.refresh_token()

@auth_bp.route('/profiles/<uuid:profile_id>', methods=['GET'])
def get_user(profile_id):
    return AuthController.get_user(profile_id)

@auth_bp.route('/profiles/<uuid:profile_id>', methods=['PUT'])
def update_user(profile_id):
    return AuthController.update_user(profile_id)

@auth_bp.route('/profiles/<uuid:profile_id>', methods=['DELETE'])
def delete_user(profile_id):
    return AuthController.delete_user(profile_id)
