# Postman Testing Steps - Database Verification

## Prerequisites
1. Install packages: `pip install -r requirements.txt`
2. Generate secret keys: `python generate_keys.py` → Copy to `.env`
3. Create tables: `python migrations/create_auth_tables.py`
4. Start server: `python run.py`
5. Import Postman files from `postman/` folder

---

## Test Steps

### Step 1: Test Signup (Create Profile)

**Request:**
- Method: `POST`
- URL: `http://localhost:5000/api/auth/profiles`
- Body (JSON):
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Expected Response (201):**
```json
{
  "success": true,
  "message": "Profile created successfully",
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "token_type": "Bearer",
    "expires_in": 900,
    "user": {
      "profile_id": "uuid-here",
      "username": "johndoe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "created_at": "2024-01-15T10:30:00"
    }
  }
}
```

**Verify:**
✓ Status code = 201
✓ `access_token` and `refresh_token` present
✓ `user.profile_id` is UUID format
✓ `user.username` = "johndoe"

---

### Step 2: Verify Database Storage

**Run verification script:**
```bash
python verify_database.py
```

**Expected Output:**
```
=== DATABASE VERIFICATION ===

1. USERS TABLE:
   Total users: 1
   - johndoe | john@example.com | Created: 2024-01-15 10:30:00

2. AUDIT_LOGS TABLE:
   Total logs: 1
   - Action: USER_SIGNUP | Time: 2024-01-15 10:30:00

3. PASSWORD VERIFICATION:
   - johndoe: Password hashed = $2b$12$abcdefghijk...

=== VERIFICATION COMPLETE ===
```

**Verify:**
✓ User exists in `users` table
✓ Password is hashed (starts with `$2b$12$`)
✓ Audit log created with action = "USER_SIGNUP"

---

### Step 3: Test Duplicate Username (409 Error)

**Request:**
- Method: `POST`
- URL: `http://localhost:5000/api/auth/profiles`
- Body (JSON):
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "username": "johndoe",
  "email": "jane@example.com",
  "password": "AnotherPass456"
}
```

**Expected Response (409):**
```json
{
  "success": false,
  "error": {
    "code": "DUPLICATE_USERNAME",
    "message": "Username already taken"
  }
}
```

**Verify:**
✓ Status code = 409
✓ Error code = "DUPLICATE_USERNAME"
✓ No new user created in database

---

### Step 4: Test Login

**Request:**
- Method: `POST`
- URL: `http://localhost:5000/api/auth/login`
- Body (JSON):
```json
{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Expected Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "token_type": "Bearer",
    "expires_in": 900,
    "user": {
      "profile_id": "uuid-here",
      "username": "johndoe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "created_at": "2024-01-15T10:30:00"
    }
  }
}
```

**Verify:**
✓ Status code = 200
✓ New tokens generated
✓ User data matches signup data

---

### Step 5: Verify Login Audit Log

**Run verification script again:**
```bash
python verify_database.py
```

**Expected Output:**
```
2. AUDIT_LOGS TABLE:
   Total logs: 2
   - Action: USER_SIGNUP | Time: 2024-01-15 10:30:00
   - Action: USER_LOGIN | Time: 2024-01-15 10:35:00
```

**Verify:**
✓ New audit log created with action = "USER_LOGIN"
✓ Total logs = 2

---

### Step 6: Test Invalid Login (401 Error)

**Request:**
- Method: `POST`
- URL: `http://localhost:5000/api/auth/login`
- Body (JSON):
```json
{
  "username": "johndoe",
  "password": "WrongPassword"
}
```

**Expected Response (401):**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid credentials"
  }
}
```

**Verify:**
✓ Status code = 401
✓ Error code = "INVALID_CREDENTIALS"
✓ No new audit log created

---

## Direct Database Verification (PostgreSQL)

**Connect to database:**
```bash
psql -U postgres -d expenseiq
```

**Check users table:**
```sql
SELECT profile_id, username, email, first_name, last_name, created_at 
FROM users;
```

**Check audit_logs table:**
```sql
SELECT log_id, profile_id, action, timestamp 
FROM audit_logs 
ORDER BY timestamp DESC;
```

**Verify password hash:**
```sql
SELECT username, LEFT(password_hash, 20) as hash_preview 
FROM users;
```

---

## Summary Checklist

✓ Signup creates user in `users` table
✓ Password is hashed with bcrypt
✓ Signup creates audit log with "USER_SIGNUP"
✓ Login verifies password correctly
✓ Login creates audit log with "USER_LOGIN"
✓ Duplicate username returns 409 error
✓ Invalid password returns 401 error
✓ Tokens are generated and returned
