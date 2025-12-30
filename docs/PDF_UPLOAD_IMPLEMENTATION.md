# PDF Upload Feature Implementation

## Overview
This document describes the complete implementation of the PDF Upload feature for ExpenseIQ, following MVC architecture and clean code principles.

## Architecture

### Frontend Structure (React + TypeScript)

```
frontend/src/
├── models/
│   └── PDFUploadResponse.ts          # Data model for upload response
├── services/
│   └── pdfService.ts                 # API communication layer
├── controllers/
│   └── pdfController.ts              # Business logic and validation
├── components/common/
│   ├── PDFUploader.tsx               # File upload component
│   ├── UploadProgress.tsx            # Progress indicator component
│   └── UploadResult.tsx              # Result display component
└── pages/
    └── PDFUploadPage.tsx             # Main page integrating all components
```

### Backend Structure (Python Flask)

```
backend/app/
├── controllers/
│   └── pdf_controller.py             # Request handling and orchestration
├── routes/
│   └── pdf_routes.py                 # API endpoint definitions
└── services/ingestion/
    ├── detect.py                     # Bank detection logic
    ├── extract.py                    # Transaction extraction
    └── standardize.py                # Data standardization
```

## Features Implemented

### 1. PDF Upload Component (PDFUploader.tsx)
- Drag-and-drop file upload zone
- Click-to-browse fallback
- File type validation (PDF only)
- File size display
- Bank selection dropdown with 7 supported banks:
  - HDFC
  - KOTAK
  - SBI
  - ICICI
  - AXIS
  - CUB
  - IDFC
- Inline error messages
- Disabled state during upload

### 2. Upload Progress Component (UploadProgress.tsx)
- Horizontal progress bar with percentage
- Status messages:
  - "Uploading PDF..."
  - "Extracting transactions..."
  - "Processing data..."
- Visual feedback during processing

### 3. Upload Result Component (UploadResult.tsx)
- Success state with green border:
  - Detected Bank
  - Transaction Count
  - Statement ID
  - Download CSV button (manual trigger only)
- Error state with red border:
  - Error message
  - Retry button
- No auto-download functionality

### 4. PDF Upload Page (PDFUploadPage.tsx)
- Centered layout with single card
- Page title: "Upload Bank Statement"
- Descriptive subtitle
- Three vertical sections:
  1. PDF Upload
  2. Upload Progress (conditional)
  3. Upload Result (conditional)
- Clean fintech styling
- Responsive design

### 5. Backend API

#### Endpoint: POST /api/pdf/upload
**Request:**
- Content-Type: multipart/form-data
- Fields:
  - `pdf`: PDF file
  - `bank`: Bank name (HDFC, KOTAK, SBI, ICICI, AXIS, CUB, IDFC)

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "statement_id": "12345",
    "bank_name": "HDFC",
    "transaction_count": 45,
    "csv_filename": "batch123_statement__STD_HDFC.csv"
  }
}
```

**Response (Error):**
```json
{
  "error": "Bank required. Valid: HDFC, KOTAK, SBI, ICICI, AXIS, CUB, IDFC"
}
```

#### Endpoint: GET /api/pdf/download/:filename
**Request:**
- Requires JWT authentication
- URL parameter: filename

**Response:**
- CSV file download

## Validation Rules

### Frontend Validation
1. File must be selected
2. File type must be PDF
3. File size must be less than 10MB
4. Bank must be selected (not "AUTO")

### Backend Validation
1. PDF file must be present in request
2. Filename must not be empty
3. Bank must be one of the supported banks
4. File must be successfully saved and processed

## Error Handling

### Frontend Errors
- File type validation error
- File size validation error
- Bank selection validation error
- Network/API errors with user-friendly messages

### Backend Errors
- Missing file error (400)
- Invalid bank error (400)
- Processing errors (500)
- Database errors (500)

## Security Features
- JWT authentication required for all endpoints
- Secure filename handling
- File type validation
- File size limits
- SQL injection prevention via ORM
- XSS prevention via React's built-in escaping

## Database Schema

### BankStatement Model
```python
- file_id (Primary Key)
- profile_id (Foreign Key to User)
- bank_name
- file_name
- file_path
- file_size_bytes
- processing_status (PENDING, PROCESSING, COMPLETED, FAILED)
- extracted_csv_path
- normalized_csv_path
- error_message
- created_at
- updated_at
```

## Styling Guidelines

### Colors
- Primary: #4299e1 (Blue)
- Success: #48bb78 (Green)
- Error: #e53e3e (Red)
- Background: #f7fafc (Light Gray)
- Text: #1a202c (Dark Gray)

### Typography
- Title: 28px, Bold
- Section Heading: 16px, Bold
- Body Text: 14px
- Small Text: 12px

### Spacing
- Card Padding: 20px
- Section Margin: 15-20px
- Element Gap: 10-15px

## Testing Checklist

### Frontend Tests
- [ ] File selection via drag-and-drop
- [ ] File selection via click-to-browse
- [ ] PDF validation (accept only PDF)
- [ ] Non-PDF rejection
- [ ] Bank selection validation
- [ ] Upload button disabled when invalid
- [ ] Progress bar updates correctly
- [ ] Success state displays correctly
- [ ] Error state displays correctly
- [ ] CSV download triggers on button click only
- [ ] Retry functionality works

### Backend Tests
- [ ] PDF upload with valid bank
- [ ] PDF upload with invalid bank
- [ ] PDF upload without file
- [ ] PDF upload without bank selection
- [ ] Transaction extraction for each bank
- [ ] CSV generation
- [ ] Database record creation
- [ ] Status updates (PENDING → PROCESSING → COMPLETED)
- [ ] Error handling and FAILED status
- [ ] CSV download with authentication

## Usage Flow

1. User navigates to `/upload`
2. User drags PDF or clicks to browse
3. User selects bank from dropdown
4. User clicks "Upload" button
5. Progress bar shows upload status
6. System extracts and processes transactions
7. Result displays with transaction count
8. User clicks "Download CSV" to get file
9. User can retry on error

## Future Enhancements

1. Auto-detect bank from PDF content
2. Support for additional banks
3. Real-time progress updates via WebSocket
4. Batch upload support
5. Preview transactions before download
6. Direct navigation to categorization after upload
7. Upload history and management
8. File compression for large PDFs

## Dependencies

### Frontend
- React 18+
- TypeScript 4+
- Axios (API calls)
- React Router (routing)

### Backend
- Flask
- Flask-JWT-Extended
- pdfplumber
- pandas
- SQLAlchemy
- psycopg2

## API Integration

The frontend uses the centralized `apiClient` utility which:
- Automatically adds JWT token to requests
- Handles base URL configuration
- Provides consistent error handling
- Supports multipart/form-data uploads

## Compliance

### Code Standards
- Follows PEP 8 (Python)
- Follows React best practices (TypeScript)
- MVC architecture maintained
- Single responsibility principle
- No unused variables or imports
- Proper error handling
- Meaningful variable names
- No console.log in production
- No Unicode characters in UI text

### Security Standards
- JWT authentication
- Input validation
- SQL injection prevention
- XSS prevention
- Secure file handling
- No sensitive data exposure
