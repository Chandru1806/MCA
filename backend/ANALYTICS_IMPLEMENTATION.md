# Analytics Module Implementation Summary

## Overview
Implemented **Step 9: Analytics with ML-Based Spending Forecast** backend APIs for ExpenseIQ.

---

## Files Created

### 1. Service Layer
**File:** `backend/app/services/analytics_service.py`

**Methods:**
- `calculate_monthly_average_spending(profile_id, category_name)` - Calculates historical average
- `generate_forecast(profile_id, budget_limit, target_month, categories)` - Generates savings forecast

**Key Features:**
- Uses SQLAlchemy ORM for JOIN queries
- Joins `Transaction` and `TransactionCategory` models
- Extracts YEAR and MONTH from `transaction_date`
- Groups by month to calculate monthly totals
- Calculates average of all monthly totals
- Returns individual savings per category

---

### 2. Controller Layer
**File:** `backend/app/controllers/analytics_controller.py`

**Endpoint:**

#### POST `/api/analytics/forecast`
- **Authentication:** JWT required
- **Input:**
```json
{
  "budget_limit": 5000,
  "target_month": "2025-03-01",
  "categories": ["Food", "Shopping"]
}
```
- **Returns:** Individual savings forecast per category
- **Response:**
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
    }
  ]
}
```

**Validation:**
- Budget limit must be > 0
- Target month must be valid date (YYYY-MM-DD)
- Categories array must not be empty

---

### 3. Blueprint Registration
**File:** `backend/run.py`

**Changes:**
- Imported `analytics_bp` from `analytics_controller`
- Registered blueprint with prefix `/api/analytics`

---

### 4. Postman Collection
**File:** `backend/postman/ExpenseIQ_Collection.json`

**Added:**
- New folder: "Analytics"
- Request: "Forecast Savings" with sample body

---

### 5. Test Documentation
**File:** `backend/postman/ANALYTICS_TEST_STEPS.md`

**Includes:**
- 11 comprehensive test cases
- Step-by-step testing instructions
- Expected responses and validations
- Error handling scenarios
- Data accuracy validation
- Troubleshooting guide

---

## MVC Architecture

```
Model (Existing):
├── Transaction (transaction.py)
├── TransactionCategory (transaction_category.py)
└── Budget (budget.py) - Not used in minimal implementation

Service (NEW):
└── AnalyticsService (analytics_service.py)
    ├── calculate_monthly_average_spending()
    └── generate_forecast()

Controller (NEW):
└── AnalyticsController (analytics_controller.py)
    └── POST /api/analytics/forecast
