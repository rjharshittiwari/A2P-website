# A2P Academy - Deployment Checklist

## ✅ Pre-Deployment Verification

### Local Development Testing
- [ ] Python 3.8+ installed and verified
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] Google OAuth credentials.json downloaded and placed in `/backend` folder
- [ ] Backend server starts without errors: `python app.py`
- [ ] Health check endpoint returns 200: GET `/api/health`
- [ ] Database auto-creates on first run: Check for `a2p_academy.db`

### Frontend Integration Testing
- [ ] api-helper.js is present in root directory
- [ ] Registration form submits to backend successfully
- [ ] Contact form submits to backend successfully
- [ ] Admin panel loads data from `/api/registrations` and `/api/inquiries`
- [ ] CSV export functionality works
- [ ] All form validations working (required fields, email format)
- [ ] Error messages display properly to users
- [ ] Success notifications appear after submission

### Backend API Testing
- [ ] POST `/api/register` - Creates registration record
- [ ] POST `/api/contact` - Creates inquiry record
- [ ] GET `/api/registrations` - Returns all registrations as JSON
- [ ] GET `/api/inquiries` - Returns all inquiries as JSON
- [ ] GET `/auth/user` - Returns user info when logged in
- [ ] GET `/auth/google` - Redirects to Google login
- [ ] GET `/auth/logout` - Clears session
- [ ] Database contains records from test submissions

### Database Verification
- [ ] SQLite database created: `a2p_academy.db`
- [ ] Three tables exist: `users`, `registrations`, `contact_inquiries`
- [ ] Schema matches expected structure
- [ ] Sample test data present in tables
- [ ] No duplicate entries
- [ ] Timestamps auto-populate correctly

### Security Checklist (Development)
- [ ] No hardcoded passwords in code
- [ ] No credentials.json in git (add to .gitignore)
- [ ] CORS headers properly configured
- [ ] Input validation on all POST endpoints
- [ ] SQL injection protections in place (parameterized queries)
- [ ] Error messages don't expose system details

---

## 🚀 Production Deployment Steps

### 1. Code Preparation
- [ ] Remove `debug=True` from `app.py`
- [ ] Change `GOOGLE_REDIRECT_URI` to production domain
- [ ] Review and remove console.log() statements from JavaScript
- [ ] Update `api-helper.js` baseURL from `localhost:5000` to prod domain
- [ ] Minify CSS and JavaScript (optional)
- [ ] Enable HTTPS everywhere
- [ ] Create `.env` file with sensitive variables

### 2. Environment Configuration
```bash
# .env file (do NOT commit this)
GOOGLE_CLIENT_SECRET=your_secret_here
DATABASE_PATH=/var/www/a2p_academy.db
ENVIRONMENT=production
DOMAIN=yourdomain.com
```

### 3. Database Migration to Production
- [ ] Backup local SQLite database
- [ ] (Optional) Migrate to PostgreSQL for scalability
- [ ] Test database connection from production server
- [ ] Set proper file permissions: `chmod 600 a2p_academy.db`
- [ ] Set backup schedule (daily recommended)

### 4. Server Setup
- [ ] Provision server (AWS, Azure, DigitalOcean, etc.)
- [ ] Install Python 3.8+
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Install WSGI server: `pip install gunicorn`
- [ ] Create systemd service for auto-start

