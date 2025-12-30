# ExpenseIQ - Project Setup Guide

## Prerequisites

Before starting the project, ensure you have the following installed:

- **Python 3.8+** (Backend)
- **Node.js 16+** and **npm** (Frontend)
- **PostgreSQL 12+** (Database)
- **Git** (Version Control)

---

## Initial Setup (First Time Only)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd MCA
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy .env.example to .env and configure:
# - DATABASE_URL
# - SECRET_KEY
# - JWT_SECRET_KEY
# - AWS credentials (if using)
```

### 3. Database Setup

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE expenseiq_db;
\q

# Run migrations
flask db upgrade

# Or if using Alembic directly:
alembic upgrade head
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env file
# Copy .env.example to .env and configure:
# - REACT_APP_API_URL=http://localhost:5000
```

---

## Starting the Project

### Option 1: Start Everything with Single Command

Create a startup script in the project root:

**For Windows (start.bat):**
```batch
@echo off
echo Starting ExpenseIQ...

echo Starting Backend...
start cmd /k "cd backend && venv\Scripts\activate && python app.py"

timeout /t 5

echo Starting Frontend...
start cmd /k "cd frontend && npm start"

echo ExpenseIQ is starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
```

**For macOS/Linux (start.sh):**
```bash
#!/bin/bash
echo "Starting ExpenseIQ..."

# Start Backend
echo "Starting Backend..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start Frontend
echo "Starting Frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "ExpenseIQ is running..."
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"

# Wait for both processes
wait
```

**Run the script:**
```bash
# Windows:
start.bat

# macOS/Linux:
chmod +x start.sh
./start.sh
```

---

### Option 2: Start Backend and Frontend Separately

#### Start Backend Only

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start Flask server
python app.py

# Or with Flask CLI:
flask run

# Or with specific host and port:
flask run --host=0.0.0.0 --port=5000

# Backend will run on: http://localhost:5000
```

#### Start Frontend Only

```bash
# Navigate to frontend directory
cd frontend

# Start React development server
npm start

# Frontend will run on: http://localhost:3000
```

---

## Running Tests

### Backend Tests

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=expenseiq --cov-report=html

# Run specific test file
pytest tests/test_ingestion.py

# Run specific test function
pytest tests/test_ingestion.py::test_detect_bank

# Run tests and stop on first failure
pytest -x
```

### Frontend Tests

```bash
# Navigate to frontend directory
cd frontend

# Run all tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch

# Run specific test file
npm test -- TransactionList.test.js
```

---

## Database Management Commands

### Create New Migration

```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Using Flask-Migrate
flask db migrate -m "Description of changes"

# Using Alembic
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
# Using Flask-Migrate
flask db upgrade

# Using Alembic
alembic upgrade head
```

### Rollback Migration

```bash
# Using Flask-Migrate
flask db downgrade

# Using Alembic
alembic downgrade -1
```

### Reset Database

```bash
# Drop all tables and recreate
flask db downgrade base
flask db upgrade

# Or manually:
psql -U postgres
DROP DATABASE expenseiq_db;
CREATE DATABASE expenseiq_db;
\q
flask db upgrade
```

---

## Additional Useful Commands

### Backend Commands

#### Install New Python Package

```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

pip install <package-name>
pip freeze > requirements.txt
```

#### Run Python Shell with App Context

```bash
flask shell
```

#### Check Code Style (Linting)

```bash
# Install flake8 if not installed
pip install flake8

# Run linter
flake8 expenseiq/

# Auto-format code with black
pip install black
black expenseiq/
```

#### Generate Requirements File

```bash
pip freeze > requirements.txt
```

---

### Frontend Commands

#### Install New npm Package

```bash
cd frontend

# Install and save to dependencies
npm install <package-name>

# Install and save to devDependencies
npm install --save-dev <package-name>
```

#### Build for Production

```bash
npm run build
```

#### Check Code Style (Linting)

```bash
# Run ESLint
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix
```

#### Update Dependencies

```bash
# Check for outdated packages
npm outdated

# Update all packages
npm update

# Update specific package
npm update <package-name>
```

---

## Environment Variables Reference

### Backend (.env)

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/expenseiq_db

# AWS Configuration (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
AWS_S3_BUCKET=expenseiq-uploads

# CORS Configuration
CORS_ORIGINS=http://localhost:3000

# File Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads/
```

### Frontend (.env)

```env
# API Configuration
REACT_APP_API_URL=http://localhost:5000

# Environment
REACT_APP_ENV=development

# Optional: Analytics, Error Tracking
REACT_APP_SENTRY_DSN=your-sentry-dsn
```

---

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

**Database connection error:**
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Ensure database exists

**Module not found error:**
- Activate virtual environment
- Run `pip install -r requirements.txt`

### Frontend Issues

**Port 3000 already in use:**
- Kill the process or use different port:
```bash
# Set different port
PORT=3001 npm start
```

**Module not found error:**
- Delete node_modules and package-lock.json
- Run `npm install` again

**Build fails:**
- Clear cache: `npm cache clean --force`
- Delete node_modules and reinstall

---

## Production Deployment Checklist

- [ ] Set `FLASK_ENV=production` in backend
- [ ] Set `REACT_APP_ENV=production` in frontend
- [ ] Use strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Configure AWS RDS for database
- [ ] Set up AWS Secrets Manager for credentials
- [ ] Configure AWS Elastic Beanstalk
- [ ] Set up AWS CloudWatch for monitoring
- [ ] Configure GitHub Actions for CI/CD
- [ ] Enable HTTPS/SSL
- [ ] Set up proper CORS origins
- [ ] Run `npm run build` for frontend
- [ ] Configure rate limiting
- [ ] Set up backup strategy for database
- [ ] Enable error tracking (Sentry)

---

## Quick Reference

| Task | Command |
|------|---------|
| Start Backend | `cd backend && venv\Scripts\activate && python app.py` |
| Start Frontend | `cd frontend && npm start` |
| Run Backend Tests | `cd backend && pytest` |
| Run Frontend Tests | `cd frontend && npm test` |
| Create Migration | `flask db migrate -m "message"` |
| Apply Migration | `flask db upgrade` |
| Install Backend Package | `pip install <package> && pip freeze > requirements.txt` |
| Install Frontend Package | `npm install <package>` |
| Build Frontend | `npm run build` |
| Check Backend Style | `flake8 expenseiq/` |
| Check Frontend Style | `npm run lint` |

---

## Support

For issues or questions:
- Check the troubleshooting section above
- Review error logs in console
- Check AWS CloudWatch logs (production)
- Refer to individual package documentation
