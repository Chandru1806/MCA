# ExpenseIQ Tech Stack - Complete Overview

## Backend Technologies

### Core Framework
**Python Flask**
- Lightweight WSGI web application framework
- Flexible and easy to extend
- Perfect for RESTful API development
- Minimal boilerplate code

### Database & ORM
**SQLAlchemy (ORM)**
- Python SQL toolkit and Object-Relational Mapping
- Provides full SQL expression language
- Prevents SQL injection attacks
- Database-agnostic (works with PostgreSQL, MySQL, SQLite)

**PostgreSQL**
- Open-source relational database
- ACID compliant for data integrity
- Excellent performance for complex queries
- Strong support for JSON data types
- Robust transaction support

**AWS RDS (Managed Database)**
- Automated backups and point-in-time recovery
- Automatic software patching
- Multi-AZ deployment for high availability
- Scalable storage and compute resources
- Monitoring via CloudWatch integration

**Alembic (Database Migrations)**
- Database migration tool for SQLAlchemy
- Version control for database schema
- Supports forward and backward migrations
- Essential for production deployments

### Authentication & Security
**Flask-JWT-Extended (Authentication)**
- JSON Web Token authentication for Flask
- Stateless authentication mechanism
- Token refresh functionality
- Blacklist support for logout
- Role-based access control

**bcrypt (Password Hashing)**
- Industry-standard password hashing
- Adaptive hash function (resistant to brute-force)
- Salt generation for each password
- Configurable work factor for future-proofing

**AWS Secrets Manager (Credential Management)**
- Centralized secrets management
- Automatic rotation of credentials
- Encryption at rest and in transit
- Fine-grained access control via IAM
- Audit trail via CloudTrail

### API & Communication
**Flask-CORS (API Communication)**
- Cross-Origin Resource Sharing support
- Enables frontend-backend communication
- Configurable origin whitelist
- Supports preflight requests

### PDF Processing
**pdfplumber (PDF Processing)**
- Extract text and tables from PDFs
- Precise table detection
- Character-level positioning
- Works with complex PDF layouts
- Better than PyPDF2 for bank statements

### Data Processing
**pandas (Data Manipulation)**
- Powerful data analysis library
- DataFrame operations for transaction data
- CSV reading and writing
- Data cleaning and transformation
- Statistical operations

### Environment & Configuration
**python-dotenv (Environment Management)**
- Load environment variables from .env files
- Separates configuration from code
- Different configs for dev/staging/prod
- Keeps secrets out of version control

**psycopg2 (PostgreSQL Adapter)**
- PostgreSQL database adapter for Python
- Required by SQLAlchemy for PostgreSQL
- Efficient connection pooling
- Binary version (psycopg2-binary) for easy installation

### Testing
**pytest (Testing)**
- Modern Python testing framework
- Simple and scalable test structure
- Fixtures for test setup/teardown
- Parametrized testing
- Coverage reporting integration

---

## Frontend Technologies

### Core Framework
**React 18+**
- Component-based UI library
- Virtual DOM for performance
- Hooks for state management
- Large ecosystem and community

**TypeScript**
- Static type checking
- Better IDE support and autocomplete
- Catches errors at compile time
- Improved code documentation
- Easier refactoring

### Build Tool
**Vite**
- Fast development server with HMR
- Optimized production builds
- Native ES modules support
- Better than Create React App for performance

### Routing
**React Router v6**
- Declarative routing for React
- Nested routes support
- Protected routes implementation
- URL parameter handling

### API Communication
**Axios (API Communication)**
- Promise-based HTTP client
- Request/response interceptors
- Automatic JSON transformation
- Better error handling than fetch
- Request cancellation support
- File upload support (multipart/form-data)

### State Management
**Redux or Zustand (State Management)**

**Redux:**
- Predictable state container
- Time-travel debugging
- Middleware support (Redux Thunk, Saga)
- Large ecosystem
- Best for complex state logic

**Zustand (RECOMMENDED):**
- Simpler API than Redux
- Less boilerplate code
- Built-in TypeScript support
- Smaller bundle size
- Sufficient for ExpenseIQ's needs

