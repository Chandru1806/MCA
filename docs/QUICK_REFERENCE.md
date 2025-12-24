# ExpenseIQ - Quick Reference Guide

## Running the Application

### Backend (Flask)
```bash
cd backend
python run.py
```

### Frontend (React - To be initialized)
```bash
cd frontend
npm install
npm start
```

## Project Structure Overview

### Backend (Python Flask)
```
backend/
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
├── app/
│   ├── models/                     # Database models (SQLAlchemy)
│   ├── controllers/                # Business logic handlers
│   ├── services/                   # Core business logic
│   │   ├── ingestion/              # PDF parsing & bank detection
│   │   ├── preprocessing/          # Data cleaning & normalization
│   │   ├── repair/                 # Reject file repair
│   │   └── *_categorizer.py        # Transaction categorization
│   ├── routes/                     # API route definitions
│   ├── utils/                      # Helper functions
│   ├── config/                     # Configuration files
│   └── templates/                  # HTML templates (Flask)
├── tests/                          # Unit tests
├── migrations/                     # Database migrations (Alembic)
└── storage/                        # File uploads & outputs
```

### Frontend (React + TypeScript)
```
frontend/
├── public/                         # Static assets
└── src/
    ├── components/                 # Reusable UI components
    │   ├── common/                 # Shared components (Button, Input, Modal)
    │   ├── auth/                   # Login, Register forms
    │   ├── dashboard/              # Dashboard widgets
    │   └── analytics/              # Analytics components
    ├── pages/                      # Page-level components
    ├── controllers/                # Business logic
    ├── models/                     # TypeScript interfaces
    ├── services/                   # API communication (Axios)
    ├── store/                      # State management (Redux/Zustand)
    ├── hooks/                      # Custom React hooks
    ├── utils/                      # Helper functions
    └── styles/                     # CSS files
```

## Key Files & Their Purpose

### Backend
- **run.py**: Flask app initialization and route registration
- **app/services/ingestion/**: Handles PDF upload, bank detection, and parsing
- **app/services/preprocessing/**: Data normalization and cleaning
- **app/services/repair/**: Repairs rejected transactions
- **app/services/*_categorizer.py**: ML-based transaction categorization
- **app/templates/**: HTML templates for Flask views

### Frontend (To be created)
- **src/App.tsx**: Root React component
- **src/index.tsx**: Application entry point
- **src/services/api.ts**: Axios configuration for API calls
- **src/store/**: Global state management
- **src/components/**: Reusable UI components

## Import Path Examples

### Backend
```python
# From run.py
from app.services.ingestion import ingestion_bp
from app.services.preprocessing import preprocess_csv

# From controllers
from app.models.user import User
from app.services.pdf_service import parse_pdf

# From services
from app.utils.validators import validate_date
```

### Frontend (TypeScript)
```typescript
// From pages
import { Button } from '@/components/common/Button';
import { authService } from '@/services/authService';

// From components
import { useAuth } from '@/hooks/useAuth';
import { Transaction } from '@/models/Transaction';
```

## Development Workflow

### Adding a New Feature

#### Backend:
1. Create model in `app/models/`
2. Create service logic in `app/services/`
3. Create controller in `app/controllers/`
4. Define routes in `app/routes/`
5. Register blueprint in `run.py`

#### Frontend:
1. Create TypeScript interface in `src/models/`
2. Create API service in `src/services/`
3. Create UI component in `src/components/`
4. Create page in `src/pages/`
5. Add route in router configuration

## Environment Variables

Create `.env` file in `backend/` directory:
```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=expenseiq
FLASK_SECRET_KEY=your_secret_key
```

## Testing

### Backend
```bash
cd backend
pytest tests/
```

### Frontend
```bash
cd frontend
npm test
```

## Deployment

### Backend (AWS Elastic Beanstalk)
```bash
cd backend
eb init
eb create
eb deploy
```

### Frontend (Build for production)
```bash
cd frontend
npm run build
```

## Common Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py

# Run tests
pytest

# Database migrations
alembic upgrade head
```

### Frontend
```bash
# Initialize React + TypeScript project
npx create-react-app . --template typescript

# Install dependencies
npm install axios redux react-redux @reduxjs/toolkit

# Run development server
npm start

# Build for production
npm run build
```

## Notes

- Backend runs on port 5000 by default
- Frontend will run on port 3000 by default
- API calls from frontend should point to `http://localhost:5000`
- Use CORS configuration in Flask for local development
