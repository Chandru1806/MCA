# Postman Setup for ExpenseIQ

## Import Files into Postman

1. **Import Environment:**
   - Open Postman
   - Click "Import" button (top left)
   - Select `ExpenseIQ_Environment.json`
   - Environment "ExpenseIQ Environment" will be created

2. **Import Collection:**
   - Click "Import" button
   - Select `ExpenseIQ_Collection.json`
   - Collection "ExpenseIQ API Collection" will be created

3. **Select Environment:**
   - Click environment dropdown (top right)
   - Select "ExpenseIQ Environment"

## Environment Variables

| Variable | Description | Auto-set |
|----------|-------------|----------|
| `base_url` | API base URL (http://localhost:5000) | Manual |
| `access_token` | JWT access token | Auto (after login/signup) |
| `refresh_token` | JWT refresh token | Auto (after login/signup) |
| `user_id` | User profile ID | Auto (after login/signup) |

## Test Requests

### 1. Signup
- **Endpoint:** POST `{{base_url}}/api/auth/profiles`
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
- **Auto-saves:** access_token, refresh_token, user_id

### 2. Login
- **Endpoint:** POST `{{base_url}}/api/auth/login`
- **Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePass123"
}
```
- **Auto-saves:** access_token, refresh_token, user_id

## Using Tokens in Future Requests

Add this header to protected endpoints:
```
Authorization: Bearer {{access_token}}
```

Postman will automatically replace `{{access_token}}` with the saved token.