**Recommendation:** Use Zustand for ExpenseIQ due to:
- Simpler learning curve
- Less code to maintain
- Better performance for small-to-medium apps
- Easier testing

### Server State Management
**React Query (Server State)**
- Caching and synchronization of server state
- Automatic background refetching
- Optimistic updates
- Request deduplication
- Pagination and infinite scroll support
- Reduces boilerplate for API calls

### Testing
**Jest (Testing)**
- JavaScript testing framework
- Snapshot testing
- Mocking capabilities
- Code coverage reports
- Watch mode for development

**React Testing Library (RECOMMENDED ADDITION)**
- Test React components
- User-centric testing approach
- Works with Jest
- Encourages accessibility

---

## Database

### Primary Database
**PostgreSQL**
- See Backend section for details

**AWS RDS (Managed Database)**
- See Backend section for details

---

## Deployment & DevOps

### Version Control
**GitHub (Version Control)**
- Source code management
- Collaboration and code review
- Issue tracking
- Project management

### CI/CD
**GitHub Actions (CI/CD)**
- Automated testing on push
- Automated deployment pipelines
- Matrix builds for multiple environments
- Secrets management
- Integration with AWS

### Application Hosting
**AWS Elastic Beanstalk (Application Hosting)**
- Platform as a Service (PaaS)
- Automatic capacity provisioning
- Load balancing
- Auto-scaling
- Health monitoring
- Easy deployment (zip upload or CLI)
- Supports Python and Node.js

### Monitoring & Logging
**AWS CloudWatch (Monitoring & Logging)**
- Application and infrastructure metrics
- Log aggregation and analysis
- Custom dashboards
- Alarms and notifications
- Integration with Elastic Beanstalk
- Performance insights

### Access Management
**AWS IAM (Access Management)**
- Fine-grained access control
- Role-based permissions
- Service-to-service authentication
- Multi-factor authentication
- Audit trail via CloudTrail

---

## Additional Tools

### Containerization (Future)
**Docker (Future Implementation)**
- Containerize application
- Consistent environments (dev/staging/prod)
- Easier deployment
- Microservices architecture support
- Local development environment

**Why Future?**
- Not critical for initial deployment
- Elastic Beanstalk supports Docker when needed
- Adds complexity for small team
- Implement when scaling requirements increase

### Error Tracking (Optional)
**Sentry (Error Tracking - Optional)**
- Real-time error tracking
- Stack traces and context
- Release tracking
- Performance monitoring
- User feedback collection

**Why Optional?**
- CloudWatch provides basic error logging
- Sentry adds cost
- Implement if error volume becomes high
- Useful for production debugging

---

## Recommended Additions

### 1. React Testing Library
**Purpose:** Component testing
**Why:** Jest alone doesn't test React components effectively
**Installation:** `npm install --save-dev @testing-library/react @testing-library/jest-dom`

