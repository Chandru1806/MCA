# Budget Saving Testing Guide

## Overview
This guide covers testing the budget saving functionality added to the Analytics module.

---

## Test Case 1: Forecast with Budget Saving

### Objective
Verify that budgets are saved to the database when `save_budget: true` is provided.

### Steps

**Step 1: Login and get access token**
```
POST {{base_url}}/api/auth/login
```

**Step 2: Forecast savings with save_budget enabled**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Authorization: Bearer {{access_token}}
  Content-Type: application/json
Body:
{
  "budget_limit": 5000,
  "target_month": "2025-03-01",
  "categories": ["Food", "Shopping"],
  "save_budget": true
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
  ],
  "budget_saved": true
}
```

**Step 4: Verify in database**
```sql
SELECT * FROM budgets 
WHERE profile_id = 'your_profile_id' 
  AND budget_month = '2025-03-01';
```

**Expected:**
- 2 records (Food and Shopping)
- budget_limit = 5000.00 for both
- budget_month = 2025-03-01

**Postman:** Use "Forecast Savings" request with `save_budget: true`

**Verify:**
- ✓ Response has `budget_saved: true`
- ✓ Budgets saved in database
- ✓ Forecast calculation still works

---

## Test Case 2: Forecast Without Budget Saving

### Objective
Verify that budgets are NOT saved when `save_budget: false` or omitted.

### Steps

**Step 1: Forecast without save_budget parameter**
```
POST {{base_url}}/api/analytics/forecast
Headers:
  Authorization: Bearer {{access_token}}
  Content-Type: application/json
Body:
{
  "budget_limit": 3000,
  "target_month": "2025-04-01",
  "categories": ["Travel"]
}

Expected Response: 200 OK
```

**Step 2: Verify response**
```json
{
  "success": true,
  "data": [...],
  "budget_saved": false
}
```

**Step 3: Verify in database**
```sql
SELECT * FROM budgets 
WHERE profile_id = 'your_profile_id' 
  AND category_name = 'Travel'
  AND budget_month = '2025-04-01';
```

**Expected:** No records found

**Verify:**
- ✓ Response has `budget_saved: false`
- ✓ No new budgets in database
- ✓ Forecast calculation still works

---

## Test Case 3: Update Existing Budget

### Objective
Verify that existing budgets are updated when saving with same category and month.

### Steps

**Step 1: Save initial budget**
```
POST {{base_url}}/api/analytics/forecast
Body:
{
  "budget_limit": 5000,
  "target_month": "2025-03-01",
  "categories": ["Food"],
  "save_budget": true
}
```

**Step 2: Save again with different budget_limit**
```
POST {{base_url}}/api/analytics/forecast
Body:
{
  "budget_limit": 7000,
  "target_month": "2025-03-01",
  "categories": ["Food"],
  "save_budget": true
}
```

**Step 3: Verify in database**
```sql
SELECT * FROM budgets 
WHERE profile_id = 'your_profile_id' 
  AND category_name = 'Food'
  AND budget_month = '2025-03-01';
```

**Expected:**
- Only 1 record (not 2)
- budget_limit = 7000.00 (updated)
- updated_at timestamp changed

**Verify:**
- ✓ No duplicate budgets created
- ✓ Budget limit updated to new value
- ✓ updated_at timestamp reflects change

---

## Test Case 4: Get All Budgets

### Objective
Verify that saved budgets can be retrieved.

### Steps

**Step 1: Get all budgets for user**
```
GET {{base_url}}/api/budgets/
Headers:
  Authorization: Bearer {{access_token}}

Expected Response: 200 OK
```

**Step 2: Verify response**
```json
{
  "success": true,
  "data": [
    {
      "budget_id": "uuid-here",
      "category_name": "Food",
      "budget_limit": 5000.00,
      "budget_month": "2025-03-01",
      "created_at": "2025-01-15 10:30:00",
      "updated_at": "2025-01-15 10:30:00"
    },
    {
      "budget_id": "uuid-here",
      "category_name": "Shopping",
      "budget_limit": 5000.00,
      "budget_month": "2025-03-01",
      "created_at": "2025-01-15 10:30:00",
      "updated_at": "2025-01-15 10:30:00"
    }
  ]
}
```

**Postman:** Use "Get All Budgets" request

**Verify:**
- ✓ All saved budgets returned
- ✓ Sorted by budget_month DESC
- ✓ All fields present

---

## Test Case 5: Get Budget by Category

### Objective
Verify that budgets can be retrieved for specific category.

### Steps

**Step 1: Get budget for specific category**
```
GET {{base_url}}/api/budgets/Food
Headers:
  Authorization: Bearer {{access_token}}

