# A2P Academy - Testing Guide & QA Checklist

## 📋 Overview

This guide provides comprehensive testing procedures for the A2P Academy backend, frontend integration, and deployment validation.

---

## 🧪 Unit Testing Checklist

### Backend API Testing

#### 1. Health Check Endpoint
```bash
# Test: Backend is running
curl http://localhost:5000/api/health

# Expected Response:
{
  "status": "Backend is running",
  "database": "connected"
}

# Verify:
✅ Response code is 200
✅ Database shows "connected"
✅ Timestamp is current
```

#### 2. Registration Endpoint

**Test 2.1: Valid Registration**
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Test",
    "email": "john.test@example.com",
    "phone": "+91 9876543210",
    "course": "Web Development",
    "message": "I want to learn web dev"
  }'
```

**Expected:** 201 Created with registration_id

**Verify:**
- ✅ Registration ID returned
- ✅ Status is "pending"
- ✅ All fields stored correctly
- ✅ Timestamp auto-populated

**Test 2.2: Missing Required Field**
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Test",
    "email": "john.test@example.com",
    "phone": "+91 9876543210"
    # missing course and message
  }'
```

**Expected:** 400 Bad Request

**Verify:**
- ✅ Error message shown
- ✅ Validation errors listed
- ✅ No record created in database

**Test 2.3: Invalid Email Format**
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Test",
    "email": "invalid-email",
    "phone": "+91 9876543210",
    "course": "Python",
    "message": "Test"
  }'
```

**Expected:** 400 Bad Request

**Verify:**
- ✅ Email validation error shown
- ✅ No record created

**Test 2.4: Duplicate Registration**
```bash
# First submission (should succeed)
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+91 9876543210",
    "course": "Python",
    "message": "Test"
  }'

# Second with same email (behavior depends on implementation)
# Current: Allows multiple registrations per email
# Check database: Should have both records
```

#### 3. Contact Form Endpoint

**Test 3.1: Valid Contact Submission**
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Inquiry",
    "email": "jane.inquiry@example.com",
    "phone": "+91 9876543211",
    "subject": "Course Price Question",
    "message": "What is the price of the Python course?"
  }'
```

**Expected:** 201 Created

**Verify:**
- ✅ Inquiry ID returned
- ✅ Status is "new"
- ✅ All fields stored
- ✅ Timestamp auto-populated

**Test 3.2: Long Message**
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+91 9876543210",
    "subject": "Detailed Inquiry",
    "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit... [long text up to 2000 chars]"
  }'
```

**Verify:**
- ✅ Full message stored
- ✅ No truncation
- ✅ Response successful

#### 4. Retrieve Data Endpoints

**Test 4.1: Get All Registrations**
```bash
curl http://localhost:5000/api/registrations

# Expected: Array of all registration records
```

**Verify:**
- ✅ Returns all registrations
- ✅ All fields present
- ✅ Correct count

**Test 4.2: Get All Inquiries**
```bash
curl http://localhost:5000/api/inquiries

# Expected: Array of all inquiry records
```

**Verify:**
- ✅ Returns all inquiries
- ✅ All fields present
- ✅ Correct count

#### 5. Authentication Endpoints

**Test 5.1: Google Login Flow**
```javascript
// In browser console at http://localhost:5000
window.location.href = '/auth/google';

// Expected:
// 1. Redirects to Google login
// 2. After Google approval, redirects back
// 3. Session/cookie set
// 4. User logged in
```

**Verify:**
- ✅ Google login redirects correctly
- ✅ User data retrieved from Google
- ✅ User created in database
- ✅ Session cookie set

**Test 5.2: Get Current User**
```bash
# After login, test:
curl http://localhost:5000/auth/user

# Expected: User object with email, name, profile_picture
```

**Verify:**
- ✅ User info returned
- ✅ All fields present
- ✅ Google profile picture URL valid

**Test 5.3: Logout**
```bash
curl http://localhost:5000/auth/logout

# Expected: Success message
```

**Verify:**
- ✅ Session cleared
- ✅ User cannot access protected endpoints after logout

---

## 🖥️ Frontend Integration Testing

### Registration Form Testing

**Test 1: Form Submission Success**
```javascript
// In browser console on /registration.html
1. Fill form with valid data:
   - First Name: John
   - Last Name: Doe
   - Email: john@example.com
   - Phone: +91 9876543210
   - Course: Web Development
   - Message: I want to learn

2. Click Submit

3. Verify:
   ✅ Form submits without page reload
   ✅ Success message appears
   ✅ Form clears or shows confirmation
   ✅ Data appears in admin.html dashboard
```

**Test 2: Form Validation**
```javascript
// Leave email field empty, click submit
✅ Error message appears: "Email is required"
✅ Form does NOT submit to server
✅ Required fields highlighted

