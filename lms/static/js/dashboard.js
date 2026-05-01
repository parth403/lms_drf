if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeDashboard);
} else {
    initializeDashboard();
}

function initializeDashboard() {
    initializeAuth();
    initializeLeave();
}

/**
 * Switch between dashboard sections
 */
function switchSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });

    // Show selected section
    document.getElementById(sectionId).classList.add('active');

    // Update active nav link
    document.querySelectorAll('.nav-item-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`[data-section="${sectionId}"]`).classList.add('active');

    // Update page title if element exists
    const pageTitle = document.getElementById('page-title');
    if (pageTitle) {
        const titles = {
            'dashboard': 'Dashboard',
            'apply-leave': 'Apply Leave',
            'my-leaves': 'My Leaves',
            'leave-balance': 'Leave Balance',
            'pending-leaves': 'Pending Leaves',
            'leave-history': 'Leave History',
            'profile': 'Profile'
        };
        pageTitle.textContent = titles[sectionId] || 'Dashboard';
    }

    // Load data based on section
    if (sectionId === 'leave-balance') {
        loadLeaveBalance();
    } else if (sectionId === 'my-leaves') {
        loadMyLeaves();
    } else if (sectionId === 'pending-leaves') {
        loadPendingLeaves();
    } else if (sectionId === 'leave-history') {
        loadLeaveHistory();
    }
}
/**
 * Display alert message
 */
function showAlert(message, type = 'info') {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="bi bi-exclamation-circle"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const container = document.getElementById('alert-container');
    container.innerHTML = alertHTML;

    setTimeout(() => {
        container.innerHTML = '';
    }, 5000);
}