Expected Response: 200 OK
```

**Step 2: Verify response**
```json
{
  "success": true,
  "data": {
    "budget_id": "uuid-here",
    "category_name": "Food",
    "budget_limit": 5000.00,
    "budget_month": "2025-03-01",
    "created_at": "2025-01-15 10:30:00",
    "updated_at": "2025-01-15 10:30:00"
  }
}
```

**Postman:** Use "Get Budget by Category" request

**Verify:**
- ✓ Correct category returned
- ✓ Single budget object (not array)

---

## Test Case 6: Get Budget by Category and Month

### Objective
Verify that budgets can be filtered by category and month.

### Steps

**Step 1: Get budget for specific category and month**
```
GET {{base_url}}/api/budgets/Food?budget_month=2025-03-01
Headers:
  Authorization: Bearer {{access_token}}

Expected Response: 200 OK
```

**Step 2: Verify response returns correct budget**

**Postman:** Use "Get Budget by Category" request with query parameter

**Verify:**
- ✓ Correct category and month returned
- ✓ Query parameter filtering works

---

## Test Case 7: Delete Budget

### Objective
Verify that budgets can be deleted.

### Steps

**Step 1: Get budget_id from previous test**
```
GET {{base_url}}/api/budgets/
Save budget_id from response
```

**Step 2: Delete budget**
```
DELETE {{base_url}}/api/budgets/{{budget_id}}
Headers:
  Authorization: Bearer {{access_token}}

Expected Response: 200 OK
```

**Step 3: Verify response**
```json
{
  "success": true,
  "message": "Budget deleted successfully"
}
```

**Step 4: Verify in database**
```sql
SELECT * FROM budgets WHERE budget_id = 'deleted_budget_id';
```

**Expected:** No records found

**Postman:** Use "Delete Budget" request

**Verify:**
- ✓ Budget deleted from database
- ✓ Success message returned

---

## Test Case 8: Error - Budget Not Found

### Objective
Verify error handling when budget doesn't exist.

### Steps

**Step 1: Get non-existent budget**
```
GET {{base_url}}/api/budgets/NonExistentCategory
Headers:
  Authorization: Bearer {{access_token}}

Expected Response: 404 Not Found
```

**Step 2: Verify error response**
```json
{
  "success": false,
  "error": "Budget not found"
}
```

**Verify:**
- ✓ Status is 404
- ✓ Error message is clear

---

## Test Case 9: Error - Delete Non-Existent Budget

### Objective
Verify error handling when deleting non-existent budget.

### Steps

**Step 1: Delete with invalid budget_id**
```
DELETE {{base_url}}/api/budgets/invalid-uuid
Headers:
  Authorization: Bearer {{access_token}}

Expected Response: 404 Not Found
```

**Step 2: Verify error response**
```json
{
  "success": false,
  "error": "Budget not found"
}
```

**Verify:**
- ✓ Status is 404
- ✓ No database changes

---

## Complete Testing Workflow

### Full Flow Test:

1. **Login** → Get access_token
2. **Forecast with save_budget: true** → Budgets saved
3. **Get All Budgets** → Verify budgets exist
4. **Get Budget by Category** → Verify specific budget
5. **Forecast again with different limit** → Budget updated
6. **Get Budget by Category** → Verify update
7. **Delete Budget** → Budget removed
8. **Get All Budgets** → Verify deletion

---

## Database Verification Queries

### Check all budgets for user:
```sql
SELECT * FROM budgets 
WHERE profile_id = 'your_profile_id'
ORDER BY budget_month DESC, category_name;
```

### Check specific budget:
```sql
SELECT * FROM budgets 
WHERE profile_id = 'your_profile_id'
  AND category_name = 'Food'
  AND budget_month = '2025-03-01';
```

### Count budgets:
```sql
SELECT COUNT(*) FROM budgets 
WHERE profile_id = 'your_profile_id';
```

---

## Expected Results Summary

| Test Case | Expected Status | Expected Behavior |
|-----------|----------------|-------------------|
| Forecast with save | 200 OK | Budgets saved, budget_saved: true |
| Forecast without save | 200 OK | No budgets saved, budget_saved: false |
| Update existing | 200 OK | Budget updated, no duplicates |
| Get all budgets | 200 OK | Returns all user budgets |
| Get by category | 200 OK | Returns specific budget |
| Get by category + month | 200 OK | Returns filtered budget |
| Delete budget | 200 OK | Budget removed from database |
| Budget not found | 404 Not Found | Error message returned |
| Delete non-existent | 404 Not Found | Error message returned |

---

## Notes

- `save_budget` parameter is optional (defaults to false)
- Budgets are saved per category per month
- Duplicate budgets (same profile, category, month) are updated, not duplicated
- All budget endpoints require JWT authentication
- Budget month must be in YYYY-MM-DD format
- Budget limit must be greater than 0
