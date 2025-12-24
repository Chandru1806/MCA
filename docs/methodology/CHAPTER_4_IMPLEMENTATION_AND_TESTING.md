# CHAPTER 4
# SYSTEM IMPLEMENTATION AND TESTING

## 4.1 Introduction

This chapter details the implementation of ExpenseIQ, a smart personal expense and budget advisor system. The implementation follows a modular architecture with distinct layers for backend processing, frontend presentation, and data management. The system processes PDF bank statements, extracts transactions, normalizes data, categorizes expenses using hybrid ML-based approach, and provides real-time analytics through an interactive dashboard.

---

## 4.2 Implementation Details

### 4.2.1 Backend Implementation (Flask & API Layer)

The backend is built using Python Flask framework with RESTful API endpoints for handling client requests. Key components include:

**Framework & Dependencies:**
- Flask: Lightweight web framework for routing and request handling
- Flask-JWT-Extended: Token-based authentication for secure API access
- Flask-CORS: Cross-Origin Resource Sharing for frontend-backend communication
- python-dotenv: Environment variable management for configuration

**API Endpoints:**
- `/api/upload` - Accepts PDF bank statements
- `/api/preview` - Returns extracted transaction preview
- `/api/categorize` - Triggers expense categorization
- `/api/dashboard` - Fetches aggregated spending data
- `/api/analytics` - Provides ML-based spending forecasts

**Authentication:**
- JWT tokens issued upon user login
- Token validation on protected endpoints
- Secure credential storage using bcrypt hashing

---

### 4.2.2 PDF Processing & Bank Detection Module

The ingestion module extracts transaction data from PDF bank statements and identifies the issuing bank.

**Bank Detection Process:**
- Scans first 2 pages of PDF using pdfplumber
- Applies regex patterns to identify bank headers
- Supported banks: SBI, HDFC, ICICI, KOTAK
- Returns bank name or "UNKNOWN" for unrecognized statements

**Transaction Extraction:**
- Detects transaction tables using table detection algorithms
- Applies bank-specific column mapping rules
- Handles variable table structures across different banks
- Extracts transaction metadata (date, description, amounts, balance)

**Key Implementation Files:**
- `modules/ingestion/detect.py` - Bank detection logic
- `modules/ingestion/extract.py` - Transaction table extraction
- `modules/ingestion/banks/` - Bank-specific column mappings

---

### 4.2.3 Data Standardization & Normalization

Converts extracted transactions into a unified schema for consistent processing.

**Standard Schema:**
```
Transaction_ID | Transaction_Date | Description | Debit_Amount | 
Credit_Amount | Balance | Bank_Name
```

**Normalization Steps:**
- Removes trailing dates, amounts, and system metadata from descriptions
- Strips bank address information and special characters
- Converts numeric values to 2-decimal float format
- Removes commas from amounts (e.g., "1,000" → 1000.00)
- Generates unique Transaction_IDs for each row

**Data Validation & Repair:**
- Validates required columns (Debit_Amount, Credit_Amount, Balance)
- Identifies rows with missing values
- Uses balance-based inference algorithm to repair missing amounts
- Maintains balance consistency throughout the statement
- Outputs repaired CSV with "_NORMALIZED" suffix

**Key Implementation Files:**
- `modules/ingestion/standardize.py` - Schema normalization
- `modules/ingestion/validator.py` - Data validation
- `modules/preprocessing/preprocess_csv.py` - Data cleaning
- `modules/repair/repair_rejects.py` - Missing value imputation

---

### 4.2.4 Expense Categorization (Hybrid ML Model)

Implements a two-tier categorization system combining rule-based and machine learning approaches.

**Rule-Based Classification (Priority 1):**
- Keyword matching against 10 master categories: Food, Shopping, Travel, Bills, Entertainment, Subscriptions, Health, Groceries, Education, Fuel
- Special categories: ATM, Salary, Interest, Refund, Internal_Transfer, Person (P2P transfers)
- Regex pattern matching for high-confidence patterns (FastTag, Hotels, Supermarkets)
- Confidence scores: 0.85–0.95 for rule-based predictions

