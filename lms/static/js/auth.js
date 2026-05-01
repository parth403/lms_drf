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
        console.log('Token exists:', !!token);
        console.log('Token value:', token ? token.substring(0, 20) + '...' : 'null');

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

        if (response.status === 403) {
            showAlert('Access denied. Please contact administrator.');
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
 * Update UI with user information
 */
function updateUserDisplay() {
    try {
        if (!currentUser) {
            console.error('Current user is null');
            return;
        }

        const firstName = currentUser.firstName || currentUser.first_name || currentUser.username || 'User';
        const lastName = currentUser.lastName || currentUser.last_name || '';
        const userNameElement = document.getElementById('user-name');
        const userRoleElement = document.getElementById('user-role');

        if (userNameElement) userNameElement.textContent = firstName;
        if (userRoleElement) userRoleElement.textContent = currentUser.role || 'Employee';

        // Profile section
        const profileUsername = document.getElementById('profile-username');
        const profileEmail = document.getElementById('profile-email');
        const profileFirstName = document.getElementById('profile-first-name');
        const profileLastName = document.getElementById('profile-last-name');
        const profileRole = document.getElementById('profile-role');

        if (profileUsername) profileUsername.value = currentUser.username || '';
        if (profileEmail) profileEmail.value = currentUser.email || '';
        if (profileFirstName) profileFirstName.value = firstName || '';
        if (profileLastName) profileLastName.value = lastName || '';
        if (profileRole) profileRole.value = currentUser.role || '';

        console.log('User display updated successfully');
    } catch (error) {
        console.error('Error updating user display:', error);
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
