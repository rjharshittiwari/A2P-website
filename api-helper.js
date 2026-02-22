/**
 * A2P Academy - Frontend API Helper
 * Handles all API calls to the backend
 */

const API_BASE = 'http://localhost:5000';

// ==================== AUTHENTICATION ====================

async function googleLogin() {
    window.location.href = `${API_BASE}/auth/google`;
}

async function logout() {
    try {
        const response = await fetch(`${API_BASE}/auth/logout`);
        const data = await response.json();
        if (data.success) {
            window.location.reload();
        }
    } catch (error) {
        console.error('Logout error:', error);
    }
}

async function getCurrentUser() {
    try {
        const response = await fetch(`${API_BASE}/auth/user`);
        if (response.ok) {
            return await response.json();
        }
        return null;
    } catch (error) {
        console.error('Error getting user:', error);
        return null;
    }
}

// Update navbar with user info
async function updateUserUI() {
    const user = await getCurrentUser();
    if (user) {
        const loginBtn = document.getElementById('google-login-btn');
        if (loginBtn) {
            loginBtn.innerHTML = `
                <img src="${user.picture}" alt="${user.name}" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px;">
                <span>${user.name}</span>
                <button onclick="logout()" style="margin-left: 10px;">Logout</button>
            `;
        }
    }
}

// ==================== REGISTRATION ====================

async function submitRegistration(formData) {
    try {
        const response = await fetch(`${API_BASE}/api/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('✅ Registration successful! We will contact you soon.');
            return { success: true, data: data };
        } else {
            alert('❌ ' + (data.error || 'Registration failed'));
            return { success: false, error: data.error };
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('❌ Error submitting registration');
        return { success: false, error: error.message };
    }
}

// ==================== CONTACT FORM ====================

async function submitContact(formData) {
    try {
        const response = await fetch(`${API_BASE}/api/contact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('✅ Thank you! Your inquiry has been received. We will contact you soon.');
            return { success: true, data: data };
        } else {
            alert('❌ ' + (data.error || 'Failed to submit inquiry'));
            return { success: false, error: data.error };
        }
    } catch (error) {
        console.error('Contact error:', error);
        alert('❌ Error submitting inquiry');
        return { success: false, error: error.message };
    }
}

// ==================== ADMIN FUNCTIONS ====================

async function getAllRegistrations() {
    try {
        const response = await fetch(`${API_BASE}/api/registrations`);
        if (response.ok) {
            return await response.json();
        }
        return [];
    } catch (error) {
        console.error('Error fetching registrations:', error);
        return [];
    }
}

async function getAllInquiries() {
    try {
        const response = await fetch(`${API_BASE}/api/inquiries`);
        if (response.ok) {
            return await response.json();
        }
        return [];
    } catch (error) {
        console.error('Error fetching inquiries:', error);
        return [];
    }
}

// ==================== HEALTH CHECK ====================

async function checkBackendStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/health`);
        if (response.ok) {
            console.log('✅ Backend is running');
            return true;
        }
    } catch (error) {
        console.warn('⚠️ Backend is not running. Please start the backend server.');
        return false;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    updateUserUI();
    checkBackendStatus();
});
