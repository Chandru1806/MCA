# Postman Testing Guide - Updated with New Endpoints

## Import Steps

1. **Delete old collection** (if already imported)
   - Right-click "ExpenseIQ API Collection" → Delete

2. **Import updated collection**
   - Click "Import" button
   - Select `postman/ExpenseIQ_Collection.json`
   - Collection now has 5 requests

3. **Verify environment is selected**
   - Top-right dropdown → "ExpenseIQ Environment"

---

## Testing Flow

### Step 1: Signup
- **Request:** POST `/api/auth/profiles`
- **Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```
- **Result:** `user_id` auto-saved to environment

---

### Step 2: Get User by ID
- **Request:** GET `/api/auth/profiles/{{user_id}}`
- **No body needed**
- **Expected Response (200):**
```json
{
  "success": true,
  "message": "User retrieved successfully",
  "data": {
    "user": {
      "profile_id": "uuid-here",
      "username": "johndoe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "phone": null,
      "address_line_1": null,
      "address_line_2": null,
      "city": null,
      "state": null,
      "is_active": "A",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  }
}
```

---

### Step 3: Update User
- **Request:** PUT `/api/auth/profiles/{{user_id}}`
- **Body:**
```json
{
  "first_name": "Updated",
  "last_name": "Name",
  "phone": "1234567890",
  "city": "Chennai",
  "state": "Tamil Nadu"
}
```
- **Expected Response (200):**
```json
{
  "success": true,
  "message": "User updated successfully",
  "data": {
    "user": {
      "profile_id": "uuid-here",
      "first_name": "Updated",
      "last_name": "Name",
      "phone": "1234567890",
      "city": "Chennai",
      "state": "Tamil Nadu",
      "is_active": "A",
      "updated_at": "2024-01-15T10:35:00"
    }
  }
}
```

---

### Step 4: Get User Again (Verify Update)
- **Request:** GET `/api/auth/profiles/{{user_id}}`
- **Verify:** Updated fields are reflected

---

### Step 5: Delete User (Soft Delete)
- **Request:** DELETE `/api/auth/profiles/{{user_id}}`
- **No body needed**
- **Expected Response (200):**
```json
{
  "success": true,
  "message": "User deactivated successfully",
  "data": {
    "message": "User deactivated successfully"
  }
}
```

---

### Step 6: Verify Soft Delete
- **Request:** GET `/api/auth/profiles/{{user_id}}`
- **Verify:** `is_active` = "I"

---

### Step 7: Try Login with Deleted User
- **Request:** POST `/api/auth/login`
- **Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123"
}
```
- **Expected Response (401):**
```json
{
  "success": false,
  "error": {
    "code": "ACCOUNT_INACTIVE",
    "message": "Account is inactive"
  }
}
```

---

## Database Verification

**Check is_active status:**
```sql
SELECT profile_id, username, first_name, last_name, is_active, updated_at 
FROM users 
WHERE username = 'johndoe';
```

**Expected:**
- After signup: `is_active = 'A'`
- After delete: `is_active = 'I'`

---

## API Summary

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/auth/profiles` | Signup | 201 |
| POST | `/api/auth/login` | Login | 200 |
| GET | `/api/auth/profiles/{id}` | Get user | 200 |
| PUT | `/api/auth/profiles/{id}` | Update user | 200 |
| DELETE | `/api/auth/profiles/{id}` | Soft delete | 200 |

---

## Notes

- `{{user_id}}` is auto-populated after signup/login
- Update only sends fields you want to change (partial update)
- Delete is soft delete (sets `is_active = 'I'`)
- Inactive users cannot login
