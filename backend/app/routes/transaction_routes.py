from flask import Blueprint
from app.controllers.transaction_controller import transaction_bp
from app.controllers.categorization_controller import categorization_bp

def register_transaction_routes(app):
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
    app.register_blueprint(categorization_bp, url_prefix='/api/categorization')
