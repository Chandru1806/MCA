from flask import jsonify
from marshmallow import ValidationError

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    @app.errorhandler(ValidationError)
    def validation_error(error):
        return jsonify({'success': False, 'error': error.messages}), 400
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        return jsonify({'success': False, 'error': str(error)}), 500
