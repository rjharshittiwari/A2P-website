# A2P Academy Backend - Quick Reference Guide

## 🚀 Start Backend (5 minutes)

```bash
# 1. Navigate to backend folder
cd backend

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Add credentials.json (get from Google Cloud Console)
# Place file: backend/credentials.json

# 4. Run the server
python app.py

# Expected output:
# Starting A2P Academy Backend API...
# Server running on http://localhost:5000
```

---

## 🔗 API Endpoints (Quick Reference)

### Health Check
```bash
GET http://localhost:5000/api/health
```
Response: `{"status": "Backend is running"}`

### Register a Student
```bash
POST http://localhost:5000/api/register
Content-Type: application/json

{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+91 9876543210",
  "course": "Web Development",
  "message": "I want to learn web development"
}
```

### Submit Contact Form
```bash
POST http://localhost:5000/api/contact
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+91 9876543210",
  "subject": "Course Inquiry",
  "message": "I have questions about the courses"
}
```

### Get All Registrations (Admin)
```bash
GET http://localhost:5000/api/registrations
```

### Get All Inquiries (Admin)
```bash
GET http://localhost:5000/api/inquiries
```

### Get User Info (After Login)
```bash
GET http://localhost:5000/auth/user
```

---

## 📁 Key Files & Their Purpose

| File | Purpose |
|------|---------|
| `app.py` | Main Flask API server with all routes |
| `requirements.txt` | Python package dependencies |
| `credentials.json` | Google OAuth credentials (create this) |
| `a2p_academy.db` | SQLite database (auto-created) |
| `/api-helper.js` | Frontend JavaScript to call backend APIs |
| `/admin.html` | Admin dashboard to view submissions |

---

## 🔐 Quick Setup Checklist

- [ ] Python installed? → `python --version` should show 3.8+
- [ ] In correct folder? → `ls requirements.txt` should work
- [ ] Dependencies installed? → `pip install -r requirements.txt`
- [ ] Credentials ready? → `ls credentials.json` should exist
- [ ] Server running? → `python app.py` starts without errors
- [ ] API working? → Visit `http://localhost:5000/api/health` in browser
- [ ] Frontend ready? → Check `api-helper.js` is in root folder
- [ ] Forms connected? → registration.html & contact.html have script tag

---

## 🧪 Test Each Feature (5-10 mins)

### 1. Test Backend Health
```bash
curl http://localhost:5000/api/health
```

### 2. Test Registration POST
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test Student",
    "email": "test@example.com",
    "phone": "+91 9876543210",
    "course": "Python",
    "message": "Test message"
  }'
```

### 3. Test Get Registrations
```bash
curl http://localhost:5000/api/registrations
```

### 4. Test on Website
- Go to `http://localhost:5000` (if serving from root)
- Fill out registration form
- Submit and check for success message
- Visit `/admin.html` to see submitted data

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` |
| `Port 5000 already in use` | Kill other process: `lsof -ti:5000 \| xargs kill -9` |
| `credentials.json not found` | Download from Google Cloud Console and place in `/backend` |
| `CORS error in browser` | Backend CORS is enabled. Check that frontend is on localhost:5000 |
| `Forms not submitting` | Check browser console for JavaScript errors. Verify api-helper.js is loaded |
| `Admin dashboard shows no data` | Ensure backend is running. Check browser console for fetch errors |

---

## 📊 Database Quick Look

### View all registrations:
```bash
sqlite3 a2p_academy.db "SELECT * FROM registrations;"
```

### Count records:
```bash
sqlite3 a2p_academy.db "SELECT COUNT(*) FROM registrations;"
```

### Reset database:
```bash
rm a2p_academy.db
python app.py  # Recreates fresh database
```

---

## 🔑 Key Passwords/Keys

- **Google OAuth Secret:** In `credentials.json` (keep secure!)
- **Database Password:** None (SQLite is file-based)
- **Admin Password:** None yet (add authentication before production)

---

## 📞 Common Questions

**Q: Can I change the port from 5000?**
A: Yes! In `app.py`, change `app.run(debug=True, port=5000)` to your desired port.

**Q: How do I deploy to production?**
A: See `BACKEND_SETUP.md` for detailed deployment guide.

**Q: Can I use a different database?**
A: Yes! SQLite → PostgreSQL migration is mentioned in deployment guide.

**Q: How often should I backup the database?**
A: Daily in production. Use: `cp a2p_academy.db backups/backup_$(date +%s).db`

**Q: Is the admin panel secure?**
A: No! Add authentication before production. See security section in setup guide.

---

## 🎯 Next Steps

1. **Immediate:** Get credentials.json from Google Cloud Console
2. **Quick:** Test all endpoints with curl commands above
3. **Integration:** Connect frontend forms to backend
4. **Admin:** Set up and test admin dashboard
5. **Production:** Follow DEPLOYMENT_CHECKLIST.md when ready

---

## 📚 Full Documentation

- **Setup Guide:** `BACKEND_SETUP.md`
- **Deployment:** `DEPLOYMENT_CHECKLIST.md`
- **Code:** `backend/app.py` (fully commented)
- **Frontend:** `api-helper.js` (with JSDoc comments)

---

**Need help? Check the error logs:**
```bash
# During development, errors print to console
# In production, check server logs:
tail -n 50 /var/log/a2p-api.log
```

**Happy coding! 🚀**
