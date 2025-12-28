# Analytics API Testing Guide

## Prerequisites

Before testing the Analytics API, ensure:

1. **User Account Created**: You have a registered user account
2. **User Logged In**: You have a valid JWT access token
3. **Transactions Imported**: You have uploaded a PDF and imported transactions
4. **Transactions Categorized**: You have categorized the imported transactions
5. **Historical Data**: At least 2-3 months of transaction data for accurate averages

---

## Test Case 1: Basic Forecast with Multiple Categories

### Objective
Verify that the API calculates savings forecast for multiple categories individually.

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

**Step 2: Request savings forecast**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Authorization: Bearer {{access_token}}
  Content-Type: application/json
Body:
{
  "budget_limit": 5000,
  "target_month": "2025-03-01",
  "categories": ["Food", "Shopping"]
}

Expected Response: 200 OK
```

**Step 3: Verify response structure**
```json
{
  "success": true,
  "data": [
    {
      "category": "Food",
      "current_spending": 8500.00,
      "budget_limit": 5000.00,
      "savings": 3500.00,
      "message": "If you reduce spending in Food to ₹5000.00, you'll save ₹3500.00"
    },
    {
      "category": "Shopping",
      "current_spending": 15000.50,
      "budget_limit": 5000.00,
      "savings": 10000.50,
      "message": "If you reduce spending in Shopping to ₹5000.00, you'll save ₹10000.50"
    }
  ]
}
```

**Step 4: Validate response**
- ✅ Response status is 200
- ✅ `success` field is `true`
- ✅ `data` is an array with 2 items (one per category)
- ✅ Each item has: `category`, `current_spending`, `budget_limit`, `savings`, `message`
- ✅ `savings` = `current_spending` - `budget_limit`
- ✅ Results are NOT aggregated (individual per category)

---

## Test Case 2: Single Category Forecast

### Objective
Verify that the API works with a single category selection.

### Steps

**Step 1: Use existing access token from Test Case 1**

**Step 2: Request forecast for single category**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Authorization: Bearer {{access_token}}
  Content-Type: application/json
Body:
{
  "budget_limit": 3000,
  "target_month": "2025-04-01",
  "categories": ["Food"]
}

Expected Response: 200 OK
```

**Step 3: Verify response**
```json
{
  "success": true,
  "data": [
    {
      "category": "Food",
      "current_spending": 8500.00,
      "budget_limit": 3000.00,
      "savings": 5500.00,
      "message": "If you reduce spending in Food to ₹3000.00, you'll save ₹5500.00"
    }
  ]
}
```

**Step 4: Validate**
- ✅ Only one category in response
- ✅ Calculations are correct

---

## Test Case 3: Multiple Categories (4+ categories)

### Objective
Verify that the API handles multiple category selections correctly.

### Steps

**Step 1: Request forecast for 4 categories**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Authorization: Bearer {{access_token}}
  Content-Type: application/json
Body:
{
  "budget_limit": 10000,
  "target_month": "2025-05-01",
  "categories": ["Food", "Shopping", "Travel", "Entertainment"]
}

Expected Response: 200 OK
```

**Step 2: Verify response has 4 separate results**
- ✅ Array has 4 items
- ✅ Each category has individual savings calculation
- ✅ No aggregation across categories

---

## Test Case 4: Validation - Missing Budget Limit

### Objective
Verify that the API returns 400 when budget_limit is missing or invalid.

### Steps

**Step 1: Send request without budget_limit**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Authorization: Bearer {{access_token}}
  Content-Type: application/json
Body:
{
  "target_month": "2025-03-01",
  "categories": ["Food"]
}

Expected Response: 400 Bad Request
```

**Step 2: Verify error response**
```json
{
  "success": false,
  "error": "Budget limit must be greater than 0"
}
```

**Step 3: Send request with budget_limit = 0**
```
Body:
{
  "budget_limit": 0,
  "target_month": "2025-03-01",
  "categories": ["Food"]
}

Expected Response: 400 Bad Request
```

**Step 4: Send request with negative budget_limit**
```
Body:
{
  "budget_limit": -1000,
  "target_month": "2025-03-01",
  "categories": ["Food"]
}

Expected Response: 400 Bad Request
```

---

## Test Case 5: Validation - Invalid Date Format

### Objective
Verify that the API returns 400 when target_month has invalid format.

### Steps

**Step 1: Send request with invalid date format**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Authorization: Bearer {{access_token}}
  Content-Type: application/json
Body:
{
  "budget_limit": 5000,
  "target_month": "01-03-2025",
  "categories": ["Food"]
}

Expected Response: 400 Bad Request
```

**Step 2: Verify error response**
```json
{
  "success": false,
  "error": "Invalid date format. Use YYYY-MM-DD"
}
```

**Step 3: Test other invalid formats**
```
"target_month": "2025/03/01" → 400 Bad Request
"target_month": "March 2025" → 400 Bad Request
"target_month": "2025-3-1" → 400 Bad Request (should be 2025-03-01)
```

---

## Test Case 6: Validation - Empty Categories Array

### Objective
Verify that the API returns 400 when categories array is empty.

### Steps

**Step 1: Send request with empty categories**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Authorization: Bearer {{access_token}}
  Content-Type: application/json
Body:
{
  "budget_limit": 5000,
  "target_month": "2025-03-01",
  "categories": []
}

Expected Response: 400 Bad Request
```

**Step 2: Verify error response**
```json
{
  "success": false,
  "error": "At least one category must be selected"
}
```

---

## Test Case 7: Authentication - Missing Token

### Objective
Verify that the API returns 401 when no authentication token is provided.

