# PDF Upload Feature - Quick Start Guide

## For Developers

### Prerequisites
- Node.js 16+ installed
- Python 3.8+ installed
- PostgreSQL running
- Git repository cloned

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create `.env` file in backend directory:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/expenseiq
JWT_SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=storage/uploads
OUTPUT_FOLDER=storage/outputs
```

5. **Run database migrations**
```bash
python migrations/create_auth_tables.py
```

6. **Start backend server**
```bash
python run.py
```

Backend should be running on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**
Create `.env` file in frontend directory:
```env
VITE_API_BASE_URL=http://localhost:5000/api
```

4. **Start development server**
```bash
npm run dev
```

Frontend should be running on `http://localhost:5173`

### Testing the Feature

1. **Create a test user**
   - Navigate to `http://localhost:5173/signup`
   - Create an account
   - Login with credentials

2. **Access PDF Upload**
   - Navigate to `http://localhost:5173/upload`
   - Or click "Upload" in navigation menu

3. **Upload a PDF**
   - Drag and drop a bank statement PDF
   - Or click to browse and select file
   - Select bank from dropdown
   - Click "Upload" button

4. **Download CSV**
   - Wait for processing to complete
   - Click "Download CSV" button
   - Verify CSV file downloads

### Project Structure

```
MCA/
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   │   └── pdf_controller.py
│   │   ├── routes/
│   │   │   └── pdf_routes.py
│   │   ├── services/
│   │   │   └── ingestion/
│   │   │       ├── detect.py
│   │   │       ├── extract.py
│   │   │       └── standardize.py
│   │   └── models/
│   │       └── bank_statement.py
│   ├── storage/
│   │   ├── uploads/    # PDFs saved here
│   │   └── outputs/    # CSVs saved here
│   └── run.py
└── frontend/
    └── src/
        ├── models/
        │   └── PDFUploadResponse.ts
        ├── services/
        │   └── pdfService.ts
        ├── controllers/
        │   └── pdfController.ts
        ├── components/common/
        │   ├── PDFUploader.tsx
        │   ├── UploadProgress.tsx
        │   └── UploadResult.tsx
        └── pages/
            └── PDFUploadPage.tsx
```

### API Endpoints

#### Upload PDF
```
POST /api/pdf/upload
Headers: Authorization: Bearer <token>
Body: multipart/form-data
  - pdf: File
  - bank: String (HDFC, KOTAK, SBI, ICICI, AXIS, CUB, IDFC)
```

#### Download CSV
```
GET /api/pdf/download/:filename
Headers: Authorization: Bearer <token>
```

### Common Issues

#### Issue: "Module not found" error
**Solution:** Run `npm install` or `pip install -r requirements.txt`

#### Issue: Database connection error
**Solution:** Check PostgreSQL is running and DATABASE_URL is correct

#### Issue: CORS error
**Solution:** Verify Flask-CORS is installed and configured

#### Issue: File upload fails
**Solution:** Check UPLOAD_FOLDER and OUTPUT_FOLDER exist and have write permissions

#### Issue: JWT token invalid
**Solution:** Login again to get fresh token

### Development Tips

1. **Hot Reload**
   - Frontend: Vite provides automatic hot reload
   - Backend: Use `flask run --reload` for auto-restart

2. **Debugging**
   - Frontend: Use React DevTools browser extension
   - Backend: Use Python debugger or print statements

3. **Testing**
   - Frontend: `npm test`
   - Backend: `pytest`

4. **Code Quality**
   - Frontend: `npm run lint`
   - Backend: `flake8 app/`

### File Locations

**Uploaded PDFs:** `backend/storage/uploads/`
**Generated CSVs:** `backend/storage/outputs/`
**Database:** PostgreSQL (check .env for connection string)

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/expenseiq
JWT_SECRET_KEY=your-secret-key
UPLOAD_FOLDER=storage/uploads
OUTPUT_FOLDER=storage/outputs
FLASK_ENV=development
```

#### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:5000/api
```

### Database Schema

**bank_statements table:**
- file_id (UUID, Primary Key)
- profile_id (UUID, Foreign Key)
- bank_name (String)
- file_name (String)
- file_path (String)
- file_size_bytes (Integer)
- processing_status (String: PENDING, PROCESSING, COMPLETED, FAILED)
- extracted_csv_path (String)
- normalized_csv_path (String)
- error_message (String, nullable)
- created_at (Timestamp)
- updated_at (Timestamp)

### Supported Banks

1. HDFC Bank
2. Kotak Mahindra Bank
3. State Bank of India (SBI)
4. ICICI Bank
5. Axis Bank
6. City Union Bank (CUB)
7. IDFC First Bank

### Sample Test Data

Create sample PDFs for each bank or use real bank statements (with sensitive data removed).

### Git Workflow

1. **Create feature branch**
```bash
git checkout -b feature/pdf-upload
```

2. **Make changes and commit**
```bash
git add .
git commit -m "Add PDF upload feature"
```

3. **Push to remote**
```bash
git push origin feature/pdf-upload
```

4. **Create pull request**
   - Go to GitHub
   - Create PR from feature branch to main
   - Request code review

### Code Review Checklist

Before submitting PR:
- [ ] Code follows MVC architecture
- [ ] No unused variables or imports
- [ ] Proper error handling
- [ ] Type safety (TypeScript)
- [ ] No console.log statements
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No sensitive data in code

### Deployment

#### Frontend
```bash
npm run build
# Deploy dist/ folder to hosting service
```

#### Backend
```bash
# Create deployment package
zip -r deploy.zip app/ requirements.txt run.py

# Deploy to AWS Elastic Beanstalk
eb deploy
```

### Monitoring

#### Development
- Frontend: Browser console
- Backend: Terminal logs

#### Production
- AWS CloudWatch for logs
- Sentry for error tracking (optional)

### Performance Optimization

1. **Frontend**
   - Code splitting
   - Lazy loading
   - Image optimization
   - Caching

2. **Backend**
   - Database indexing
   - Query optimization
   - Connection pooling
   - Caching

### Security Checklist

- [ ] JWT authentication enabled
- [ ] File type validation
- [ ] File size limits
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CORS configured
- [ ] HTTPS in production
- [ ] Environment variables secured

### Next Features to Implement

1. Upload history page
2. Transaction preview
3. Batch upload
4. Auto-detect bank
5. Progress notifications
6. File compression

### Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [AWS Documentation](https://docs.aws.amazon.com/)

### Support

For issues or questions:
1. Check documentation in `docs/` folder
2. Review error logs
3. Check GitHub issues
4. Contact team lead

### License

See LICENSE file in repository root.

---

## Quick Commands Reference

### Backend
```bash
# Start server
python run.py

# Run tests
pytest

# Database migration
alembic upgrade head

# Check code quality
flake8 app/
```

### Frontend
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

### Git
```bash
# Pull latest changes
git pull origin main

# Create branch
git checkout -b feature/name

# Commit changes
git add .
git commit -m "message"

# Push changes
git push origin branch-name
```

### Docker (Future)
```bash
# Build image
docker build -t expenseiq .

# Run container
docker run -p 5000:5000 expenseiq

# Docker compose
docker-compose up
```

---

**Happy Coding! 🚀**
