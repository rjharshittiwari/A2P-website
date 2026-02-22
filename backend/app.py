"""
A2P Academy Backend API
Handles registration, inquiry form submissions, and Google OAuth login
"""

from flask import Flask, request, jsonify, redirect, session
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import secrets

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
    
    # Registration table
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
    try:
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
    except FileNotFoundError:
        return jsonify({'error': 'credentials.json not found. Please set up Google OAuth.'}), 500
    except Exception as e:
        return jsonify({'error': f'OAuth Error: {str(e)}'}), 500

@app.route('/auth/google/callback', methods=['GET'])
def google_callback():
    """Handle Google OAuth callback"""
    try:
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
            # User already exists, update info
            cursor.execute('''
            UPDATE users SET name = ?, profile_picture = ? WHERE google_id = ?
            ''', (user_info['name'], user_info.get('picture'), user_info['id']))
            db.commit()
        
        db.close()
        
        # Store in session
        session['user'] = {
            'email': user_info['email'],
            'name': user_info['name'],
            'picture': user_info.get('picture')
        }
        
        return redirect('/index.html')
    except Exception as e:
        return jsonify({'error': f'Callback Error: {str(e)}'}), 500

@app.route('/auth/logout', methods=['GET'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/auth/user', methods=['GET'])
def get_user():
    """Get current logged in user"""
    if 'user' in session:
        return jsonify({
            'user': session['user'],
            'status': 'logged_in'
        })
    return jsonify({'user': None, 'status': 'not_logged_in'}), 200

# ==================== REGISTRATION ROUTES ====================

@app.route('/api/register', methods=['POST'])
def register_student():
    """Handle student registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Request body is empty'
            }), 400
        
        required_fields = ['full_name', 'email', 'course']
        errors = {}
        
        for field in required_fields:
            if field not in data or not str(data.get(field, '')).strip():
                errors[field] = f'{field} is required'
        
        if errors:
            return jsonify({
                'status': 'error',
                'message': 'Validation failed',
                'errors': errors
            }), 400
        
        # Validate email format
        email = data.get('email', '').strip()
        if '@' not in email or '.' not in email:
            return jsonify({
                'status': 'error',
                'message': 'Invalid email format',
                'errors': {'email': 'Invalid email format'}
            }), 400
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
        INSERT INTO registrations (full_name, email, phone, course, message)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            data['full_name'].strip(),
            email,
            data.get('phone', '').strip(),
            data['course'].strip(),
            data.get('message', '').strip()
        ))
        
        db.commit()
        registration_id = cursor.lastrowid
        db.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Registration submitted successfully!',
            'registration_id': registration_id,
            'data': {
                'id': registration_id,
                'full_name': data['full_name'],
                'email': email,
                'course': data['course']
            }
        }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/registrations', methods=['GET'])
def get_registrations():
    """Get all registrations (for admin panel)"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM registrations ORDER BY created_at DESC')
        registrations = [dict(row) for row in cursor.fetchall()]
        db.close()
        
        return jsonify({
            'status': 'success',
            'count': len(registrations),
            'registrations': registrations
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving registrations: {str(e)}'
        }), 500

# ==================== CONTACT/INQUIRY ROUTES ====================

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Request body is empty'
            }), 400
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        errors = {}
        
        for field in required_fields:
            if field not in data or not str(data.get(field, '')).strip():
                errors[field] = f'{field} is required'
        
        if errors:
            return jsonify({
                'status': 'error',
                'message': 'Validation failed',
                'errors': errors
            }), 400
        
        # Validate email format
        email = data.get('email', '').strip()
        if '@' not in email or '.' not in email:
            return jsonify({
                'status': 'error',
                'message': 'Invalid email format',
                'errors': {'email': 'Invalid email format'}
            }), 400
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
        INSERT INTO contact_inquiries (name, email, phone, subject, message)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            data['name'].strip(),
            email,
            data.get('phone', '').strip(),
            data.get('subject', '').strip(),
            data['message'].strip()
        ))
        
        db.commit()
        inquiry_id = cursor.lastrowid
        db.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Thank you for contacting us. We will get back to you soon!',
            'inquiry_id': inquiry_id,
            'data': {
                'id': inquiry_id,
                'name': data['name'],
                'email': email
            }
        }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500

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
            return jsonify({
                'status': 'success',
                'inquiry': dict(inquiry)
            }), 200
        return jsonify({
            'status': 'error',
            'message': 'Inquiry not found'
        }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving inquiry: {str(e)}'
        }), 500

@app.route('/api/inquiries', methods=['GET'])
def get_all_inquiries():
    """Get all contact inquiries (for admin panel)"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM contact_inquiries ORDER BY created_at DESC')
        inquiries = [dict(row) for row in cursor.fetchall()]
        db.close()
        
        return jsonify({
            'status': 'success',
            'count': len(inquiries),
            'inquiries': inquiries
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving inquiries: {str(e)}'
        }), 500

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT COUNT(*) FROM registrations')
        db.close()
        
        return jsonify({
            'status': 'Backend is running',
            'database': 'connected',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'Backend running but database error',
            'database': 'error',
            'error': str(e)
        }), 503

# ==================== ROOT ROUTES ====================

@app.route('/', methods=['GET'])
def serve_index():
    """Serve the index page"""
    return redirect('/index.html')

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'code': 500
    }), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'status': 'error',
        'message': 'Method not allowed',
        'code': 405
    }), 405

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Starting A2P Academy Backend API...")
    print("=" * 50)
    print("✅ Server running on http://localhost:5000")
    print("✅ Database: a2p_academy.db")
    print("✅ CORS: Enabled for all origins")
    print("📚 API Docs: See API_DOCUMENTATION.md")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