**Machine Learning Classification (Priority 2):**
- Applied only if rule confidence < 0.90
- Uses TF-IDF vectorization (max 2000 features, 1-3 n-grams)
- Random Forest classifier (300 estimators, max depth 25)
- ML confidence adjusted by 0.90 multiplier for conservative estimates
- Final prediction uses ML only if (ML_confidence × 0.90) > rule_confidence

**Merchant Extraction:**
- Isolates merchant name from transaction description
- Enables person detection for P2P transfers (85 known names database)
- Improves classification accuracy

**Output:**
- Each transaction assigned: Category, Confidence score, Rule-based and ML predictions

**Key Implementation Files:**
- `dynamic_categorizer.py` - Hybrid categorization logic
- `optimized_categorizer.py` - Performance-optimized version
- `CATEGORY_MODEL_DEFINITION.txt` - Category definitions and rules

---

### 4.2.5 Frontend Implementation (React Dashboard)

Interactive user interface for uploading statements, viewing transactions, and analyzing spending patterns.

**Key Features:**
- PDF upload interface with drag-and-drop support
- Transaction preview with validation feedback
- Real-time expense tracking dashboard
- Category-wise spending visualization
- Analytics panel with budget forecasting

**Technology Stack:**
- React: Component-based UI framework
- Axios: HTTP client for API communication
- Redux/Zustand: State management for application state
- React Query: Server state management and caching
- Jest: Unit testing framework

**Dashboard Components:**
- Upload module: File handling and progress tracking
- Preview module: Transaction verification interface
- Dashboard module: Spending aggregation and visualization
- Analytics module: Budget planning and savings projection

---

### 4.2.6 Database Design & ORM Integration

Persistent storage of user data, transactions, and categorization results.

**Database Technology:**
- PostgreSQL: Relational database for structured data
- AWS RDS: Managed database service for scalability and reliability
- SQLAlchemy: Python ORM for database abstraction

**Key Tables:**
- Users: User account information and authentication
- Transactions: Normalized transaction records
- Categories: Expense category definitions
- Categorizations: Transaction-to-category mappings with confidence scores
- Budgets: User-defined budget limits and targets

**Database Migrations:**
- Alembic: Version control for database schema changes
- Enables rollback and forward migration capabilities
- Tracks schema evolution across deployments

**Key Implementation Files:**
- `DATABASE_SCHEMA.md` - Complete schema definition
- Database migration scripts in `alembic/` directory

---

## 4.3 System Testing

Comprehensive testing strategy covering multiple testing levels to ensure system reliability, security, and performance.

### 4.3.1 Unit Testing

Tests individual components in isolation to verify correct behavior.

**Scope:**
- Bank detection logic (regex patterns, edge cases)
- Data normalization functions (type conversion, formatting)
- Categorization rules (keyword matching, confidence scoring)
- Validation functions (schema compliance, data integrity)

**Tools & Framework:**
- pytest: Python testing framework
- Jest: JavaScript testing for React components
- Mock objects for external dependencies (database, APIs)

**Coverage Target:** Minimum 80% code coverage for critical modules

**Test Cases:**
- Valid input scenarios (standard bank statements)
- Edge cases (empty tables, malformed data)
- Error handling (invalid formats, missing fields)
- Boundary conditions (extreme values, special characters)

---

### 4.3.2 Integration Testing

Tests interactions between multiple components and modules.

**Scope:**
- PDF upload → Bank detection → Transaction extraction pipeline
- Data normalization → Validation → Database storage
- Transaction categorization → Dashboard aggregation
- API endpoints with database operations

**Test Scenarios:**
- End-to-end PDF processing workflow
- API request/response validation
- Database transaction consistency
- Authentication and authorization flows

**Tools:**
- pytest with fixtures for test data
- Postman/REST client for API testing
- Database test containers for isolated testing

---

### 4.3.3 System Testing

Tests complete system functionality against requirements.

**Scope:**
- Full workflow from PDF upload to analytics dashboard
- Multi-user concurrent access scenarios
- Data consistency across components
- Error recovery and graceful degradation

**Test Scenarios:**
- Upload multiple bank statements from different banks
- Verify transaction categorization accuracy
- Validate dashboard aggregations and calculations
- Test budget forecasting with historical data
- Verify data persistence and retrieval