### 5. Web Server Configuration
- [ ] Configure Nginx or Apache as reverse proxy
- [ ] Set up SSL certificate (Let's Encrypt - free)
- [ ] Configure domain to point to server
- [ ] Test HTTPS connectivity
- [ ] Set up redirects from HTTP to HTTPS

### 6. Google OAuth Configuration
- [ ] Update OAuth redirect URIs in Google Cloud Console
  - Remove `http://localhost:5000/...`
  - Add `https://yourdomain.com/auth/google/callback`
  - Add `https://yourdomain.com/auth/google`
- [ ] Download updated credentials.json
- [ ] Upload to production server
- [ ] Set proper permissions: `chmod 600 credentials.json`

### 7. Testing in Production
- [ ] Access homepage: https://yourdomain.com
- [ ] Test Google login flow
- [ ] Submit registration form, verify in database
- [ ] Submit contact form, verify in database
- [ ] Access admin panel: https://yourdomain.com/admin.html
- [ ] Verify data appears in admin dashboard
- [ ] Test CSV export
- [ ] Monitor server logs for errors

### 8. Monitoring & Logging
- [ ] Set up error logging (Sentry, LogRocket, etc.)
- [ ] Configure server monitoring (Datadog, New Relic, etc.)
- [ ] Set up automated backups (daily)
- [ ] Configure backup storage (AWS S3, etc.)
- [ ] Create uptime monitoring (UptimeRobot, Pingdom)

### 9. Performance Optimization
- [ ] Enable gzip compression
- [ ] Set up CDN for static files
- [ ] Enable database query caching
- [ ] Optimize images
- [ ] Minify CSS/JavaScript
- [ ] Configure browser caching headers

### 10. Security Hardening
- [ ] Add rate limiting to API endpoints
- [ ] Implement CSRF protection
- [ ] Add security headers (HSTS, CSP, X-Frame-Options)
- [ ] Enable SQL injection protection
- [ ] Set up Web Application Firewall (WAF) rules
- [ ] Regular security audits
- [ ] Update dependencies monthly

---

## 🔧 Systemd Service Configuration

Create `/etc/systemd/system/a2p-api.service`:

```ini
[Unit]
Description=A2P Academy Backend API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/a2p-api
ExecStart=/usr/bin/python3 -m gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable a2p-api
sudo systemctl start a2p-api
```

---

## 📊 Post-Deployment Verification

### Week 1 (Monitoring)
- [ ] Daily check of new registrations/inquiries
- [ ] Monitor server resource usage
- [ ] Review error logs
- [ ] Test all form submissions
- [ ] Verify backup processes
- [ ] Check SSL certificate validity

### Week 2-4
- [ ] Analyze traffic patterns
- [ ] Performance optimization if needed
- [ ] Security vulnerability scanning
- [ ] Database maintenance
- [ ] Update dependencies if critical updates available

### Monthly Tasks
- [ ] Full backup and restore test
- [ ] Security audit
- [ ] Performance review
- [ ] Update documentation
- [ ] Plan capacity for next month

---

## 🆘 Common Production Issues

### Issue: Forms not submitting
**Solution:** 
- Check CORS headers in response
- Verify API endpoint URLs in api-helper.js
- Check browser console for JavaScript errors
- Ensure backend is running

### Issue: Database corruption
**Solution:**
- Restore from backup
- Check disk space
- Verify file permissions
- Switch to PostgreSQL if persistent

### Issue: Google login fails
**Solution:**
- Verify credentials.json on server
- Check OAuth redirect URIs in Google Cloud Console
- Check domain SSL certificate
- Review server error logs

### Issue: Slow admin dashboard
**Solution:**
- Add database indexes
- Implement pagination
- Cache data with Redis
- Upgrade server resources

### Issue: High memory usage
**Solution:**
- Increase number of worker processes
- Add load balancer
- Implement caching
- Optimize database queries

---

## 📈 Scaling for Growth

### Stage 1: <1000 registrations
- Single server with SQLite (current)
- Daily backups
- Basic monitoring

### Stage 2: 1000-10000 registrations
- Upgrade to PostgreSQL
- Add caching layer (Redis)
- Implement CI/CD pipeline
- Set up load balancer

### Stage 3: 10000+ registrations
- Database replication
- Multiple application servers
- CDN for static assets
- Real-time analytics
- Email queue system

---

## 💳 Estimated Costs

### Development/Testing
- Google Cloud always free tier: $0
- Local development: $0

### Production (Small Scale)
- Server: $5-20/month (DigitalOcean, Linode)
- Database backups: $10/month
- Monitoring: $0-50/month
- SSL Certificate: $0 (Let's Encrypt)
- **Total: ~$15-70/month**

### Production (Enterprise Scale)
- Server cluster: $100+/month
- Database: $50-200/month
- CDN: $20-100/month
- Monitoring & Analytics: $50-200/month
- Security services: $50-500/month
- **Total: $250-1000+/month**

---

## 📞 Emergency Contacts

### During Production Incidents:
1. Check server status
2. Review error logs
3. Restore from backup if needed
4. Update stakeholders
5. Document incident

---

**Last Updated:** 2026
**Version:** 1.0
**Status:** Ready for Production
