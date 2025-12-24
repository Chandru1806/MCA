import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run import create_app, db

app = create_app()

with app.app_context():
    try:
        db.session.execute("SELECT 1")
        print("✓ Database connection successful!")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