// Enter invalid email "abc123"
✅ Error message appears: "Invalid email format"
✅ Form does NOT submit
```

**Test 3: Long Form Fields**
```javascript
// Test with maximum length inputs:
Message: 1000+ characters
✅ Accepts without truncation
✅ Submits successfully
✅ Stored correctly in database
```

**Test 4: Special Characters**
```javascript
// Submit with special characters:
Name: "José García-López"
Message: "I'm interested & excited!"
✅ Accepted and stored correctly
✅ No injection attacks
✅ Data displayed correctly in admin
```

### Contact Form Testing

**Test 1: Contact Form Submission**
```javascript
// Navigate to /contact.html
1. Fill form:
   - Name: Jane Smith
   - Email: jane@example.com
   - Phone: +91 9876543211
   - Subject: Course Inquiry
   - Message: When does the course start?

2. Click Submit

3. Verify:
   ✅ Success message shown
   ✅ Form clears
   ✅ Data in admin.html
   ✅ Status shows "new"
```

**Test 2: Multiple Submissions Same Email**
```javascript
// Submit contact form twice with same email
1. First submission - Success ✅
2. Second submission - Also succeeds (allows multiple)
3. Verify both appear in admin panel
```

### Admin Dashboard Testing

**Test 1: Dashboard Loads**
```javascript
// Open /admin.html
✅ Page loads without errors
✅ Tabs visible (Registrations, Inquiries)
✅ Statistics boxes show numbers
✅ Tables not empty (if data exists)
```

**Test 2: Tab Switching**
```javascript
// Click "Registrations" tab
✅ Registration data displays
✅ Correct columns shown

// Click "Inquiries" tab
✅ Inquiry data displays
✅ Different columns shown

// Switch back to Registrations
✅ Data remains the same
```

**Test 3: Statistics Display**
```javascript
// Verify statistics boxes show:
✅ Total Registrations: Correct count
✅ Pending Registrations: Active count
✅ Total Inquiries: Correct count
✅ New Inquiries: Unread count
```

**Test 4: CSV Export**
```javascript
// Click "Export CSV" for Registrations
1. File download starts
2. Open downloaded file
3. Verify:
   ✅ CSV format correct
   ✅ All columns present
   ✅ All rows included
   ✅ Data intact (no corruption)

// Repeat for Inquiries export
```

**Test 5: Data Refresh**
```javascript
// Click "Refresh Data" button
✅ Data reloads from server
✅ Statistics update
✅ New records appear

// Or wait 30 seconds (auto-refresh)
✅ Data auto-refreshes
✅ New submissions appear
```

---

## 🌍 Browser Compatibility Testing

### Desktop Browsers
- [ ] Chrome (Latest)
- [ ] Firefox (Latest)
- [ ] Safari (Latest)
- [ ] Edge (Latest)

### Mobile Browsers
- [ ] Chrome Mobile
- [ ] Safari Mobile
- [ ] Firefox Mobile

### Test Checklist per Browser
```
✅ Registration form responsive
✅ Contact form responsive
✅ Admin dashboard usable
✅ CSS displays correctly
✅ Forms submit successfully
✅ No console errors
```

---

## ⚡ Performance Testing

### Backend Performance

**Test 1: Response Time**
```bash
# Measure response time for registration
time curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test","email":"test@example.com",...}'

# Expected: < 500ms
```

**Test 2: Load Testing (Basic)**
```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:5000/api/health

# Verify: No errors, good response rate
```

**Test 3: Database Query Performance**
```bash
# Get all registrations with 1000+ records
curl http://localhost:5000/api/registrations

# Expected: < 2 seconds response
```

---

## 🔒 Security Testing

### Test 1: SQL Injection Prevention
```bash
# Try SQL injection in email field
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test",
    "email": "test@example.com\"; DROP TABLE registrations;--",
    "phone": "+91 9876543210",
    "course": "Python",
    "message": "Test"
  }'

# Expected: ✅ Rejected or safely handled
# Verify: ✅ Database not affected
```

### Test 2: XSS Prevention
```bash
# Try XSS in message field
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "email": "test@example.com",
    "phone": "+91 9876543210",
    "subject": "Test",
    "message": "<script>alert(\"XSS\")</script>"
  }'

# Expected: ✅ Script tags escaped/removed
# Verify: ✅ No alert when viewing in admin
```

### Test 3: CORS Security
```bash
# Try request from different domain
# From browser console on different site:
fetch('http://localhost:5000/api/registrations')
  .then(r => r.json())

