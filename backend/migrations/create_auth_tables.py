"""
Run this script to create the database tables for authentication.
Execute from backend folder: python migrations/create_auth_tables.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import create_app, db
from app.models import User, AuditLog

def create_tables():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✓ Tables created successfully!")
        print("  - users")
        print("  - audit_logs")

if __name__ == "__main__":
    create_tables()