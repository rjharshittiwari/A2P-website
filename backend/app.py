"""
A2P Academy Backend API
Handles registration, inquiry form submissions, and Google OAuth login
"""

from flask import Flask, request, jsonify, render_template, redirect, session
from flask_cors import CORS
import sqlite3
import os
import json
from datetime import datetime
from functools import wraps
import secrets
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# Database configuration
DATABASE = 'a2p_academy.db'

# Google OAuth Configuration
GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'
GOOGLE_REDIRECT_URI = 'http://localhost:5000/auth/google/callback'

def get_db():
    """Get database connection"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize database with tables"""
    db = get_db()
    cursor = db.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT,
        google_id TEXT UNIQUE,
        profile_picture TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Registration/Inquiry table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        course TEXT,
        message TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Contact inquiries table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contact_inquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        subject TEXT,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'new',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    db.commit()
    db.close()

# Initialize database on startup
if not os.path.exists(DATABASE):
    init_db()

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/auth/google', methods=['GET'])
def google_login():
    """Redirect to Google OAuth consent screen"""
    from google_auth_oauthlib.flow import Flow
    
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['profile', 'email'],
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    session['state'] = state
    return redirect(authorization_url)

@app.route('/auth/google/callback', methods=['GET'])
def google_callback():
    """Handle Google OAuth callback"""
    from google_auth_oauthlib.flow import Flow
    
    state = session.get('state')
    
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['profile', 'email'],
        state=state,
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    user_info = flow.oauth2session.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    
    # Store user in database
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO users (email, name, google_id, profile_picture)
        VALUES (?, ?, ?, ?)
        ''', (user_info['email'], user_info['name'], user_info['id'], user_info.get('picture')))
        db.commit()
    except sqlite3.IntegrityError:
        # User already exists
        cursor.execute('SELECT * FROM users WHERE google_id = ?', (user_info['id'],))
        user = cursor.fetchone()
    
    db.close()
    
    # Store in session
    session['user'] = {
        'email': user_info['email'],
        'name': user_info['name'],
        'picture': user_info.get('picture')
    }
    
    return redirect('/index.html')

@app.route('/auth/logout', methods=['GET'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/auth/user', methods=['GET'])
def get_user():
    """Get current logged in user"""
    if 'user' in session:
        return jsonify(session['user'])
    return jsonify({'error': 'Not logged in'}), 401

# ==================== REGISTRATION ROUTES ====================

@app.route('/api/register', methods=['POST'])
def register_student():
    """Handle student registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'email', 'course']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
        INSERT INTO registrations (full_name, email, phone, course, message)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            data['full_name'],
            data['email'],
            data.get('phone', ''),
            data['course'],
            data.get('message', '')
        ))
        
        db.commit()
        registration_id = cursor.lastrowid
        db.close()
        
        return jsonify({
            'success': True,
            'message': 'Registration submitted successfully!',
            'id': registration_id
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/registrations', methods=['GET'])
def get_registrations():
    """Get all registrations (for admin panel)"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM registrations ORDER BY created_at DESC')
        registrations = [dict(row) for row in cursor.fetchall()]
        db.close()
        
        return jsonify(registrations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== CONTACT/INQUIRY ROUTES ====================

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
        INSERT INTO contact_inquiries (name, email, phone, subject, message)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            data.get('phone', ''),
            data.get('subject', ''),
            data['message']
        ))
        
        db.commit()
        inquiry_id = cursor.lastrowid
        db.close()
        
        return jsonify({
            'success': True,
            'message': 'Your inquiry has been received. We will contact you soon!',
            'id': inquiry_id
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact/<int:inquiry_id>', methods=['GET'])
def get_contact(inquiry_id):
    """Get specific contact inquiry"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM contact_inquiries WHERE id = ?', (inquiry_id,))
        inquiry = cursor.fetchone()
        db.close()
        
        if inquiry:
            return jsonify(dict(inquiry))
        return jsonify({'error': 'Inquiry not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inquiries', methods=['GET'])
def get_all_inquiries():
    """Get all contact inquiries (for admin panel)"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM contact_inquiries ORDER BY created_at DESC')
        inquiries = [dict(row) for row in cursor.fetchall()]
        db.close()
        
        return jsonify(inquiries)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'Backend is running'}), 200

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting A2P Academy Backend API...")
    print("Server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
