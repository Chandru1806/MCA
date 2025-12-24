# ExpenseIQ - System Architecture

## Complete System Flow Architecture

```mermaid
graph TB
    subgraph Frontend["🎨 Frontend Layer (React)"]
        Logo["Logo"]
        Login["Login Page"]
        Signup["Signup Page"]
        Dashboard["Dashboard"]
        UploadPDF["Upload PDF Module"]
        Preprocessing["Preprocessing Module"]
        Category["Categorization Module"]
        BudgetAdvisor["Budget Advisor Module"]
    end

    subgraph Auth["🔐 Authentication Layer (Flask-JWT-Extended)"]
        SignupHandler["Signup Handler"]
        LoginHandler["Login Handler"]
        TokenGen["JWT Token Generation"]
        TokenRefresh["Refresh Token Mechanism"]
        SessionTimeout["Session Timeout Enforcement"]
        TokenValidation["Token Validation Middleware"]
    end

    subgraph Backend["⚙️ Backend Layer (Python Flask)"]
        UserService["User Service"]
        BankDetection["Bank Detection Module"]
        TransactionExtraction["Transaction Extraction"]
        DataNormalization["Data Normalization"]
        DataRepair["Data Repair & Validation"]
        RuleBasedCategorization["Rule-Based Categorization"]
        MLCategorization["ML Categorization"]
        DashboardService["Dashboard Service"]
        BudgetService["Budget Service"]
        AuditService["Audit Service"]
    end

    subgraph Processing["📊 Data Processing Pipeline"]
        Step1["Step 1: PDF Ingestion & Bank Detection"]
        Step2["Step 2: Transaction Extraction"]
        Step3["Step 3: Data Standardization"]
        Step4["Step 4: Data Preprocessing & Validation"]
        Step5["Step 5: Data Repair & Balance Validation"]
        Step6["Step 6: CSV Export & Verification"]
        Step7["Step 7: Expense Categorization"]
        Step8["Step 8: Real-Time Dashboard"]
        Step9["Step 9: Analytics & ML Forecast"]
    end

    subgraph Database["🗄️ Database Layer (PostgreSQL)"]
        UsersTable["users Table<br/>profile_id, username, password_hash"]
        BankStatementsTable["bank_statements Table<br/>statement_id, profile_id, bank_name"]
        TransactionsTable["transactions Table<br/>transaction_id, debit_amount, credit_amount"]
        CategoriesTable["transaction_categories Table<br/>category_id, confidence_score"]
        BudgetsTable["budgets Table<br/>budget_id, budget_limit"]
        AuditLogsTable["audit_logs Table<br/>log_id, action, old_values, new_values"]
    end

    subgraph Storage["☁️ Cloud Storage (AWS)"]
        S3PDFs["AWS S3: PDF Files"]
        S3CSVs["AWS S3: CSV Files"]
        RDS["AWS RDS: PostgreSQL"]
        SecretsManager["AWS Secrets Manager"]
    end

    subgraph Monitoring["📈 Monitoring & Logging"]
        CloudWatch["AWS CloudWatch"]
        Sentry["Sentry Error Tracking"]
        AuditLogs["Audit Logs"]
    end

    subgraph DevOps["🚀 DevOps & Deployment"]
        GitHub["GitHub Repository"]
        GitHubActions["GitHub Actions CI/CD"]
        Docker["Docker Containers"]
        ElasticBeanstalk["AWS Elastic Beanstalk"]
    end

    %% Frontend Flow
    Logo --> Login
    Login -->|New User| Signup
    Login -->|Existing User| Dashboard
    Signup --> Dashboard
    
    %% Authentication Flow
    Signup --> SignupHandler
    Login --> LoginHandler
    SignupHandler --> TokenGen
    LoginHandler --> TokenGen
    TokenGen --> TokenRefresh
    TokenRefresh --> SessionTimeout
    TokenValidation -.->|Middleware| Dashboard
    TokenValidation -.->|Middleware| UploadPDF
    
    %% Dashboard Navigation
    Dashboard --> UploadPDF
    Dashboard --> Preprocessing
    Dashboard --> Category
    Dashboard --> BudgetAdvisor
    
    %% User Management
    SignupHandler --> UserService
    LoginHandler --> UserService
    UserService --> UsersTable
    
    %% Upload PDF Flow
    UploadPDF --> Step1
    Step1 --> BankDetection
    BankDetection --> BankStatementsTable
    
    %% Processing Pipeline
    Step1 --> Step2
    Step2 --> TransactionExtraction
    TransactionExtraction --> Step3
    Step3 --> DataNormalization
    DataNormalization --> Step4
    Step4 --> DataRepair
    DataRepair --> Step5
    Step5 --> Step6
    Step6 --> TransactionsTable
    
    %% Preprocessing Module
    Preprocessing --> Step4
    Preprocessing --> Step5
    Preprocessing --> Step6
    
    %% Categorization Flow
    Category --> Step7
    Step7 --> RuleBasedCategorization
    RuleBasedCategorization --> MLCategorization
    MLCategorization --> CategoriesTable
    
    %% Dashboard Analytics
    Dashboard --> Step8
    Step8 --> DashboardService
    DashboardService --> TransactionsTable
    DashboardService --> CategoriesTable
    
    %% Budget Advisor
    BudgetAdvisor --> Step9
    Step9 --> BudgetService
    BudgetService --> BudgetsTable
    BudgetService --> TransactionsTable
    
    %% Database Relationships
    UsersTable --> BankStatementsTable
    BankStatementsTable --> TransactionsTable
    TransactionsTable --> CategoriesTable
    UsersTable --> BudgetsTable
    UsersTable --> AuditLogsTable
    
    %% Audit Trail
    UserService --> AuditService
    BankDetection --> AuditService
    TransactionExtraction --> AuditService
    RuleBasedCategorization --> AuditService
    MLCategorization --> AuditService
    BudgetService --> AuditService
    AuditService --> AuditLogsTable
    
    %% Storage Integration
    BankDetection --> S3PDFs
    DataNormalization --> S3CSVs
    TransactionExtraction --> S3CSVs
    UsersTable -.->|Encrypted| SecretsManager
    
    %% Monitoring
    Backend --> CloudWatch
    Backend --> Sentry
    AuditService --> AuditLogs
    
    %% DevOps Pipeline
    GitHub --> GitHubActions
    GitHubActions --> Docker
    Docker --> ElasticBeanstalk
    ElasticBeanstalk --> Backend
    ElasticBeanstalk --> RDS
    
    style Frontend fill:#e1f5ff
    style Auth fill:#fff3e0
    style Backend fill:#f3e5f5
    style Processing fill:#e8f5e9
    style Database fill:#fce4ec
    style Storage fill:#fff9c4
    style Monitoring fill:#f1f8e9
    style DevOps fill:#ede7f6
```

