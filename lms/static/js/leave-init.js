const API_BASE = '/leave';
let editLeaveModal;
let approveRejectModal;

function initializeLeave() {
    // Initialize Bootstrap modals
    editLeaveModal = new bootstrap.Modal(document.getElementById('editLeaveModal'));
    approveRejectModal = new bootstrap.Modal(document.getElementById('approveRejectModal'));

    loadLeaveTypes();
    setupEventListeners();
}

function setupEventListeners() {
    document.querySelectorAll('.nav-item-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            switchSection(link.dataset.section);
        });
    });
}

async function loadDashboardData() {
    if (currentUser.role === 'employee') {
        loadEmployeeDashboard();
    } else if (currentUser.role === 'manager') {
        loadManagerDashboard();
    }
}

async function loadLeaveTypes() {
    try {
        const response = await fetch(`${API_BASE}/leave-types/`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.ok) {
            const types = await response.json();
            const select = document.getElementById('leave-type');
            select.innerHTML = '<option value="">Select Leave Type</option>';

            // Handle both array and paginated responses
            const typeList = Array.isArray(types) ? types : (types.results || []);
            typeList.forEach(type => {
                const option = document.createElement('option');
                option.value = type.id;
                option.textContent = type.name;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading leave types:', error);
    }
}