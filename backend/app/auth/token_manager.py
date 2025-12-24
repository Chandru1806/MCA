from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

def generate_tokens(user_id):
    access_token = create_access_token(
        identity=str(user_id),
        expires_delta=timedelta(minutes=15)
    )
    refresh_token = create_refresh_token(
        identity=str(user_id),
        expires_delta=timedelta(days=7)
    )
    return access_token, refresh_token