**Tools:**
- Selenium: Automated browser testing for UI
- JMeter: Load testing for concurrent users
- Test data generators for realistic scenarios

---

### 4.3.4 Performance Testing

Evaluates system performance under various load conditions.

**Scope:**
- PDF processing speed (large statements with 1000+ transactions)
- API response times under concurrent requests
- Database query optimization
- Memory and CPU utilization

**Test Scenarios:**
- Process PDFs of varying sizes (10 KB to 10 MB)
- Simulate 100+ concurrent users uploading statements
- Query dashboard with 1 year of transaction history
- Categorization performance on large datasets

**Metrics:**
- Response time (p50, p95, p99 percentiles)
- Throughput (requests per second)
- Resource utilization (CPU, memory, disk I/O)
- Database query execution time

**Tools:**
- JMeter: Load and stress testing
- AWS CloudWatch: Performance monitoring
- Python profilers: Code-level performance analysis

---

### 4.3.5 Security Testing

Validates security controls and identifies vulnerabilities.

**Scope:**
- Authentication and authorization mechanisms
- Input validation and injection attack prevention
- Sensitive data protection (encryption, hashing)
- API security (CORS, rate limiting)
- Database security (SQL injection prevention)

**Test Scenarios:**
- SQL injection attempts in transaction descriptions
- XSS attacks in UI components
- Unauthorized API access without valid JWT tokens
- Password strength validation
- Sensitive data exposure in logs/error messages

**Tools:**
- OWASP ZAP: Automated security scanning
- Burp Suite: Manual penetration testing
- Bandit: Python security linter
- npm audit: JavaScript dependency vulnerability scanning

**Security Checklist:**
- Credentials stored securely (bcrypt hashing, AWS Secrets Manager)
- HTTPS/TLS for all communications
- CORS properly configured
- Rate limiting on API endpoints
- Input sanitization on all user inputs

---

### 4.3.6 User Acceptance Testing (UAT)

Validates system meets business requirements and user expectations.

**Scope:**
- Usability of upload and preview interfaces
- Accuracy of expense categorization
- Dashboard clarity and usefulness
- Analytics and forecasting relevance
- Overall user experience

**Test Scenarios:**
- End users upload real bank statements
- Verify categorization matches user expectations
- Test budget planning workflow
- Validate savings projections accuracy
- Gather feedback on UI/UX

**Participants:**
- Target users (personal finance managers)
- Business stakeholders
- Product owners

**Success Criteria:**
- 90%+ categorization accuracy
- Dashboard loads within 2 seconds
- Users can complete workflows without assistance
- Positive feedback on usability

---

### 4.3.7 Regression Testing

Ensures new changes don't break existing functionality.

**Scope:**
- Re-run all unit and integration tests after code changes
- Verify previously fixed bugs remain fixed
- Test backward compatibility with old data formats

**Automation:**
- CI/CD pipeline (GitHub Actions) runs tests on every commit
- Automated test suite execution before deployment
- Failed tests block deployment to production

---

## 4.4 Testing Tools & Infrastructure

**Testing Framework:**
- pytest (Python backend)
- Jest (React frontend)
- Selenium (UI automation)

**Performance & Load Testing:**
- Apache JMeter
- AWS CloudWatch

**Security Testing:**
- OWASP ZAP
- Bandit (Python)
- npm audit (JavaScript)

**CI/CD Pipeline:**
- GitHub Actions for automated testing
- Docker containers for test environment consistency

**Monitoring & Logging:**
- AWS CloudWatch for production monitoring
- Sentry for error tracking and alerting

---

## 4.5 Deployment Strategy

**Deployment Pipeline:**
1. Code commit to GitHub
2. GitHub Actions triggers automated tests
3. Tests pass → Build Docker image
4. Push to AWS ECR (Elastic Container Registry)
5. Deploy to AWS Elastic Beanstalk
6. Health checks and smoke tests
7. Monitor with CloudWatch and Sentry

**Rollback Plan:**
- Maintain previous version in Elastic Beanstalk
- Automatic rollback on health check failures
- Database migrations tracked with Alembic for easy rollback

---
