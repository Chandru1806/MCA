# Authentication Module Setup

## 1. Install Required Packages

```bash
cd backend
pip install -r requirements.txt
```

## 2. Create Database Tables

```bash
python migrations/create_auth_tables.py
```

## 3. Start the Server

```bash
python run.py
```

## 4. Test the APIs

### Signup (Create Profile)

**Endpoint:** `POST http://localhost:5000/api/auth/profiles`

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Success Response (201):**
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

**Error Response (409):**
```json
{
  "success": false,
  "error": {
    "code": "DUPLICATE_USERNAME",
    "message": "Username already taken"
  }
}
```

### Login

**Endpoint:** `POST http://localhost:5000/api/auth/login`

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Success Response (200):**
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

**Error Response (401):**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid credentials"
  }
}
```

## Database Tables Created

### users
- profile_id (UUID, Primary Key)
- first_name (VARCHAR 100)
- last_name (VARCHAR 100)
- username (VARCHAR 80, Unique)
- email (VARCHAR 120, Unique)
- password_hash (VARCHAR 255)
- created_at (TIMESTAMP)

### audit_logs
- log_id (UUID, Primary Key)
- profile_id (UUID, Foreign Key → users.profile_id)
- action (VARCHAR 50)
- timestamp (TIMESTAMP)

## Token Details

- **Access Token:** Expires in 15 minutes
- **Refresh Token:** Expires in 7 days
- **Algorithm:** HS256
- **Secret:** Stored in .env file (JWT_SECRET_KEY)

## Security Features

✓ Password hashing with bcrypt (salt rounds: 12)
✓ JWT-based authentication
✓ Duplicate username/email validation
✓ Input validation with marshmallow
✓ Audit logging for all auth actions
✓ Secure password requirements (min 8 characters)
