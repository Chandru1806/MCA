# ExpenseIQ API Endpoints

## Existing Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Home redirect |
| `/ingestion` | GET | Upload page |
| `/ingestion/upload` | POST | Process PDFs/CSVs |
| `/ingestion/preview` | GET | Preview standardized data |
| `/ingestion/download/<fname>` | GET | Download CSV files |
| `/repair` | GET/POST | Repair rejected transactions |
| `/preprocess_csv` | POST | Preprocess CSV data |

---

## New Endpoints to Create

### 1. Preprocessing & Validation

**POST `/api/preprocess`** - Normalize and validate transaction data
- Input: CSV file
- Output: Normalized CSV with validation report
- Handles: Data type conversion, missing value imputation, balance validation

**POST `/api/validate`** - Validate transaction integrity
- Input: CSV file
- Output: Validation errors/warnings
- Checks: Required columns, data types, balance consistency

---

### 2. Categorization

**POST `/api/categorize`** - Categorize transactions (hybrid model)
- Input: CSV with transactions
- Output: CSV with categories and confidence scores
- Uses: Rule-based + ML classification

**GET `/api/categories`** - Get all available categories
- Output: List of 10 master + 7 special categories

**POST `/api/train-model`** - Train/retrain ML categorizer
- Input: Labeled transaction data
- Output: Model performance metrics

---

### 3. Dashboard & Analytics

**GET `/api/dashboard`** - Real-time spending dashboard
- Output: Category-wise spending totals, trends
- Aggregates: All transactions grouped by category

**GET `/api/dashboard/category/<category>`** - Category-specific details
- Output: Transactions, spending trend, merchant breakdown

**POST `/api/analytics/forecast`** - ML-based spending forecast
- Input: Budget limit, future month, selected categories
- Output: Savings report per category

**GET `/api/analytics/trends`** - Historical spending trends
- Output: Monthly/weekly spending patterns by category

---

### 4. Transaction Management

**GET `/api/transactions`** - List all transactions (paginated)
- Query params: `page`, `limit`, `category`, `date_range`
- Output: Paginated transaction list

**GET `/api/transactions/<id>`** - Get single transaction details
- Output: Full transaction with category confidence

**PUT `/api/transactions/<id>`** - Update transaction category
- Input: New category, confidence override
- Output: Updated transaction

**DELETE `/api/transactions/<id>`** - Delete transaction
- Output: Success/error message

---

### 5. Budget Management

**POST `/api/budgets`** - Create budget for category
- Input: Category, limit amount, month
- Output: Budget ID

**GET `/api/budgets`** - List all budgets
- Output: Active budgets with status

**PUT `/api/budgets/<id>`** - Update budget
- Input: New limit, category
- Output: Updated budget

**DELETE `/api/budgets/<id>`** - Delete budget
- Output: Success message

**GET `/api/budgets/<id>/status`** - Check budget status
- Output: Current spending vs limit, savings potential

---

### 6. Reports

**GET `/api/reports/monthly`** - Monthly spending report
- Query params: `month`, `year`
- Output: Category breakdown, trends, insights

**GET `/api/reports/savings`** - Savings potential report
- Output: Categories with highest savings potential

**POST `/api/reports/export`** - Export report as PDF/Excel
- Input: Report type, date range
- Output: File download

---

### 7. User Management

**POST `/api/auth/register`** - User registration
- Input: Email, password
- Output: User ID, JWT token

**POST `/api/auth/login`** - User login
- Input: Email, password
- Output: JWT token

**POST `/api/auth/logout`** - User logout
- Output: Success message

**GET `/api/profile`** - Get user profile
- Output: User details, preferences

**PUT `/api/profile`** - Update user profile
- Input: Name, preferences
- Output: Updated profile

---

### 8. Bank Statement Management

**GET `/api/statements`** - List uploaded statements
- Output: Statement history with metadata

**POST `/api/statements/upload`** - Upload new statement
- Input: PDF file
- Output: Processing status, statement ID

**GET `/api/statements/<id>`** - Get statement details
- Output: Statement metadata, transaction count

**DELETE `/api/statements/<id>`** - Delete statement
- Output: Success message

---

### 9. Merchant Management

**GET `/api/merchants`** - List all merchants
- Query params: `category`, `search`
- Output: Merchant list with transaction count

**POST `/api/merchants/<id>/category`** - Set merchant category
- Input: Category
- Output: Updated merchant

---

### 10. Settings & Configuration

**GET `/api/settings`** - Get user settings
- Output: Preferences, notification settings

**PUT `/api/settings`** - Update settings
- Input: Settings object
- Output: Updated settings

**POST `/api/settings/export-data`** - Export all user data
- Output: ZIP file with all data

---

## Priority Implementation Order

### Phase 1 (Core)
- Categorization
- Dashboard
- Transactions

### Phase 2 (Analytics)
- Forecasting
- Reports
- Trends

### Phase 3 (Management)
- Budgets
- Statements
- Merchants

### Phase 4 (User)
- Auth
- Profile
- Settings