---

## Authentication & Session Flow

```mermaid
sequenceDiagram
    participant User as User
    participant Frontend as React Frontend
    participant Auth as Auth Service
    participant Backend as Flask Backend
    participant DB as PostgreSQL
    participant JWT as JWT Handler

    User->>Frontend: Click Signup
    Frontend->>Auth: POST /auth/signup (credentials)
    Auth->>Backend: Validate input
    Backend->>DB: Check username/email exists
    DB-->>Backend: Not found
    Backend->>Backend: Hash password with bcrypt
    Backend->>DB: INSERT into users (profile_id, username, password_hash)
    DB-->>Backend: User created (profile_id: UUID)
    Backend->>JWT: Generate JWT token
    JWT-->>Backend: Access token + Refresh token
    Backend-->>Auth: Return tokens
    Auth-->>Frontend: Store tokens (localStorage/sessionStorage)
    Frontend-->>User: Redirect to Dashboard

    User->>Frontend: Click Login
    Frontend->>Auth: POST /auth/login (username, password)
    Auth->>Backend: Validate credentials
    Backend->>DB: SELECT user by username
    DB-->>Backend: User found
    Backend->>Backend: Compare password hash
    Backend->>JWT: Generate JWT token
    JWT-->>Backend: Access token + Refresh token
    Backend-->>Auth: Return tokens
    Auth-->>Frontend: Store tokens
    Frontend-->>User: Redirect to Dashboard

    Frontend->>Backend: API request with token
    Backend->>JWT: Validate token
    JWT-->>Backend: Token valid
    Backend-->>Frontend: Process request
    
    Note over JWT: Token expires after 15 min
    Frontend->>Backend: POST /auth/refresh (refresh_token)
    Backend->>JWT: Validate refresh token
    JWT-->>Backend: Valid
    Backend->>JWT: Generate new access token
    JWT-->>Backend: New access token
    Backend-->>Frontend: Return new token
    Frontend->>Frontend: Update token in storage
```

---

## Data Processing Pipeline Flow