### 2. ESLint & Prettier
**Purpose:** Code quality and formatting
**Why:** Enforces coding standards, catches errors
**Installation:** 
```bash
npm install --save-dev eslint prettier eslint-config-prettier
npm install --save-dev @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

### 3. Husky & lint-staged
**Purpose:** Pre-commit hooks
**Why:** Prevents bad code from being committed
**Installation:** `npm install --save-dev husky lint-staged`

### 4. React Hook Form
**Purpose:** Form handling
**Why:** Better performance than controlled components, less re-renders
**Installation:** `npm install react-hook-form`
**Use Case:** PDF upload form, login/signup forms

### 5. Zod
**Purpose:** Schema validation
**Why:** TypeScript-first validation, works with React Hook Form
**Installation:** `npm install zod @hookform/resolvers`
**Use Case:** Form validation, API response validation

### 6. date-fns
**Purpose:** Date manipulation
**Why:** Lightweight alternative to moment.js, tree-shakeable
**Installation:** `npm install date-fns`
**Use Case:** Transaction date formatting, analytics date ranges

### 7. Recharts
**Purpose:** Data visualization
**Why:** React-based charts, responsive, customizable
**Installation:** `npm install recharts`
**Use Case:** Dashboard charts, spending trends, budget visualization

### 8. React Hot Toast
**Purpose:** Toast notifications
**Why:** Better UX for success/error messages
**Installation:** `npm install react-hot-toast`
**Use Case:** Upload success, error notifications, form submissions

---

## Updated Complete Tech Stack

### Backend
- Python Flask
- SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- Flask-CORS (API Communication)
- pdfplumber (PDF Processing)
- pandas (Data Manipulation)
- python-dotenv (Environment Management)
- psycopg2 (PostgreSQL Adapter)
- Alembic (Database Migrations)
- pytest (Testing)
- bcrypt (Password Hashing)

### Frontend
- React 18+
- TypeScript
- Vite (Build Tool)
- React Router v6 (Routing)
- Axios (API Communication)
- Zustand (State Management) ✓ RECOMMENDED
- React Query (Server State)
- Jest (Testing)
- React Testing Library ✓ NEW
- ESLint & Prettier ✓ NEW
- Husky & lint-staged ✓ NEW
- React Hook Form ✓ NEW
- Zod ✓ NEW
- date-fns ✓ NEW
- Recharts ✓ NEW
- React Hot Toast ✓ NEW

### Database
- PostgreSQL
- AWS RDS (Managed Database)

### Deployment
- GitHub (Version Control)
- GitHub Actions (CI/CD)
- AWS Elastic Beanstalk (Application Hosting)
- AWS CloudWatch (Monitoring & Logging)
- AWS IAM (Access Management)

### Security
- bcrypt (Password Hashing)
- AWS Secrets Manager (Credential Management)
- Flask-JWT-Extended (Token Management)

### Future/Optional
- Docker (Containerization)
- Sentry (Error Tracking)

---

## Installation Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

### New Frontend Dependencies
```bash
# Testing
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Code Quality
npm install --save-dev eslint prettier eslint-config-prettier
npm install --save-dev @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Pre-commit Hooks
npm install --save-dev husky lint-staged

# Form Handling
npm install react-hook-form zod @hookform/resolvers

# Utilities
npm install date-fns recharts react-hot-toast
```

---

## Architecture Benefits

### Scalability
- Horizontal scaling via Elastic Beanstalk
- Database scaling via RDS
- Stateless authentication (JWT)
- Caching via React Query

### Security
- Multiple layers of authentication
- Encrypted credentials
- SQL injection prevention
- XSS prevention
- CORS protection

### Maintainability
- Type safety (TypeScript)
- Code quality tools (ESLint, Prettier)
- Automated testing (Jest, pytest)
- Database migrations (Alembic)
- Version control (GitHub)

### Performance
- Fast build times (Vite)
- Optimized queries (SQLAlchemy)
- Client-side caching (React Query)
- CDN for static assets
- Database indexing

### Developer Experience
- Hot module replacement (Vite)
- Type checking (TypeScript)
- Auto-formatting (Prettier)
- Pre-commit hooks (Husky)
- Comprehensive error messages

---

## Cost Considerations

### Free Tier Eligible
- GitHub (public repos)
- AWS RDS (750 hours/month for 12 months)
- AWS Elastic Beanstalk (no additional charge, pay for resources)
- AWS CloudWatch (basic monitoring)

### Paid Services
- AWS RDS (after free tier)
- AWS Elastic Beanstalk resources (EC2, Load Balancer)
- AWS Secrets Manager ($0.40/secret/month)
- Sentry (optional, has free tier)

### Cost Optimization
- Use t2.micro/t3.micro instances
- Enable auto-scaling with min=1
- Use RDS single-AZ for development
- Implement CloudWatch alarms for cost monitoring
- Use AWS Cost Explorer for tracking

---

## Thesis Writing Format Compliance

This tech stack documentation follows the specified format:
- Font: Times New Roman
- Main text: 12 pt
- Headings: 14 pt, Bold, ALL CAPS (for chapters)
- Sub-headings: 12 pt, Bold
- Line spacing: 1.5
- Alignment: Justified
- Indentation: First line – 0.5 inch
