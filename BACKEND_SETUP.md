# A2P Academy - Complete Backend Setup Guide

## 📋 Project Overview

This is a complete backend system for A2P Academy website with the following features:
- **User Registration & Inquiry Management** via SQLite database
- **Google OAuth 2.0 Login** integration
- **Admin Dashboard** to view all registrations and inquiries
- **RESTful API** for form submissions
- **CSV Export** functionality for data management

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Google OAuth 2.0 credentials

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Google OAuth Setup

1. **Create Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project named "A2P Academy"
   
2. **Enable Google+ API:**
   - APIs & Services → Library
   - Search "Google+ API"
   - Click Enable
   
3. **Create OAuth Credentials:**
   - APIs & Services → Credentials
   - Click "Create Credentials" → OAuth client ID
   - Choose "Web application"
   - Add JavaScript origins: `http://localhost:5000`
   - Add redirect URIs:
     ```
     http://localhost:5000/auth/google/callback
     http://localhost:5000/auth/google
     ```
   - Download JSON file
   
4. **Save credentials:**
   - Save downloaded JSON as `backend/credentials.json`

### Step 3: Run Backend Server

```bash
cd backend
python app.py
```

Expected output:
```
Starting A2P Academy Backend API...
Server running on http://localhost:5000
```

---

## 📁 Project Structure

```
A2P website/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── credentials.json       # Google OAuth credentials (add this)
│   ├── a2p_academy.db        # SQLite database (auto-created)
│   └── README.md             # Backend documentation
├── api-helper.js             # Frontend API client
├── registration.html         # Registration form
├── contact.html              # Contact form
├── admin.html                # Admin dashboard
├── index.html                # Homepage
├── styles.css                # Styling
└── ... (other pages)
```

---

## 🔗 API Endpoints

### Authentication
- **GET** `/auth/google` - Initiate Google login
- **GET** `/auth/google/callback` - Google OAuth callback
- **GET** `/auth/logout` - User logout
- **GET** `/auth/user` - Get current user info

### Registration
- **POST** `/api/register` - Submit registration
  ```json
  {
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+91 9876543210",
    "course": "Web Development",
    "message": "I want to learn..."
  }
  ```
- **GET** `/api/registrations` - Get all registrations (admin)

### Contact/Inquiry
- **POST** `/api/contact` - Submit contact form
  ```json
  {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "+91 9876543210",
    "subject": "Admission Inquiry",
    "message": "I have questions about..."
  }
  ```
- **GET** `/api/contact/<id>` - Get specific inquiry
- **GET** `/api/inquiries` - Get all inquiries (admin)

### Health
- **GET** `/api/health` - Check backend status

---

## 💾 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    google_id TEXT UNIQUE,
    profile_picture TEXT,
    created_at TIMESTAMP
)
```

### Registrations Table
```sql
CREATE TABLE registrations (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    course TEXT,
    message TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP
)
```

### Contact Inquiries Table
```sql
CREATE TABLE contact_inquiries (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    subject TEXT,
    message TEXT NOT NULL,
    status TEXT DEFAULT 'new',
    created_at TIMESTAMP
)
```

---

## 🌐 Frontend Integration

### Include API Helper
```html
<script src="api-helper.js"></script>
```

### Registration Form Submission
```javascript
async function handleRegistration() {
    const result = await submitRegistration({
        full_name: "John Doe",
        email: "john@example.com",
        phone: "+91 9876543210",
        course: "Web Development"
    });
    
    if (result.success) {
        console.log("Registration successful!");
    }
}
```

### Contact Form Submission
```javascript
async function handleContact() {
    const result = await submitContact({
        name: "Jane Doe",
        email: "jane@example.com",
        message: "I have a question..."
    });
    
    if (result.success) {
        console.log("Message sent!");
    }
}
```

### Google Login
```html
<button onclick="googleLogin()">Login with Google</button>
```

---

## 👨‍💼 Admin Panel

Access admin dashboard at `/admin.html`

**Features:**
- View all registrations
- View all contact inquiries
- Real-time statistics
- Export data to CSV
- Filter by status

**Stats Displayed:**
- Total registrations
- Pending registrations
- Total inquiries
- New inquiries

---

## 🔒 Security Considerations

### For Production:

1. **Environment Variables:**
   ```python
   import os
   GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
   DB_PATH = os.environ.get('DATABASE_PATH', 'a2p_academy.db')
   ```

2. **HTTPS Only:**
   - Use HTTPS in production
   - Update `GOOGLE_REDIRECT_URI` to HTTPS

3. **Authentication:**
   - Protect admin panel with login
   - Implement API key authentication
   - Rate limiting on endpoints

4. **Database:**
   - Regular backups
   - Use strong database passwords
   - Encrypt sensitive data

5. **CORS:**
   - Restrict CORS to your domain
   ```python
   CORS(app, origins=["https://yourdomain.com"])
   ```

---

## 📦 Deployment Options

### Option 1: Heroku
```bash
heroku create a2p-academy-api
git push heroku main
```

### Option 2: PythonAnywhere
1. Upload files to PythonAnywhere
2. Configure web app
3. Update WSGI file

### Option 3: AWS/DigitalOcean
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 4: Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:5000", "app:app"]
```

---

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm backend/a2p_academy.db
python backend/app.py  # Recreates database
```

### Google OAuth Issues
- Verify `credentials.json` is in backend folder
- Check redirect URIs match exactly
- Ensure Google+ API is enabled

### CORS Errors
- Backend already has CORS enabled
- Check API base URL in `api-helper.js`
- Verify frontend and backend URLs match

### Connection Issues
```bash
# Check if backend is running
curl http://localhost:5000/api/health

# Should return: {"status": "Backend is running"}
```

---

## 📊 Monitoring & Logs

View recent requests:
```bash
tail -f backend/app.log
```

Monitor database:
```python
import sqlite3
conn = sqlite3.connect('backend/a2p_academy.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM registrations")
print(cursor.fetchone())
```

---

## 🔄 Backup Strategy

### Automatic Backups
```bash
#!/bin/bash
# backup.sh
cp backend/a2p_academy.db backups/a2p_academy_$(date +%Y%m%d_%H%M%S).db
```

### Schedule with Cron
```bash
0 2 * * * /path/to/backup.sh  # Daily at 2 AM
```

---

## 📞 Support & Maintenance

### Regular Tasks:
- Monitor database size
- Clear old records (optional)
- Update dependencies
- Review error logs
- Test API endpoints

### Weekly Checklist:
- ✅ Backup database
- ✅ Review new registrations
- ✅ Check error logs
- ✅ Test admin panel
- ✅ Verify email notifications

---

## 📝 License & Credits

Created for A2P Academy
© 2026 All Rights Reserved

---

## 📧 Contact

For issues or questions:
- Email: support@a2pacademy.com
- Phone: +918696023635

---

**Happy deploying! 🚀**