```mermaid
graph LR
    A["📄 PDF Upload"] --> B["🔍 Bank Detection<br/>SBI/HDFC/ICICI/KOTAK"]
    B --> C["📊 Transaction Extraction<br/>Table Detection"]
    C --> D["🔄 Data Standardization<br/>Common Schema"]
    D --> E["✅ Data Validation<br/>Type Normalization"]
    E --> F["🔧 Data Repair<br/>Balance Inference"]
    F --> G["💾 CSV Export<br/>_NORMALIZED suffix"]
    G --> H["👤 User Verification<br/>Manual Review"]
    H --> I["🏷️ Categorization<br/>Rule-Based + ML"]
    I --> J["📈 Dashboard<br/>Spending Analytics"]
    J --> K["💰 Budget Advisor<br/>Savings Forecast"]
    
    B -.->|bank_statements| DB1["DB: bank_name"]
    C -.->|transactions| DB2["DB: raw data"]
    D -.->|normalized| DB3["DB: standardized"]
    F -.->|repaired| DB4["DB: is_repaired flag"]
    I -.->|categories| DB5["DB: category_name<br/>confidence_score"]
    
    style A fill:#bbdefb
    style B fill:#c8e6c9
    style C fill:#fff9c4
    style D fill:#ffe0b2
    style E fill:#f8bbd0
    style F fill:#e1bee7
    style G fill:#b2dfdb
    style H fill:#ffccbc
    style I fill:#c5cae9
    style J fill:#b3e5fc
    style K fill:#dcedc8
```

---

## Dashboard Module Architecture

```mermaid
graph TB
    Dashboard["🎯 Dashboard"]
    
    Dashboard --> Box1["📤 Upload PDF<br/>Square 1"]
    Dashboard --> Box2["⚙️ Preprocessing<br/>Square 2"]
    Dashboard --> Box3["🏷️ Categorization<br/>Square 3"]
    Dashboard --> Box4["💰 Budget Advisor<br/>Square 4"]
    
    Box1 --> Upload["Upload PDF File"]
    Upload --> Detect["Detect Bank"]
    Detect --> Extract["Extract Transactions"]
    Extract --> Store["Store in DB"]
    
    Box2 --> Validate["Validate Data"]
    Validate --> Repair["Repair Missing Values"]
    Repair --> Normalize["Normalize Schema"]
    Normalize --> Export["Export CSV"]
    
    Box3 --> Rules["Apply Rule-Based<br/>Classification"]
    Rules --> ML["Apply ML Model"]
    ML --> Confidence["Calculate Confidence"]
    Confidence --> Assign["Assign Categories"]
    
    Box4 --> Analyze["Analyze Spending"]
    Analyze --> Budget["Set Budget Limits"]
    Budget --> Forecast["Project Future Spending"]
    Forecast --> Report["Generate Savings Report"]
    
    style Dashboard fill:#e3f2fd
    style Box1 fill:#c8e6c9
    style Box2 fill:#fff9c4
    style Box3 fill:#ffe0b2
    style Box4 fill:#f8bbd0
```

---

## Database Schema Relationships

```mermaid
erDiagram
    USERS ||--o{ BANK_STATEMENTS : uploads
    USERS ||--o{ TRANSACTIONS : has
    USERS ||--o{ TRANSACTION_CATEGORIES : categorizes
    USERS ||--o{ BUDGETS : sets
    USERS ||--o{ AUDIT_LOGS : generates
    BANK_STATEMENTS ||--o{ TRANSACTIONS : contains

    USERS {
        uuid profile_id PK
        string username UK
        string password_hash
        string email UK
        timestamp created_at
    }

    BANK_STATEMENTS {
        uuid statement_id PK
        uuid profile_id FK
        string bank_name
        string processing_status
    }

    TRANSACTIONS {
        uuid transaction_id PK
        uuid profile_id FK
        uuid statement_id FK
        date transaction_date
        decimal debit_amount
        decimal credit_amount
        decimal balance
    }

    TRANSACTION_CATEGORIES {
        uuid category_id PK
        uuid transaction_id FK
        string category_name
        decimal confidence_score
    }

    BUDGETS {
        uuid budget_id PK
        uuid profile_id FK
        string category_name
        decimal budget_limit
        date budget_month
    }

    AUDIT_LOGS {
        uuid log_id PK
        uuid profile_id FK
        string action
        json old_values
        json new_values
    }
```

---

## API Endpoints Architecture

