/**
 * Load employee dashboard with leave balance and recent leaves
 */
async function loadEmployeeDashboard() {
    // Load leave balance
    try {
        const response = await fetch(`${API_BASE}/leave-balance/`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        if (response.ok) {
            const balances = await response.json();
            let totalLeaves = 0, usedLeaves = 0;

            // Handle both array and paginated responses
            const balanceList = Array.isArray(balances) ? balances : (balances.results || []);
            balanceList.forEach(balance => {
                totalLeaves += balance.totalLeaves || 0;
                usedLeaves += balance.usedLeaves || 0;
            });

            const remainingLeaves = totalLeaves - usedLeaves;

            const totalElement = document.getElementById('total-leaves-card');
            const usedElement = document.getElementById('used-leaves-card');
            const remainingElement = document.getElementById('remaining-leaves-card');

            if (totalElement) totalElement.textContent = totalLeaves;
            if (usedElement) usedElement.textContent = usedLeaves;
            if (remainingElement) remainingElement.textContent = remainingLeaves;
        } else {
            console.log('Error loading leave balance:', response.status);
        }
    } catch (error) {
        console.error('Error in loadEmployeeDashboard:', error);
    }

    // Load recent leaves
    console.log('Calling loadMyLeaves...');
    loadMyLeaves('recent');
}

/**
 * Load manager dashboard
 */
async function loadManagerDashboard() {
    loadPendingLeaves();
    loadLeaveHistory();
}