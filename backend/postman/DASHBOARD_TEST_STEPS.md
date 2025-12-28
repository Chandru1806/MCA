# Dashboard API Testing Guide

## Prerequisites

Before testing the Dashboard APIs, ensure:

1. **User Account Created**: You have a registered user account
2. **User Logged In**: You have a valid JWT access token
3. **Transactions Imported**: You have uploaded a PDF and imported transactions
4. **Transactions Categorized**: You have categorized the imported transactions

---

## Test Case 1: Get Category Spending

### Objective
Verify that the API returns category-wise spending totals sorted in descending order.

### Steps

**Step 1: Login to get access token**
```
POST {{base_url}}/api/auth/login
Body:
{
  "username": "johndoe",
  "password": "SecurePass123"
}

Expected Response: 200 OK
Save: access_token from response
```

**Step 2: Request category spending**
```
GET {{base_url}}/api/dashboard/spending
Headers:
  Authorization: Bearer {{access_token}}

Expected Response: 200 OK
```

**Step 3: Verify response structure**
```json
{
  "success": true,
  "data": [
    {
      "category": "Shopping",
      "total_amount": 15000.50,
      "transaction_count": 25
    },
    {
      "category": "Food",
      "total_amount": 8500.00,
      "transaction_count": 42
    }
  ]
}
```

**Step 4: Validate response**
- ✅ Response status is 200
- ✅ `success` field is `true`
- ✅ `data` is an array
- ✅ Categories are sorted by `total_amount` in descending order
- ✅ Each item has: `category`, `total_amount`, `transaction_count`
- ✅ Only debit transactions are included (no credits)

---

## Test Case 2: Get Spending Trends

### Objective
Verify that the API returns monthly spending trends grouped by category.

### Steps

**Step 1: Use existing access token from Test Case 1**

**Step 2: Request spending trends with date range**
```
GET {{base_url}}/api/dashboard/trends?start_date=2024-01-01&end_date=2024-12-31
Headers:
  Authorization: Bearer {{access_token}}

Expected Response: 200 OK
```

**Step 3: Verify response structure**
```json
{
  "success": true,
  "data": [
    {
      "year": 2024,
      "month": 1,
      "category": "Food",
      "amount": 2500.00
    },
    {
      "year": 2024,
      "month": 1,
      "category": "Shopping",
      "amount": 5000.00
    },
    {
      "year": 2024,
      "month": 2,
      "category": "Food",
      "amount": 3000.00
    }
  ]
}
```

**Step 4: Validate response**
- ✅ Response status is 200
- ✅ `success` field is `true`
- ✅ `data` is an array
- ✅ Data is sorted by year and month
- ✅ Each item has: `year`, `month`, `category`, `amount`
- ✅ Amounts are grouped by month and category

**Step 5: Test without date range (optional parameters)**
```
GET {{base_url}}/api/dashboard/trends
Headers:
  Authorization: Bearer {{access_token}}

Expected Response: 200 OK
Should return all historical data
```

---

## Test Case 3: Error Handling - Missing Authentication

### Objective
Verify that the API returns 401 when no authentication token is provided.

### Steps

**Step 1: Request without Authorization header**
```
GET {{base_url}}/api/dashboard/spending

Expected Response: 401 Unauthorized
```

**Step 2: Verify error response**
```json
{
  "msg": "Missing Authorization Header"
}
```

---

## Test Case 4: Error Handling - Invalid Token

### Objective
Verify that the API returns 401 when an invalid token is provided.

### Steps

**Step 1: Request with invalid token**
```
GET {{base_url}}/api/dashboard/spending
Headers:
  Authorization: Bearer invalid_token_here

Expected Response: 401 Unauthorized
```

**Step 2: Verify error response**
```json
{
  "msg": "Invalid token" or "Token has expired"
}
```

---

## Test Case 5: Error Handling - Invalid Date Format

### Objective
Verify that the API returns 400 when invalid date format is provided.

### Steps

**Step 1: Request with invalid date format**
```
GET {{base_url}}/api/dashboard/trends?start_date=01-01-2024&end_date=31-12-2024
Headers:
  Authorization: Bearer {{access_token}}

Expected Response: 400 Bad Request
```

