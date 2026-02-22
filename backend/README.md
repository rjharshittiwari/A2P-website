# A2P Academy - Backend Configuration Guide

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Google OAuth Setup

#### Get Google OAuth Credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project called "A2P Academy"
3. Enable the Google+ API:
   - Go to "APIs & Services" > "Libraries"
   - Search for "Google+ API"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Web application"
   - Add authorized redirect URIs:
     - `http://localhost:5000/auth/google/callback`
     - `http://yourdomain.com/auth/google/callback` (for production)
   - Download the credentials as JSON
5. Save the JSON file as `credentials.json` in the backend folder

### 3. Update Frontend to Use Backend

In your HTML files, update forms to submit to these endpoints:

**Registration Form:**
```javascript
fetch('/api/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        full_name: document.getElementById('full_name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        course: document.getElementById('course').value
    })
})
.then(response => response.json())
.then(data => console.log(data))
```

**Contact Form:**
```javascript
fetch('/api/contact', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value
    })
})
```

### 4. Run the Backend

```bash
python app.py
```

Backend will run on: `http://localhost:5000`

### 5. Database

- SQLite database created automatically: `a2p_academy.db`
- Contains tables for:
  - Users (from Google OAuth)
  - Registrations
  - Contact Inquiries

### API Endpoints

#### Authentication
- `GET /auth/google` - Initiate Google login
- `GET /auth/google/callback` - Google OAuth callback
- `GET /auth/logout` - Logout user
- `GET /auth/user` - Get current logged in user

#### Registration
- `POST /api/register` - Submit registration form
- `GET /api/registrations` - Get all registrations (admin)

#### Contact
- `POST /api/contact` - Submit contact form
- `GET /api/contact/<id>` - Get specific inquiry
- `GET /api/inquiries` - Get all inquiries (admin)

#### Health
- `GET /api/health` - Check if backend is running

### Production Deployment

For production, update:
1. `GOOGLE_REDIRECT_URI` to your production domain
2. `app.run(debug=False)` - Disable debug mode
3. Use a production WSGI server like Gunicorn
4. Add environment variables for sensitive data
5. Use HTTPS

### Troubleshooting

- **Database error**: Delete `a2p_academy.db` and restart
- **Google OAuth issues**: Ensure credentials.json is in backend folder
- **CORS errors**: Backend already has CORS enabled
