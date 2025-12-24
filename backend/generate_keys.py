import secrets

print("Add these to your .env file:\n")
print(f"JWT_SECRET_KEY={secrets.token_urlsafe(32)}")
print(f"FLASK_SECRET_KEY={secrets.token_urlsafe(32)}")
