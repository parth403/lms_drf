let currentUser = {};
function initializeAuth() {
    // Check if token exists
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login/';
        return;
    }

    getCurrentUser();
}

/**
 * Fetch and load current user data
 */
async function getCurrentUser() {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('/user/profile/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login/';
            return;
        }

        if (response.ok) {
            const userData = await response.json();
            currentUser = userData;
            updateUserDisplay();
            loadDashboardData();
            toggleMenus();
        } else {
            const errorData = await response.text();
            showAlert('Error loading user profile: ' + response.status);
        }
    } catch (error) {
        showAlert('Connection error: ' + error.message + '. Please refresh the page.');
    }
}

/**
 * Update user display information in the dashboard
 */
function updateUserDisplay() {
    const userNameElement = document.getElementById('user-name');
    const userRoleElement = document.getElementById('user-role');

    if (userNameElement) {
        const displayName = currentUser.firstName && currentUser.lastName 
            ? `${currentUser.firstName} ${currentUser.lastName}`
            : currentUser.username || 'User';
        userNameElement.textContent = displayName;
    }

    if (userRoleElement) {
        userRoleElement.textContent = (currentUser.role || 'user').charAt(0).toUpperCase() + (currentUser.role || 'user').slice(1);
    }
}

/**
 * Toggle menu visibility based on user role
 */
function toggleMenus() {
    const isEmployee = currentUser.role === 'employee';
    const isManager = currentUser.role === 'manager';

    document.querySelectorAll('.employee-menu').forEach(el => {
        el.style.display = isEmployee ? '' : 'none';
    });

    document.querySelectorAll('.manager-menu').forEach(el => {
        el.style.display = isManager ? '' : 'none';
    });

    document.querySelectorAll('.employee-content').forEach(el => {
        el.style.display = isEmployee ? 'block' : 'none';
    });

    document.querySelectorAll('.manager-only').forEach(el => {
        el.style.display = isManager ? 'block' : 'none';
    });

    document.querySelectorAll('.manager-content').forEach(el => {
        if (isManager) {
            el.style.removeProperty('display');
        }
    });
}

/**
 * Logout user
 */
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login/';
}
