Methodology for ExpenseIQ: Smart Personal Expense and Budget Advisor

Step 1: Data Ingestion & Bank Detection
User uploads a PDF bank statement.

System extracts text from the first 2 pages using pdfplumber.

Bank detection module scans headers using regex patterns to identify the issuing bank.

Supported banks: SBI, HDFC, ICICI, KOTAK.

Returns: Bank name or "UNKNOWN" if unrecognized.

Step 2: Transaction Extraction & Bank-Specific Parsing
System extracts transaction tables from the PDF using table detection.

For each supported bank, applies bank-specific column mapping rules:

SBI → Maps columns to standard schema

HDFC → Maps columns to standard schema

ICICI → Maps columns to standard schema

KOTAK → Maps columns to standard schema

Splits extracted data into standardized transactions and rejected rows (validation failures).

Step 3: Data Standardization & Schema Normalization
Converts all transactions to a common schema:

Transaction_ID | Transaction_Date | Description | Debit_Amount | Credit_Amount | Balance | Bank_Name

Copy

Insert at cursor
Cleans descriptions by removing:

Trailing dates, amounts, and system metadata

Bank address information

Special characters and extra whitespace

Formats numeric values:

Removes commas from amounts (e.g., "1,000" → 1000.00)

Converts to 2-decimal float format

Handles missing/invalid values gracefully

Generates unique Transaction_IDs for each row.

Step 4: Data Preprocessing & Validation
Data Type Normalization:
- Convert string values to floats using safe_float() function
- Remove commas from numeric strings (e.g., "1,000" → 1000.0)
- Handle invalid/missing values gracefully by returning None

Data Validation:
- Validate required columns: Debit_Amount, Credit_Amount, Balance
- Raise error if any required column is missing

Missing Data Imputation:
- Identify rows with missing Debit_Amount, Credit_Amount, or Balance
- Use balance-based inference: diff = previous_balance - next_balance
- Case 1 (debit in next row): inferred_debit = diff - next_debit
- Case 2 (credit in next row): inferred_credit = diff + next_credit
- Case 3 (fallback): inferred_debit = diff
- Only repair rows where surrounding balances are available

Output:
- Save repaired data to CSV with "_NORMALIZED" suffix
- Preserve original file unchanged

Step 5: Data Repair & Balance Validation
Identifies rows with missing Debit_Amount, Credit_Amount, or Balance.

Uses balance-based inference algorithm to repair missing values:

Calculates balance difference between surrounding rows

Reverse-engineers missing amounts based on transaction type (debit/credit)

Updates current row with inferred values

Maintains balance consistency throughout the statement

Limitation: Only repairs rows where surrounding balances are available.

Outputs repaired CSV with "_NORMALIZED" suffix.

Step 6: CSV Export & User Verification
System generates a raw CSV (no modifications to original data).

User downloads CSV → verifies accuracy → re-uploads for categorization.

Ensures transparency and allows manual correction before processing.

Step 7: Expense Categorization (Hybrid Model)
Rule-Based Classification (Priority 1):

Keyword matching against 10 master categories: Food, Shopping, Travel, Bills, Entertainment, Subscriptions, Health, Groceries, Education, Fuel

Special categories: ATM, Salary, Interest, Refund, Internal_Transfer, Person (P2P transfers)

Regex pattern matching for high-confidence patterns (FastTag, Hotels, Supermarkets, etc.)

Confidence scores: 0.85–0.95 for rule-based predictions

Machine Learning Classification (Priority 2):

Applied only if rule confidence < 0.90

Uses TF-IDF vectorization (max 2000 features, 1-3 n-grams)

Random Forest classifier (300 estimators, max depth 25)

ML confidence adjusted by 0.90 multiplier for conservative estimates

Final prediction uses ML only if (ML_confidence × 0.90) > rule_confidence

Merchant Extraction:

Isolates merchant name from transaction description

Enables person detection for P2P transfers (85 known names database)

Improves classification accuracy

Output: Each transaction now has:

Category (10 master + 7 special categories)

Confidence score (0.0–1.0)

Rule-based and ML predictions (if applicable)

Step 8: Real-Time Expense Tracking Dashboard
Create a dashboard that displays spending by category. The system should:

Aggregate all transactions grouped by category and sum their amounts

Display categories sorted in descending order by total spending

Show category-wise spending totals and spending trends over time on a visual dashboard

Step 9: Analytics with ML-Based Spending Forecast:

Create an analytics feature with a "Next" button that opens a dialog. Users can:

Enter a budget limit amount (in ₹)

Select a future month for projection

Select one or more categories via checkboxes (displayed in descending order by spending)

For each selected category, generate a savings report showing:

Option A: "If you reduce spending in [Category] to ₹[budget_limit], you'll save ₹[current_spending - budget_limit]"

Option B: "Your current spending in [Category] is ₹[current_spending]. Budget limit is ₹[budget_limit]. Savings potential: ₹[current_spending - budget_limit]"

The system should:

Calculate savings individually for each selected category (not aggregated)

Project current spending patterns to the selected future month using historical average monthly spending

Display the savings report for all selected categories.


What else has to be added on the tech stack? Could you add and and explain for adding

TECH-STACK:
BackEnd:

Python Flask, SQLAlchemy (ORM),Flask-JWT-Extended (Authentication), Flask-CORS (API Communication), pdfplumber (PDF Processing), pandas (Data Manipulation), python-dotenv (Environment Management), psycopg2 (PostgreSQL Adapter), Alembic (Database Migrations), pytest (Testing)

FrontEnd:

React

Axios (API Communication), Redux or Zustand (State Management), React Query (Server State), Jest (Testing),

Database:

PostgreSQL , AWS RDS (Managed Database)

Deployment:

GitHub (Version Control), GitHub Actions (CI/CD), AWS Elastic Beanstalk (Application Hosting), AWS CloudWatch (Monitoring & Logging), AWS IAM (Access Management)

Security:

bcrypt (Password Hashing), AWS Secrets Manager (Credential Management)

Additional Tools:

Docker (Future Implementation)

Sentry (Error Tracking - Optional)

Format for thesis writing:

Format: 

| Item                  | Specification             |
| --------------------- | ------------------------- |
| Font type             | **Times New Roman**       |
| Main text size        | **12 pt**                 |
| Chapter headings      | **14 pt, Bold, ALL CAPS** |
| Sub-headings          | **12 pt, Bold**           |
| Line spacing          | **1.5 spacing**           |
| Paragraph alignment   | **Justified**             |
| Paragraph indentation | **First line – 0.5 inch** |