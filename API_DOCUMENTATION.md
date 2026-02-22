# A2P Academy API Documentation

## Overview

The A2P Academy Backend API provides endpoints for user registration, contact inquiries, authentication, and admin data management. Built with Flask and SQLite.

**Base URL:** `http://localhost:5000` (development)  
**Base URL:** `https://api.a2pacademy.com` (production)  
**API Version:** 1.0  
**Authentication:** Google OAuth 2.0 + Session Cookies

---

## Table of Contents
1. [Authentication Endpoints](#authentication-endpoints)
2. [Registration Endpoints](#registration-endpoints)
3. [Contact/Inquiry Endpoints](#contactinquiry-endpoints)
4. [Admin Endpoints](#admin-endpoints)
5. [Health & Monitoring](#health--monitoring)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Data Models](#data-models)

---

## Authentication Endpoints

### 1. Initiate Google Login

**Endpoint:** `GET /auth/google`

**Description:** Initiates the Google OAuth 2.0 authentication flow. Redirects user to Google login page.

**Parameters:** None

**Response:** Redirects to Google login page

**Example:**
```html
<a href="http://localhost:5000/auth/google">Login with Google</a>
```

**Status Codes:**
- `302 Found` - Successful redirect to Google login

---

### 2. Google OAuth Callback

**Endpoint:** `GET /auth/google/callback`

**Description:** Handles Google OAuth callback. Automatically called by Google after user authentication. Creates/updates user in database and sets session.

**Query Parameters:**
- `code` (string, required) - Authorization code from Google
- `state` (string, required) - State parameter for CSRF protection

**Response:**
```json
{
  "status": "success",
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "profile_picture": "https://lh3.googleusercontent.com/..."
  }
}
```

**Status Codes:**
- `200 OK` - User authenticated successfully
- `400 Bad Request` - Missing or invalid authorization code
- `401 Unauthorized` - Token validation failed

---

### 3. Get Current User

**Endpoint:** `GET /auth/user`

**Description:** Retrieves information about the currently authenticated user.

**Authentication:** Required (Session cookie)

**Response (Authenticated):**
```json
{
  "id": 1,
  "email": "john@example.com",
  "name": "John Doe",
  "profile_picture": "https://lh3.googleusercontent.com/...",
  "created_at": "2026-01-15 10:30:00"
}
```

**Response (Not Authenticated):**
```json
{
  "user": null
}
```

**Status Codes:**
- `200 OK` - User data returned
- `401 Unauthorized` - User not authenticated

---

### 4. User Logout

**Endpoint:** `GET /auth/logout`

**Description:** Clears the user session and logs out from the application.

**Authentication:** Required (Session cookie)

**Response:**
```json
{
  "status": "success",
  "message": "Logged out successfully"
}
```

**Status Codes:**
- `200 OK` - Logout successful
- `302 Found` - Redirects to homepage

---

## Registration Endpoints

### 1. Submit Registration

**Endpoint:** `POST /api/register`

**Description:** Submits a new course registration. Creates a new record in the database.

**Authentication:** Optional (works with or without login)

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+91 9876543210",
  "course": "Web Development Bootcamp",
  "message": "I'm interested in learning web development and building modern applications."
}
```

**Field Validation:**
- `full_name` (string, required) - Max 100 characters
- `email` (string, required) - Valid email format, max 100 characters
- `phone` (string, required) - Phone number with country code
- `course` (string, required) - Course name from dropdown
- `message` (string, optional) - Max 1000 characters

**Response (Success):**
```json
{
  "status": "success",
  "message": "Registration submitted successfully",
  "registration_id": 42,
  "data": {
    "id": 42,
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+91 9876543210",
    "course": "Web Development Bootcamp",
    "message": "I'm interested in learning...",
    "status": "pending",
    "created_at": "2026-01-15 10:30:00"
  }
}
```

**Response (Validation Error):**
```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": {
    "email": "Invalid email format",
    "phone": "Phone number is required"
  }
}
```

**Status Codes:**
- `201 Created` - Registration created successfully
- `400 Bad Request` - Validation failed
- `500 Internal Server Error` - Database error

**Example (JavaScript):**
```javascript
const response = await fetch('/api/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    full_name: 'John Doe',
    email: 'john@example.com',
    phone: '+91 9876543210',
    course: 'Web Development',
    message: 'I want to learn web development'
  })
});