**Step 2: Verify error response**
```json
{
  "success": false,
  "error": "Invalid date format. Use YYYY-MM-DD"
}
```

---

## Test Case 6: Empty Data Scenario

### Objective
Verify that the API handles users with no transactions gracefully.

### Steps

**Step 1: Login with a new user who has no transactions**
```
POST {{base_url}}/api/auth/login
Body:
{
  "username": "newuser",
  "password": "password123"
}
```

**Step 2: Request category spending**
```
GET {{base_url}}/api/dashboard/spending
Headers:
  Authorization: Bearer {{access_token}}

Expected Response: 200 OK
```

**Step 3: Verify empty data response**
```json
{
  "success": true,
  "data": []
}
```

---

## Test Case 7: Data Accuracy Validation

### Objective
Verify that the aggregated amounts match the database records.

### Steps

**Step 1: Get category spending from API**
```
GET {{base_url}}/api/dashboard/spending
Headers:
  Authorization: Bearer {{access_token}}
```

**Step 2: Manually verify in database**
```sql
SELECT 
    tc.category_name,
    SUM(t.debit_amount) as total_amount,
    COUNT(t.transaction_id) as transaction_count
FROM transactions t
JOIN transaction_categories tc ON t.transaction_id = tc.transaction_id
WHERE t.profile_id = 'user_profile_id'
  AND t.debit_amount IS NOT NULL
GROUP BY tc.category_name
ORDER BY SUM(t.debit_amount) DESC;
```

**Step 3: Compare API response with database results**
- ✅ Amounts match exactly
- ✅ Transaction counts match
- ✅ Categories match
- ✅ Sort order matches

---

## Test Case 8: Performance Testing

### Objective
Verify that the API responds within acceptable time limits.

### Steps

**Step 1: Request category spending**
```
GET {{base_url}}/api/dashboard/spending
Headers:
  Authorization: Bearer {{access_token}}

Measure: Response time
```

**Step 2: Validate performance**
- ✅ Response time < 2 seconds for 1000 transactions
- ✅ Response time < 5 seconds for 10,000 transactions

---

## Using Postman Collection

### Import Collection
1. Open Postman
2. Click "Import"
3. Select `ExpenseIQ_Collection.json`
4. Import `ExpenseIQ_Environment.json` for environment variables

### Set Environment Variables
```
base_url: http://localhost:5000
access_token: (auto-populated after login)
refresh_token: (auto-populated after login)
user_id: (auto-populated after login)
file_id: (auto-populated after PDF upload)
```

### Run Tests in Order
1. **Authentication** → Login
2. **PDF Upload** → Upload PDF
3. **Transactions** → Import Transactions
4. **Categorization** → Categorize Transactions
5. **Dashboard** → Get Category Spending
6. **Dashboard** → Get Spending Trends

---

## Expected Results Summary

| Test Case | Expected Status | Expected Behavior |
|-----------|----------------|-------------------|
| Get Category Spending | 200 OK | Returns sorted category totals |
| Get Spending Trends | 200 OK | Returns monthly trend data |
| Missing Auth | 401 Unauthorized | Returns auth error |
| Invalid Token | 401 Unauthorized | Returns token error |
| Invalid Date Format | 400 Bad Request | Returns format error |
| Empty Data | 200 OK | Returns empty array |
| Data Accuracy | 200 OK | Matches database records |
| Performance | 200 OK | Responds within time limit |

---

## Troubleshooting

### Issue: 401 Unauthorized
**Solution:** Ensure you have a valid access token. Re-login if token expired.

### Issue: Empty data array
**Solution:** Verify that:
- Transactions are imported
- Transactions are categorized
- User has debit transactions (not just credits)

### Issue: 500 Internal Server Error
**Solution:** Check:
- Database connection is active
- All required tables exist
- Foreign key relationships are intact

### Issue: Incorrect amounts
**Solution:** Verify:
- Only debit_amount is summed (not credit_amount)
- Transactions belong to the correct profile_id
- JOIN query is correct

---

## Notes

- All endpoints require JWT authentication
- Tokens expire after 15 minutes (configurable)
- Use refresh token to get new access token
- Date format must be YYYY-MM-DD
- Only debit transactions (expenses) are included in calculations
- Categories are sorted by total spending in descending order