```mermaid
graph TB
    API["🔌 Flask API"]
    
    subgraph Auth["Authentication"]
        POST1["POST /auth/signup"]
        POST2["POST /auth/login"]
        POST3["POST /auth/refresh"]
        POST4["POST /auth/logout"]
    end
    
    subgraph BankStatement["Bank Statements"]
        POST5["POST /statements/upload"]
        GET1["GET /statements/:statement_id"]
        GET2["GET /statements/user/:profile_id"]
    end
    
    subgraph Transaction["Transactions"]
        GET3["GET /transactions/:statement_id"]
        GET4["GET /transactions/user/:profile_id"]
        POST6["POST /transactions/repair"]
    end
    
    subgraph Category["Categorization"]
        POST7["POST /categories/classify"]
        GET5["GET /categories/:transaction_id"]
        GET6["GET /categories/summary/:profile_id"]
    end
    
    subgraph Budget["Budget Management"]
        POST8["POST /budgets/set"]
        GET7["GET /budgets/:profile_id"]
        GET8["GET /budgets/forecast"]
    end
    
    subgraph Dashboard["Dashboard"]
        GET9["GET /dashboard/spending"]
        GET10["GET /dashboard/categories"]
        GET11["GET /dashboard/trends"]
    end
    
    API --> Auth
    API --> BankStatement
    API --> Transaction
    API --> Category
    API --> Budget
    API --> Dashboard
    
    style API fill:#e8eaf6
    style Auth fill:#c8e6c9
    style BankStatement fill:#fff9c4
    style Transaction fill:#ffe0b2
    style Category fill:#f8bbd0
    style Budget fill:#e1bee7
    style Dashboard fill:#b2dfdb
```

---

## Deployment Architecture

```mermaid
graph TB
    subgraph Local["Local Development"]
        Code["Source Code"]
        Docker["Docker Compose"]
        LocalDB["Local PostgreSQL"]
    end
    
    subgraph CI["CI/CD Pipeline"]
        GitHub["GitHub Repository"]
        Actions["GitHub Actions"]
        Tests["Run Tests"]
        Build["Build Docker Image"]
    end
    
    subgraph AWS["AWS Cloud"]
        ECR["AWS ECR<br/>Docker Registry"]
        EB["AWS Elastic Beanstalk<br/>Application Hosting"]
        RDS["AWS RDS<br/>PostgreSQL"]
        S3["AWS S3<br/>File Storage"]
        SM["AWS Secrets Manager<br/>Credentials"]
        CW["AWS CloudWatch<br/>Monitoring"]
        IAM["AWS IAM<br/>Access Control"]
    end
    
    Code --> GitHub
    GitHub --> Actions
    Actions --> Tests
    Tests --> Build
    Build --> ECR
    ECR --> EB
    EB --> RDS
    EB --> S3
    EB --> SM
    EB --> CW
    EB --> IAM
    
    Docker --> LocalDB
    
    style Local fill:#f5f5f5
    style CI fill:#fff3e0
    style AWS fill:#e3f2fd
```

---

## Tech Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React, Axios, Redux/Zustand, React Query | UI, API calls, state management |
| **Authentication** | Flask-JWT-Extended, bcrypt | Token generation, password hashing |
| **Backend** | Python Flask, SQLAlchemy, pdfplumber, pandas | API, ORM, PDF processing, data manipulation |
| **Database** | PostgreSQL, AWS RDS | Data persistence, managed database |
| **Storage** | AWS S3 | PDF and CSV file storage |
| **Security** | bcrypt, AWS Secrets Manager, AWS IAM | Password hashing, credential management, access control |
| **Monitoring** | AWS CloudWatch, Sentry | Logging, error tracking |
| **DevOps** | Docker, GitHub Actions, AWS Elastic Beanstalk | Containerization, CI/CD, deployment |
| **Testing** | pytest, Jest | Backend and frontend testing |
| **Migrations** | Alembic | Database schema versioning |

---

## Key Features by Module

### 1. Upload PDF Module
- PDF file upload with validation
- Bank detection (SBI, HDFC, ICICI, KOTAK)
- Transaction table extraction
- Storage in AWS S3
- Processing status tracking

### 2. Preprocessing Module
- Data type normalization (safe_float conversion)
- Missing value imputation using balance inference
- Data validation and error handling
- CSV export with "_NORMALIZED" suffix
- User verification step

### 3. Categorization Module
- Rule-based classification (10 master + 7 special categories)
- ML classification using Random Forest (300 estimators)
- Confidence score calculation (0.0-1.0)
- Merchant extraction
- Hybrid classification method

### 4. Budget Advisor Module
- Budget limit setting per category/month
- Spending analysis and trends
- Savings potential calculation
- Future month projection
- Category-wise savings report

---

## Security Considerations

- JWT tokens with expiration and refresh mechanism
- Bcrypt password hashing (never plain text)
- AWS Secrets Manager for credential storage
- AWS IAM for access control
- Audit logs for all data modifications
- Session timeout enforcement
- HTTPS/TLS for data in transit
- Row-level security for multi-tenant isolation