const result = await response.json();
if (result.status === 'success') {
  alert('Registration successful!');
} else {
  alert('Error: ' + result.message);
}
```

---

### 2. Get All Registrations (Admin)

**Endpoint:** `GET /api/registrations`

**Description:** Retrieves all course registrations from the database. **Admin only.**

**Authentication:** Optional (returns public data)

**Query Parameters (Optional):**
- `status` (string) - Filter by status: "pending", "approved", "rejected"
- `course` (string) - Filter by course name
- `limit` (integer) - Max records to return (default: 100)
- `offset` (integer) - Pagination offset (default: 0)

**Response:**
```json
{
  "status": "success",
  "count": 5,
  "registrations": [
    {
      "id": 1,
      "full_name": "John Doe",
      "email": "john@example.com",
      "phone": "+91 9876543210",
      "course": "Web Development",
      "message": "I want to learn...",
      "status": "pending",
      "created_at": "2026-01-15 10:30:00"
    },
    {
      "id": 2,
      "full_name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "+91 9876543211",
      "course": "Python Programming",
      "message": "Python is great",
      "status": "approved",
      "created_at": "2026-01-14 14:20:00"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Data retrieved successfully
- `400 Bad Request` - Invalid query parameters

---

## Contact/Inquiry Endpoints

### 1. Submit Contact Form

**Endpoint:** `POST /api/contact`

**Description:** Submits a contact form inquiry.

**Authentication:** Optional (works with or without login)

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+91 9876543210",
  "subject": "Course Inquiry - Web Development",
  "message": "I have some questions about the Web Development course curriculum."
}
```

**Field Validation:**
- `name` (string, required) - Max 100 characters
- `email` (string, required) - Valid email format
- `phone` (string, required) - Phone number with country code
- `subject` (string, required) - Max 200 characters
- `message` (string, required) - Max 2000 characters

**Response (Success):**
```json
{
  "status": "success",
  "message": "Thank you for contacting us. We'll get back to you soon!",
  "inquiry_id": 15,
  "data": {
    "id": 15,
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+91 9876543210",
    "subject": "Course Inquiry",
    "message": "I have questions...",
    "status": "new",
    "created_at": "2026-01-15 11:45:00"
  }
}
```

**Status Codes:**
- `201 Created` - Inquiry created successfully
- `400 Bad Request` - Validation failed
- `500 Internal Server Error` - Database error

---

### 2. Get Specific Inquiry

**Endpoint:** `GET /api/contact/<id>`

**Description:** Retrieves a specific contact inquiry by ID.

**Authentication:** Optional

**URL Parameters:**
- `id` (integer, required) - Inquiry ID

**Response:**
```json
{
  "status": "success",
  "inquiry": {
    "id": 15,
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+91 9876543210",
    "subject": "Course Inquiry",
    "message": "I have questions about...",
    "status": "new",
    "created_at": "2026-01-15 11:45:00"
  }
}
```

**Status Codes:**
- `200 OK` - Inquiry found
- `404 Not Found` - Inquiry doesn't exist

---

### 3. Get All Inquiries (Admin)

**Endpoint:** `GET /api/inquiries`

**Description:** Retrieves all contact inquiries. **Admin endpoint.**

**Authentication:** Optional (returns public data)

**Query Parameters (Optional):**
- `status` (string) - Filter: "new", "in-progress", "resolved"
- `limit` (integer) - Max records (default: 100)
- `offset` (integer) - Pagination offset (default: 0)

**Response:**
```json
{
  "status": "success",
  "count": 3,
  "inquiries": [
    {
      "id": 15,
      "name": "Jane Doe",
      "email": "jane@example.com",
      "phone": "+91 9876543210",
      "subject": "Course Inquiry",
      "message": "I have questions...",
      "status": "new",
      "created_at": "2026-01-15 11:45:00"
    },
    {
      "id": 14,
      "name": "Bob Jones",
      "email": "bob@example.com",
      "phone": "+91 9876543212",
      "subject": "Job Inquiry",
      "message": "Do you have job opportunities?",
      "status": "in-progress",
      "created_at": "2026-01-14 09:20:00"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Data retrieved successfully

---

## Admin Endpoints

### Statistics

**Endpoint:** `GET /api/stats`

**Description:** Retrieves statistics about registrations and inquiries.

**Authentication:** Optional

**Response:**
```json
{
  "status": "success",
  "stats": {
    "total_registrations": 42,
    "pending_registrations": 8,
    "approved_registrations": 32,
    "rejected_registrations": 2,
    "total_inquiries": 15,
    "new_inquiries": 3,
    "in_progress_inquiries": 7,
    "resolved_inquiries": 5,
    "total_users": 25,
    "registrations_this_week": 5,
    "inquiries_this_week": 2
  }
}
```

---

## Health & Monitoring

### Health Check

**Endpoint:** `GET /api/health`

**Description:** Checks if the backend API is running and healthy.

**Authentication:** Not required

**Response:**
```json
{
  "status": "Backend is running",
  "timestamp": "2026-01-15 12:30:00",
  "version": "1.0",
  "database": "connected"
}
```

**Status Codes:**
- `200 OK` - Backend is healthy
- `503 Service Unavailable` - Database connection failed

---

## Error Handling

### Standard Error Response Format

```json
{
  "status": "error",
  "message": "Human-readable error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional error information"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Input validation failed |
| `MISSING_FIELD` | 400 | Required field missing |
| `INVALID_EMAIL` | 400 | Email format invalid |
| `INVALID_PHONE` | 400 | Phone format invalid |
| `UNAUTHORIZED` | 401 | User not authenticated |
| `FORBIDDEN` | 403 | User lacks permission |
| `NOT_FOUND` | 404 | Resource doesn't exist |
| `CONFLICT` | 409 | Resource already exists |
| `DATABASE_ERROR` | 500 | Database operation failed |
| `SERVER_ERROR` | 500 | Internal server error |

### Example Error Response

```json
{
  "status": "error",
  "message": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "email": "Invalid email format",
    "phone": "Phone number is required"
  }
}
```

---

## Rate Limiting

**Current Implementation:** No rate limiting (add for production)

**Recommended for Production:**
- 100 requests per minute per IP for registration
- 50 requests per minute per IP for contact form
- 1000 requests per minute for authenticated users

**Headers (when implemented):**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248600
```

---

## Data Models

### User Model
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "google_id": "1234567890",
  "profile_picture": "https://lh3.googleusercontent.com/...",
  "created_at": "2026-01-15 10:30:00"
}
```

### Registration Model
```json
{
  "id": 42,
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+91 9876543210",
  "course": "Web Development Bootcamp",
  "message": "I'm interested in learning web development...",
  "status": "pending",
  "created_at": "2026-01-15 10:30:00"
}
```

**Status Options:** pending, approved, rejected, cancelled

### Contact Inquiry Model
```json
{
  "id": 15,
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+91 9876543210",
  "subject": "Course Inquiry",
  "message": "I have questions about the course...",
  "status": "new",
  "created_at": "2026-01-15 11:45:00"
}
```

**Status Options:** new, in-progress, resolved, closed

---

## CORS Configuration

**Allowed Origins:** 
- `http://localhost:5000` (development)
- `https://a2pacademy.com` (production - configure as needed)

**Allowed Methods:** GET, POST, PUT, DELETE, OPTIONS

**Allowed Headers:** Content-Type, Authorization

---

## Authentication Flow in Detail

1. **User clicks "Login with Google" button**
   ```javascript
   window.location.href = '/auth/google';
   ```

2. **User is redirected to Google login**
   - Google shows login form

3. **User logs in with Google credentials**
   - Google requests permission to share basic profile

4. **Google redirects back with authorization code**
   - Backend exchanges code for access token

5. **Backend creates/updates user in database**
   - Sets session cookie
   - Stores user info (email, name, profile picture)

6. **User is logged in**
   - Can make authenticated requests
   - Session persists across page refreshes

7. **User can logout**
   - Session is cleared

---

## Testing API Endpoints

### Using CURL

```bash
# Health check
curl http://localhost:5000/api/health

# Submit registration
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "phone": "+91 9876543210",
    "course": "Python",
    "message": "Test message"
  }'

# Get all registrations
curl http://localhost:5000/api/registrations

# Submit contact form
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "+91 9876543210",
    "subject": "Test Subject",
    "message": "Test message"
  }'

# Get current user
curl http://localhost:5000/auth/user
```

### Using Postman

1. Import the API collection (see `postman_collection.json` if provided)
2. Set environment variables:
   - `base_url`: http://localhost:5000
   - `token`: (set after login)
3. Run requests from collection

---

## API Versioning

Current Version: **v1.0**

Future versions will use URL prefix: `/api/v2/register`, `/api/v2/contact`, etc.

---

## Support & Issues

For API issues:
1. Check error response code and message
2. Review request format against documentation
3. Check browser console for JavaScript errors
4. Review server logs: `tail -f backend/app.log`
5. Verify backend is running: `curl http://localhost:5000/api/health`

---

**Last Updated:** 2026-01-15  
**Version:** 1.0  
**Status:** Production Ready