### Steps

**Step 1: Request without Authorization header**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Content-Type: application/json
Body:
{
  "budget_limit": 5000,
  "target_month": "2025-03-01",
  "categories": ["Food"]
}

Expected Response: 401 Unauthorized
```

**Step 2: Verify error response**
```json
{
  "msg": "Missing Authorization Header"
}
```

---

## Test Case 8: Authentication - Invalid Token

### Objective
Verify that the API returns 401 when an invalid token is provided.

### Steps

**Step 1: Request with invalid token**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Authorization: Bearer invalid_token_here
  Content-Type: application/json
Body:
{
  "budget_limit": 5000,
  "target_month": "2025-03-01",
  "categories": ["Food"]
}

Expected Response: 401 Unauthorized
```

---

## Test Case 9: Category with No Historical Data

### Objective
Verify that the API handles categories with no transaction history.

### Steps

**Step 1: Request forecast for category with no data**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Authorization: Bearer {{access_token}}
  Content-Type: application/json
Body:
{
  "budget_limit": 5000,
  "target_month": "2025-03-01",
  "categories": ["Education"]
}

Expected Response: 200 OK
```

**Step 2: Verify response**
```json
{
  "success": true,
  "data": [
    {
      "category": "Education",
      "current_spending": 0.00,
      "budget_limit": 5000.00,
      "savings": -5000.00,
      "message": "If you reduce spending in Education to ₹5000.00, you'll save ₹-5000.00"
    }
  ]
}
```

**Step 3: Validate**
- ✅ `current_spending` is 0.00
- ✅ `savings` is negative (user is under budget)

---

## Test Case 10: Data Accuracy Validation

### Objective
Verify that the calculated average monthly spending is accurate.

### Steps

**Step 1: Get forecast from API**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Authorization: Bearer {{access_token}}
  Content-Type: application/json
Body:
{
  "budget_limit": 5000,
  "target_month": "2025-03-01",
  "categories": ["Food"]
}
```

**Step 2: Manually calculate average in database**
```sql
WITH monthly_spending AS (
    SELECT 
        EXTRACT(YEAR FROM t.transaction_date) as year,
        EXTRACT(MONTH FROM t.transaction_date) as month,
        SUM(t.debit_amount) as monthly_total
    FROM transactions t
    JOIN transaction_categories tc ON t.transaction_id = tc.transaction_id
    WHERE t.profile_id = 'user_profile_id'
        AND tc.category_name = 'Food'
        AND t.debit_amount IS NOT NULL
    GROUP BY year, month
)
SELECT AVG(monthly_total) as avg_monthly_spending
FROM monthly_spending;
```

**Step 3: Compare API response with database result**
- ✅ `current_spending` from API matches database calculation
- ✅ Rounding is consistent (2 decimal places)

---

## Test Case 11: Negative Savings (Under Budget)

### Objective
Verify that the API correctly handles cases where user is already under budget.

### Steps

**Step 1: Request forecast with high budget limit**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Authorization: Bearer {{access_token}}
  Content-Type: application/json
Body:
{
  "budget_limit": 50000,
  "target_month": "2025-03-01",
  "categories": ["Food"]
}

Expected Response: 200 OK
```

**Step 2: Verify response**
```json
{
  "success": true,
  "data": [
    {
      "category": "Food",
      "current_spending": 8500.00,
      "budget_limit": 50000.00,
      "savings": -41500.00,
      "message": "If you reduce spending in Food to ₹50000.00, you'll save ₹-41500.00"
    }
  ]
}
```

**Step 3: Validate**
- ✅ `savings` is negative
- ✅ Message still displays correctly

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
```

### Run Tests in Order
1. **Authentication** → Login
2. **PDF Upload** → Upload PDF
3. **Transactions** → Import Transactions
4. **Categorization** → Categorize Transactions
5. **Analytics** → Forecast Savings

---

## Expected Results Summary

| Test Case | Expected Status | Expected Behavior |
|-----------|----------------|-------------------|
| Basic Forecast | 200 OK | Returns individual savings per category |
| Single Category | 200 OK | Returns one category result |
| Multiple Categories | 200 OK | Returns separate results (not aggregated) |
| Missing Budget Limit | 400 Bad Request | Returns validation error |
| Invalid Date Format | 400 Bad Request | Returns format error |
| Empty Categories | 400 Bad Request | Returns validation error |
| Missing Auth | 401 Unauthorized | Returns auth error |
| Invalid Token | 401 Unauthorized | Returns token error |
| No Historical Data | 200 OK | Returns 0.00 current spending |
| Data Accuracy | 200 OK | Matches database calculation |
| Negative Savings | 200 OK | Correctly shows negative value |

---

## Troubleshooting

### Issue: 401 Unauthorized
**Solution:** Ensure you have a valid access token. Re-login if token expired.

### Issue: current_spending is 0.00
**Solution:** Verify that:
- User has transactions in the selected category
- Transactions are categorized
- Transactions have debit_amount (not just credits)
- At least one month of data exists

### Issue: 500 Internal Server Error
**Solution:** Check:
- Database connection is active
- All required tables exist
- JOIN query is working correctly

### Issue: Incorrect average calculation
**Solution:** Verify:
- Only debit transactions are included
- Grouping by month is correct
- Average calculation includes all months

---

## Notes

- All endpoints require JWT authentication
- Tokens expire after 15 minutes (configurable)
- Date format must be YYYY-MM-DD
- Budget limit must be greater than 0
- Categories array must not be empty
- Savings calculated individually per category (not aggregated)
- Negative savings means user is already under budget
- Historical average is calculated from all available months
