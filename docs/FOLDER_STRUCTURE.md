# ExpenseIQ Folder Structure

## Root Structure

```
MCA/
├── backend/                        # All backend code
├── frontend/                       # All frontend code
├── docs/                           # Documentation
├── .amazonq/                       # Amazon Q rules
├── .gitignore
└── README.md
```

## Backend Structure (Python Flask)

```
backend/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models/                     # SQLAlchemy models (database schemas)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── transaction.py
│   │   └── category.py
│   ├── controllers/                # Request handlers (business logic)
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── upload_controller.py
│   │   ├── transaction_controller.py
│   │   └── analytics_controller.py
│   ├── services/                   # Core business logic
│   │   ├── __init__.py
│   │   ├── pdf_service.py          # PDF processing
│   │   ├── bank_detector.py        # Bank detection
│   │   ├── parser_service.py       # Transaction parsing
│   │   ├── categorization_service.py
│   │   └── analytics_service.py
│   ├── utils/                      # Helper functions
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── helpers.py
│   ├── config/                     # Configuration files
│   │   ├── __init__.py
│   │   └── config.py
│   └── routes/                     # API route definitions
│       ├── __init__.py
│       ├── auth_routes.py
│       ├── transaction_routes.py
│       └── analytics_routes.py
├── migrations/                     # Alembic database migrations
├── tests/                          # pytest test files
│   ├── __init__.py
│   ├── test_bank_detector.py
│   └── test_parser.py
├── requirements.txt
├── .env
└── run.py                          # Application entry point
```

## Frontend Structure (React + TypeScript)

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/                 # Reusable UI components (Views)
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Modal.tsx
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── dashboard/
│   │   │   ├── CategoryCard.tsx
│   │   │   ├── SpendingChart.tsx
│   │   │   └── TransactionList.tsx
│   │   └── analytics/
│   │       ├── BudgetDialog.tsx
│   │       └── SavingsReport.tsx
│   ├── pages/                      # Page-level components
│   │   ├── HomePage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── UploadPage.tsx
│   │   └── AnalyticsPage.tsx
│   ├── controllers/                # Business logic handlers
│   │   ├── authController.ts
│   │   ├── uploadController.ts
│   │   └── analyticsController.ts
│   ├── models/                     # Data models/interfaces
│   │   ├── Transaction.ts
│   │   ├── Category.ts
│   │   └── User.ts
│   ├── services/                   # API communication
│   │   ├── api.ts                  # Axios instance
│   │   ├── authService.ts
│   │   ├── transactionService.ts
│   │   └── analyticsService.ts
│   ├── store/                      # State management (Redux/Zustand)
│   │   ├── authStore.ts
│   │   ├── transactionStore.ts
│   │   └── analyticsStore.ts
│   ├── hooks/                      # Custom React hooks
│   │   ├── useAuth.ts
│   │   ├── useTransactions.ts
│   │   └── useAnalytics.ts
│   ├── utils/                      # Helper functions
│   │   ├── formatters.ts
│   │   └── validators.ts
│   ├── styles/                     # CSS/styling files
│   │   └── global.css
│   ├── App.tsx                     # Root component
│   └── index.tsx                   # Entry point
├── tsconfig.json                   # TypeScript configuration
├── package.json
└── .env
```

## MVC Architecture Mapping

### Backend (Flask)
- **Models** → `app/models/` (database schemas)
- **Views** → API responses (JSON)
- **Controllers** → `app/controllers/` (orchestrate services and handle requests)
- **Services** → `app/services/` (core business logic, reusable)

### Frontend (React)
- **Models** → `src/models/` (data structures/interfaces)
- **Views** → `src/components/` and `src/pages/` (UI only)
- **Controllers** → `src/controllers/` and `src/hooks/` (business logic)

## File Extensions

- **Backend**: `.py` for all Python files
- **Frontend**: `.tsx` for React components, `.ts` for TypeScript files, `.css` for styles