# Expected: ✅ CORS headers allow/deny appropriately
```

### Test 4: Session Security
```bash
1. Login as user
2. Get session cookie
3. Clear cookie in DevTools
4. Try accessing protected endpoints
5. Expected: ✅ Unauthorized error or redirect to login
```

---

## 📱 Mobile & Responsive Design

### Test 1: Registration Form Responsiveness
```
✅ iPhone SE (375px): Form readable, clickable
✅ iPhone 12 (390px): All fields visible
✅ iPhone 12 Pro Max (428px): Optimal layout
✅ Android phones: Responsive design
✅ Tablet (iPad): Good spacing
```

### Test 2: Admin Dashboard Responsiveness
```
✅ Mobile (375px): Tables scrollable, functional
✅ Tablet (768px): Good layout
✅ Desktop (1920px): Full featured
```

---

## 🔄 Database Testing

### Test 1: Data Persistence
```sql
-- After submitting registration:
sqlite3 a2p_academy.db "SELECT * FROM registrations;" 
-- Expected: Record exists with all data

-- After logging out and in:
sqlite3 a2p_academy.db "SELECT * FROM users;"
-- Expected: User record exists
```

### Test 2: Database Integrity
```sql
-- Check for NULL values in required fields:
sqlite3 a2p_academy.db "SELECT * FROM registrations WHERE email IS NULL;"
-- Expected: Empty result (no NULLs in required fields)

-- Check timestamps:
sqlite3 a2p_academy.db "SELECT created_at FROM registrations LIMIT 5;"
-- Expected: Valid timestamps
```

### Test 3: Database Backup
```bash
# Create backup
cp a2p_academy.db a2p_academy_backup.db

# Restore from backup
cp a2p_academy_backup.db a2p_academy.db

# Verify data intact
sqlite3 a2p_academy.db "SELECT COUNT(*) FROM registrations;"
```

---

## 📊 Staging Environment Testing

Before production deployment:

```
✅ All unit tests pass
✅ All integration tests pass
✅ Performance tests acceptable
✅ Security tests pass
✅ Cross-browser compatibility verified
✅ Mobile responsiveness confirmed
✅ Database backup/restore tested
✅ Monitoring set up and working
✅ Logging configured
✅ Error handling verified
✅ Load testing (if applicable)
✅ 24-hour stability test passed
```

---

## 🚨 Error Scenario Testing

### Test 1: Backend Down
```javascript
// Stop backend server
// Try to submit form on frontend
✅ User sees error message
✅ Not blocked (useful UX)
✅ Can retry when backend up
```

### Test 2: Database Down
```bash
# Move database file
mv a2p_academy.db a2p_academy.db.bak

# Try to submit form
✅ Backend error returned
✅ User sees error message

# Restore database
mv a2p_academy.db.bak a2p_academy.db
```

### Test 3: Invalid Credentials
```javascript
// Manually corrupt credentials.json
// Try to login with Google
✅ User sees helpful error
✅ Application handles gracefully
```

---

## ✅ Final Acceptance Criteria

Before marking as "Ready for Production":

### Functional Requirements
- [ ] All CRUD operations work (Create, Read, Update, Delete where applicable)
- [ ] Forms submit successfully
- [ ] Admin panel displays all data
- [ ] Google OAuth works
- [ ] CSV export works
- [ ] Data persists across sessions

### Non-Functional Requirements
- [ ] Response time < 500ms for form submissions
- [ ] Admin dashboard loads < 2s
- [ ] 99% API uptime
- [ ] Database consistency
- [ ] No security vulnerabilities

### User Experience
- [ ] Clear error messages
- [ ] Smooth form submission
- [ ] Fast page loads
- [ ] Intuitive navigation
- [ ] Mobile friendly

### Documentation
- [ ] Setup guide complete
- [ ] API documentation complete
- [ ] Deployment guide complete
- [ ] Testing guide complete (this file)

---

## 📋 QA Sign-Off Checklist

```
Date: _______________
Tester: _____________
Build Version: ______

Functional Testing:        ✅ / ❌
Integration Testing:       ✅ / ❌
Performance Testing:       ✅ / ❌
Security Testing:          ✅ / ❌
Compatibility Testing:     ✅ / ❌
Database Testing:          ✅ / ❌
User Acceptance Testing:   ✅ / ❌

Overall Status:            PASS / FAIL
Ready for Production:      YES / NO

Notes: _______________________________________________

Signed: _______________________________________________
```

---

## 🐛 Reporting Bugs

When testing finds issues, report them as:

```markdown
**Bug ID:** BUG-001
**Severity:** High / Medium / Low
**Title:** Form submission fails with special characters
**Environment:** Firefox 95 on macOS
**Steps to Reproduce:**
1. Go to /registration.html
2. Enter name: "José García"
3. Click submit

**Expected:** Form submits successfully
**Actual:** Error: "Invalid character"
**Attached:** Screenshot, browser console errors
```

---

**Happy Testing! 🚀**
