# ExpenseIQ Test Suite

## Overview
Comprehensive test suite for ExpenseIQ using pytest framework.

## Test Structure

```
tests/
├── conftest.py                    # Pytest fixtures and configuration
├── modules/                       # Unit tests for individual modules
│   ├── test_auth_service.py      # Authentication tests
│   ├── test_bank_detection.py    # Bank detection tests
│   ├── test_transaction_service.py
│   ├── test_categorization_service.py
│   ├── test_dashboard_service.py
│   ├── test_analytics_service.py
│   ├── test_budget_service.py
│   ├── test_preprocessing.py
│   └── test_models.py            # Model validation tests
├── integration/                   # Integration tests
│   └── test_api_endpoints.py     # API endpoint tests
└── fixtures/                      # Test data fixtures
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific module tests
```bash
pytest tests/modules/test_auth_service.py
```

### Run with coverage
```bash
pytest --cov=app --cov-report=html
```

### Run only unit tests
```bash
pytest -m unit
```

### Run only integration tests
```bash
pytest -m integration
```

## Test Coverage

- **Authentication Module**: Signup, login, user management
- **PDF Upload Module**: Bank detection, file validation
- **Transaction Module**: Import, retrieval, filtering
- **Categorization Module**: Rule-based and ML classification
- **Dashboard Module**: Category summary, spending trends
- **Analytics Module**: Forecasting, savings calculation
- **Budget Module**: Budget creation, tracking, alerts
- **Preprocessing Module**: Data normalization, validation

## Fixtures

- `app`: Flask application instance
- `client`: Test client for API calls
- `session`: Database session
- `sample_user`: Test user
- `sample_statement`: Test bank statement
- `sample_transaction`: Test transaction

## Notes

- Tests use in-memory SQLite database
- Each test function runs in isolated transaction
- Mock data is automatically cleaned up after tests
