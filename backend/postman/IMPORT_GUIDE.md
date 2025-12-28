# Postman Import Guide - ExpenseIQ

## Step 1: Import Collection

### Method 1: Import via File

1. **Open Postman**

2. **Click "Import" button** (top left corner)

3. **Select "Files" tab**

4. **Click "Choose Files"**

5. **Navigate to:**
   ```
   MCA\backend\postman\ExpenseIQ_Collection.json
   ```

6. **Select the file and click "Open"**

7. **Click "Import"**

8. **Verify:** You should see "ExpenseIQ API Collection" in the left sidebar with 7 folders:
   - Authentication (6 requests)
   - PDF Upload (2 requests)
   - Transactions (2 requests)
   - Categorization (2 requests)
   - Dashboard (2 requests)
   - Analytics (1 request)
   - Budgets (3 requests)

---

## Step 2: Import Environment

### Method 1: Import via File

1. **Click the "Environments" icon** (left sidebar, looks like an eye icon)

2. **Click "Import"** (or click the gear icon ⚙️ in top right → Manage Environments → Import)

3. **Select "Files" tab**

4. **Click "Choose Files"**

5. **Navigate to:**
   ```
   MCA\backend\postman\ExpenseIQ_Environment.json
   ```

6. **Select the file and click "Open"**

7. **Click "Import"**

8. **Verify:** You should see "ExpenseIQ Environment" in the environments list

---

## Step 3: Activate Environment

1. **Click the environment dropdown** (top right corner, says "No Environment")

2. **Select "ExpenseIQ Environment"**

3. **Verify:** The dropdown should now show "ExpenseIQ Environment"

---

## Step 4: Verify Environment Variables

1. **Click the "Environments" icon** (left sidebar)

2. **Click "ExpenseIQ Environment"**

3. **Verify these variables exist:**
   - `base_url` = `http://localhost:5000`
   - `access_token` = (empty, will be auto-filled after login)
   - `refresh_token` = (empty, will be auto-filled after login)
   - `user_id` = (empty, will be auto-filled after login)
   - `file_id` = (empty, will be auto-filled after PDF upload)
   - `std_csv` = (empty, will be auto-filled after PDF upload)
   - `rej_csv` = (empty, will be auto-filled after PDF upload)
   - `budget_id` = (empty, will be set manually when needed)

---

## Step 5: Test the Setup

### Test 1: Check Collection Structure

1. **Expand "ExpenseIQ API Collection"** in left sidebar

2. **Verify all folders are present:**
   ```
   ✓ Authentication
   ✓ PDF Upload
   ✓ Transactions
   ✓ Categorization
   ✓ Dashboard
   ✓ Analytics
   ✓ Budgets
   ```

### Test 2: Check Variable Usage

1. **Click on any request** (e.g., "Login")

2. **Look at the URL:** Should show `{{base_url}}/api/auth/login`

3. **Hover over `{{base_url}}`:** Should show `http://localhost:5000`

---

## Step 6: First API Test

### Test Login Endpoint

1. **Expand "Authentication" folder**

2. **Click "Login" request**

3. **Verify:**
   - Method: `POST`
   - URL: `{{base_url}}/api/auth/login`
   - Body: Contains username and password

4. **Click "Send"**

5. **Expected Result:**
   - Status: `200 OK` (if user exists)
   - OR Status: `401 Unauthorized` (if user doesn't exist - this is normal)

6. **If 200 OK:**
   - Check "ExpenseIQ Environment" variables
   - `access_token` should be auto-filled
   - `refresh_token` should be auto-filled
   - `user_id` should be auto-filled

---

## Troubleshooting

### Issue: "This collection is empty"

**Solution:**
1. Delete the collection
2. Re-import using the steps above
3. Make sure you're importing `ExpenseIQ_Collection.json` (not a .md file)

### Issue: Variables not showing

**Solution:**
1. Make sure environment is activated (top right dropdown)
2. Re-import environment file
3. Check that file is `ExpenseIQ_Environment.json`

### Issue: {{base_url}} not resolving

**Solution:**
1. Click environment dropdown (top right)
2. Select "ExpenseIQ Environment"
3. Verify `base_url` is set to `http://localhost:5000`

### Issue: 401 Unauthorized on Login

**Solution:**
1. First run "Signup" request to create a user
2. Then run "Login" request

### Issue: Connection refused

**Solution:**
1. Make sure Flask backend is running: `python run.py`
2. Verify it's running on `http://localhost:5000`
3. Check console for any errors

---

## Quick Start Workflow

### Complete Testing Flow:

1. **Import Collection** → ExpenseIQ_Collection.json
2. **Import Environment** → ExpenseIQ_Environment.json
3. **Activate Environment** → Select "ExpenseIQ Environment"
4. **Run Signup** → Create new user
5. **Run Login** → Get access token (auto-saved)
6. **Run other APIs** → Use saved token automatically

---

## Environment Variables Explained

| Variable | Purpose | Auto-filled? |
|----------|---------|--------------|
| `base_url` | Backend API URL | No (set to localhost:5000) |
| `access_token` | JWT authentication token | Yes (after login) |
| `refresh_token` | Token refresh | Yes (after login) |
| `user_id` | User profile ID | Yes (after login/signup) |
| `file_id` | Uploaded PDF statement ID | Yes (after PDF upload) |
| `std_csv` | Standardized CSV filename | Yes (after PDF upload) |
| `rej_csv` | Rejected rows CSV filename | Yes (after PDF upload) |
| `budget_id` | Budget record ID | No (manual) |

---

## Alternative Import Method (If File Import Fails)

### Import Collection via Raw JSON:

1. **Open:** `ExpenseIQ_Collection.json` in a text editor
2. **Copy:** All content (Ctrl+A, Ctrl+C)
3. **Postman:** Click "Import"
4. **Select:** "Raw text" tab
5. **Paste:** JSON content
6. **Click:** "Import"

### Import Environment via Raw JSON:

1. **Open:** `ExpenseIQ_Environment.json` in a text editor
2. **Copy:** All content
3. **Postman:** Click gear icon ⚙️ → Manage Environments → Import
4. **Select:** "Raw text" tab
5. **Paste:** JSON content
6. **Click:** "Import"

---

## Files Location

```
MCA/
└── backend/
    └── postman/
        ├── ExpenseIQ_Collection.json       ← Import this for API requests
        ├── ExpenseIQ_Environment.json      ← Import this for variables
        ├── DASHBOARD_TEST_STEPS.md         ← Testing guide for Dashboard
        ├── ANALYTICS_TEST_STEPS.md         ← Testing guide for Analytics
        └── BUDGET_SAVING_TEST_STEPS.md     ← Testing guide for Budgets
```

---

## Next Steps After Import

1. **Start Flask backend:** `python run.py`
2. **Run Signup:** Create a test user
3. **Run Login:** Get authentication token
4. **Test Dashboard APIs:** Get category spending
5. **Test Analytics APIs:** Forecast savings
6. **Test Budget APIs:** Save and retrieve budgets

---

**Import complete! You're ready to test all APIs.**