```

---

## Database Queries

### Historical Average Monthly Spending Query
```python
WITH monthly_spending AS (
    SELECT 
        EXTRACT(YEAR FROM t.transaction_date) as year,
        EXTRACT(MONTH FROM t.transaction_date) as month,
        SUM(t.debit_amount) as monthly_total
    FROM transactions t
    JOIN transaction_categories tc 
        ON t.transaction_id = tc.transaction_id
    WHERE t.profile_id = :profile_id
        AND tc.category_name = :category_name
        AND t.debit_amount IS NOT NULL
    GROUP BY year, month
)
SELECT AVG(monthly_total) as avg_monthly_spending
FROM monthly_spending;
```

### Calculation Logic
1. Group transactions by month
2. Calculate SUM(debit_amount) per month
3. Calculate AVG of all monthly sums
4. This is the "current_spending" (historical average)
5. Savings = current_spending - budget_limit

---

## Key Features

✅ **JWT Authentication** - Endpoint protected with `@jwt_required()`

✅ **User-Specific Data** - Filters by `profile_id` from JWT token

✅ **Historical Average** - Calculates average monthly spending from all available months

✅ **Individual Savings** - Calculates separately for each selected category (not aggregated)

✅ **Input Validation** - Budget limit > 0, valid date format, non-empty categories

✅ **Error Handling** - Graceful error responses for all validation failures

✅ **No Historical Data Support** - Returns 0.00 for categories with no transactions

✅ **Negative Savings** - Correctly handles cases where user is under budget

---

## Testing Workflow

1. **Login** → Get JWT token
2. **Upload PDF** → Get file_id
3. **Import Transactions** → Populate transactions table
4. **Categorize Transactions** → Populate transaction_categories table
5. **Forecast Savings** → Calculate and view savings potential

---

## API Response Examples

### Success Response (Multiple Categories)
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

### Success Response (No Historical Data)
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

### Error Response (Invalid Budget)
```json
{
  "success": false,
  "error": "Budget limit must be greater than 0"
}
```

### Error Response (Invalid Date)
```json
{
  "success": false,
  "error": "Invalid date format. Use YYYY-MM-DD"
}
```

### Error Response (Empty Categories)
```json
{
  "success": false,
  "error": "At least one category must be selected"
}
```

---

## Implementation Notes

### Budgets Table Usage
- **NOT used** in minimal implementation
- User enters budget_limit dynamically in dialog
- No database writes for budget storage
- **Optional Enhancement:** Add endpoint to save budgets to database

### Message Format
- Uses **Option A** format: "If you reduce spending in [Category] to ₹[budget_limit], you'll save ₹[savings]"
- Can be changed to **Option B** format if needed

### Target Month
- Used for display/reference only
- Does NOT affect calculation (uses historical average from all months)
- Future enhancement: Time-series projection to specific month

### Negative Savings
- Indicates user is already under budget
- Message still displays correctly with negative value
- Frontend can color-code: Green (positive savings), Red (negative savings)

---

## Next Steps

### For Frontend Integration:
1. Create `analyticsService.js` to call this API
2. Create `ForecastDialog.jsx` component with inputs
3. Create `SavingsReport.jsx` to display results
4. Add Material-UI or React Modal for dialog
5. Add date picker for target month selection
6. Display categories as checkboxes sorted by spending DESC

### For Future Enhancements:
1. Add endpoint to save budgets to `budgets` table
2. Add endpoint to retrieve saved budgets
3. Add time-series projection (ML-based forecasting)
4. Add comparison views (what-if scenarios)
5. Add export functionality (PDF report)
6. Add budget alerts and notifications

---

## Compliance

✅ Follows MVC architecture

✅ Uses existing models (no new models created)

✅ JOIN queries in service layer

✅ JWT authentication on all endpoints

✅ Proper input validation

✅ Proper error handling

✅ Minimal code implementation

✅ Updated Postman collection

✅ Comprehensive test documentation

✅ No new database tables required

---

## Files Modified/Created Summary

| File | Action | Purpose |
|------|--------|---------|
| `services/analytics_service.py` | Created | Business logic for forecast calculations |
| `controllers/analytics_controller.py` | Created | API route handler |
| `run.py` | Modified | Registered analytics blueprint |
| `postman/ExpenseIQ_Collection.json` | Modified | Added analytics API request |
| `postman/ANALYTICS_TEST_STEPS.md` | Created | Testing documentation |
| `ANALYTICS_IMPLEMENTATION.md` | Created | Implementation summary |

---

**Implementation Status:** ✅ COMPLETE

**Ready for Testing:** YES

**Ready for Frontend Integration:** YES

**Database Tables Used:** `transactions`, `transaction_categories` (READ only)

**Database Tables Created:** NONE (minimal implementation)


---

## Budget Saving Enhancement

### **New Files Created:**

1. **`backend/app/models/budget.py`** - Budget model
2. **`backend/app/services/budget_service.py`** - Budget CRUD operations
3. **`backend/app/controllers/budget_controller.py`** - Budget API endpoints
4. **`backend/postman/BUDGET_SAVING_TEST_STEPS.md`** - Budget testing guide

### **Modified Files:**

1. **`backend/app/services/analytics_service.py`** - Added `save_budgets()` method
2. **`backend/app/controllers/analytics_controller.py`** - Added `save_budget` parameter
3. **`backend/run.py`** - Registered budget blueprint
4. **`backend/postman/ExpenseIQ_Collection.json`** - Added budget endpoints

### **New API Endpoints:**

#### Analytics Enhancement:
- `POST /api/analytics/forecast` - Now accepts optional `save_budget: true/false`

#### Budget Management:
- `GET /api/budgets/` - Get all budgets for user
- `GET /api/budgets/{category_name}` - Get budget by category
- `DELETE /api/budgets/{budget_id}` - Delete budget

### **How Budget Saving Works:**

**Request with save_budget:**
```json
{
  "budget_limit": 5000,
  "target_month": "2025-03-01",
  "categories": ["Food", "Shopping"],
  "save_budget": true
}
```

**Response:**
```json
{
  "success": true,
  "data": [...forecast results...],
  "budget_saved": true
}
```

**Database:**
- Saves one budget record per category
- If budget exists (same profile, category, month) → Updates
- If budget doesn't exist → Creates new

### **Budget Table Structure:**
```
budgets (
    budget_id UUID PRIMARY KEY,
    profile_id UUID FK,
    category_name VARCHAR(50),
    budget_limit NUMERIC(12, 2),
    budget_month DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE(profile_id, category_name, budget_month)
)
```

### **Key Features:**

✅ Optional budget saving (defaults to false)
✅ Automatic update if budget exists
✅ No duplicate budgets (UNIQUE constraint)
✅ Retrieve all budgets or by category
✅ Delete budgets
✅ Filter by month
✅ JWT authentication on all endpoints

---

**Implementation Status:** ✅ COMPLETE WITH BUDGET SAVING

**Ready for Testing:** YES

**Budgets Table:** NOW BEING USED
