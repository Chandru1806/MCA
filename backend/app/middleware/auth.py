from functools import wraps
from flask import request, jsonify
from app.auth.token_manager import TokenManager

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'success': False, 'error': 'Token missing'}), 401
        try:
            data = TokenManager.decode_token(token)
            current_profile_id = data['profile_id']
        except Exception as e:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        return f(current_profile_id, *args, **kwargs)
    return decorated
