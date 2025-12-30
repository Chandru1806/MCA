# PDF Upload Feature - Quick Testing Guide

## Prerequisites
1. Backend server running on configured port
2. Frontend development server running
3. Valid JWT token (user logged in)
4. Sample bank statement PDFs for testing

## Manual Testing Steps

### Test 1: Successful Upload Flow
1. Navigate to `/upload`
2. Drag a valid PDF file into the upload zone
3. Select "HDFC" from bank dropdown
4. Click "Upload" button
5. Verify progress bar appears and updates
6. Verify success message with:
   - Bank name: HDFC
   - Transaction count: [number]
   - Statement ID: [UUID]
7. Click "Download CSV" button
8. Verify CSV file downloads

**Expected Result:** ✓ Upload successful, CSV downloaded

### Test 2: File Type Validation
1. Navigate to `/upload`
2. Try to upload a .txt or .docx file
3. Verify error message: "Only PDF files are allowed"
4. Verify upload button is disabled

**Expected Result:** ✓ Non-PDF files rejected

### Test 3: Bank Selection Validation
1. Navigate to `/upload`
2. Select a valid PDF file
3. Leave bank dropdown at "Auto-detect or select manually"
4. Click "Upload" button
5. Verify error message: "Please select a bank"

**Expected Result:** ✓ Upload blocked without bank selection

### Test 4: Click to Browse
1. Navigate to `/upload`
2. Click on the upload zone (not drag)
3. Select PDF from file browser
4. Verify file name and size display
5. Select bank and upload

**Expected Result:** ✓ File browser opens, upload works

### Test 5: Error Handling
1. Stop the backend server
2. Navigate to `/upload`
3. Select PDF and bank
4. Click "Upload"
5. Verify error message displays
6. Verify "Retry Upload" button appears
7. Click retry button
8. Verify form resets

**Expected Result:** ✓ Error handled gracefully

### Test 6: All Supported Banks
Test upload with each bank:
- [ ] HDFC
- [ ] KOTAK
- [ ] SBI
- [ ] ICICI
- [ ] AXIS
- [ ] CUB
- [ ] IDFC

**Expected Result:** ✓ All banks process successfully

### Test 7: Large File Handling
1. Upload a PDF larger than 10MB
2. Verify error message about file size

**Expected Result:** ✓ Large files rejected

### Test 8: Concurrent Uploads
1. Upload a file
2. While processing, try to upload another file
3. Verify upload controls are disabled during processing

**Expected Result:** ✓ Concurrent uploads prevented

### Test 9: Authentication
1. Log out
2. Try to access `/upload` directly
3. Verify redirect to login page

**Expected Result:** ✓ Protected route works

### Test 10: CSV Download Authentication
1. Log in and upload a file
2. Copy the CSV download URL
3. Log out
4. Try to access the CSV URL directly
5. Verify authentication required

**Expected Result:** ✓ CSV download requires authentication

## API Testing with Postman

### Upload PDF
```
POST http://localhost:5000/api/pdf/upload
Headers:
  Authorization: Bearer <token>
Body (form-data):
  pdf: [select file]
  bank: HDFC
```

### Download CSV
```
GET http://localhost:5000/api/pdf/download/<filename>
Headers:
  Authorization: Bearer <token>
```

## Common Issues and Solutions

### Issue: "No PDF file" error
**Solution:** Ensure the form field name is "pdf" (not "file")

### Issue: "Bank required" error
**Solution:** Ensure bank value is uppercase (HDFC, not hdfc)

### Issue: CSV download fails
**Solution:** Check JWT token is valid and not expired

### Issue: Progress bar stuck at 30%
**Solution:** Check backend logs for processing errors

### Issue: Transaction count is 0
**Solution:** Verify PDF format matches expected bank format

## Browser Compatibility Testing
Test on:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

## Mobile Responsiveness Testing
Test on:
- [ ] Mobile portrait (375px)
- [ ] Mobile landscape (667px)
- [ ] Tablet (768px)
- [ ] Desktop (1024px+)

## Performance Testing
- [ ] Upload 1MB PDF: < 2 seconds
- [ ] Upload 5MB PDF: < 5 seconds
- [ ] Upload 10MB PDF: < 10 seconds
- [ ] CSV download: < 1 second

## Accessibility Testing
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast meets WCAG standards
- [ ] Focus indicators visible
- [ ] Error messages announced

## Security Testing
- [ ] SQL injection attempts blocked
- [ ] XSS attempts sanitized
- [ ] File upload size limits enforced
- [ ] File type restrictions enforced
- [ ] Authentication required for all endpoints
- [ ] CSRF protection enabled

## Database Verification
After successful upload, verify in database:
```sql
SELECT * FROM bank_statements 
WHERE processing_status = 'COMPLETED' 
ORDER BY created_at DESC 
LIMIT 1;
```

Check:
- [ ] file_id generated
- [ ] profile_id matches logged-in user
- [ ] bank_name correct
- [ ] file_path exists
- [ ] file_size_bytes > 0
- [ ] processing_status = 'COMPLETED'
- [ ] extracted_csv_path not null
- [ ] error_message is null

## File System Verification
After successful upload, verify:
- [ ] PDF saved in uploads/ directory
- [ ] CSV saved in outputs/ directory
- [ ] Filenames follow naming convention
- [ ] Files have correct permissions

## Regression Testing
After any code changes, re-run:
1. Test 1 (Successful Upload Flow)
2. Test 2 (File Type Validation)
3. Test 3 (Bank Selection Validation)
4. Test 6 (All Supported Banks)

## Test Data
Prepare sample PDFs for each bank:
- HDFC_sample.pdf
- KOTAK_sample.pdf
- SBI_sample.pdf
- ICICI_sample.pdf
- AXIS_sample.pdf
- CUB_sample.pdf
- IDFC_sample.pdf

## Automated Testing (Future)
Consider implementing:
- Unit tests for validation functions
- Integration tests for API endpoints
- E2E tests for complete upload flow
- Visual regression tests for UI
