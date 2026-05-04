/**
 * Load user's leave requests
 */
async function loadMyLeaves(type = 'all') {
    try {
        const url = `${API_BASE}/my-leaves/`;
        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.ok) {
            const leaves = await response.json();
            if (leaves.length > 0) {
                console.log('First leave object:', JSON.stringify(leaves[0], null, 2));
            }

            const tbody = type === 'recent' ?
                document.getElementById('recent-leaves-tbody') :
                document.getElementById('my-leaves-tbody');

            tbody.innerHTML = '';

            if (!leaves || leaves.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="7" class="text-center text-muted py-4">
                            <i class="bi bi-inbox" style="font-size: 30px; opacity: 0.5;"></i>
                            <p>No leaves</p>
                        </td>
                    </tr>
                `;
                return;
            }

            const displayLeaves = type === 'recent' ? leaves.slice(0, 5) : leaves;

            displayLeaves.forEach(leave => {
                // Get dates and leave type using camelCase keys (from DRF camel-case renderer)
                const startDateStr = leave.startDate || 'N/A';
                const endDateStr = leave.endDate || 'N/A';
                const leaveTypeName = leave.leaveTypeName || 'Unknown';

                // Calculate days
                let days = 'N/A';
                if (leave.startDate && leave.endDate) {
                    try {
                        const [startY, startM, startD] = leave.startDate.split('-').map(Number);
                        const [endY, endM, endD] = leave.endDate.split('-').map(Number);
                        const start = new Date(startY, startM - 1, startD);
                        const end = new Date(endY, endM - 1, endD);
                        days = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
                    } catch (e) {
                        console.warn('Error calculating days:', e);
                        days = 'N/A';
                    }
                }

                const appliedDate = leave.appliedAt ? new Date(leave.appliedAt).toLocaleDateString() : 'N/A';
                const statusBadge = `<span class="badge ${leave.status}">${leave.status}</span>`;

                let actions = '';
                if (leave.status === 'pending') {
                    actions = `
                        <button class="action-btn action-btn-edit" onclick="openEditModal(${leave.id}, '${leave.startDate}', '${leave.endDate}', '${(leave.reason || '').replace(/'/g, "\\'")}')">
                            <i class="bi bi-pencil"></i> Edit
                        </button>
                        <button class="action-btn action-btn-delete" onclick="deleteLeave(${leave.id})">
                            <i class="bi bi-trash"></i> Delete
                        </button>
                    `;
                }

                const cols = type === 'recent' ? 6 : 7;
                const reasonCol = type === 'recent' ? '' : `<td>${(leave.reason || '').substring(0, 30)}</td>`;
                const extraCol = type === 'recent' ? `<td>${appliedDate}</td>` : `<td>${actions}</td>`;

                tbody.innerHTML += `
                    <tr>
                        <td>${leaveTypeName}</td>
                        <td>${startDateStr}</td>
                        <td>${endDateStr}</td>
                        <td>${days}</td>
                        <td>${statusBadge}</td>
                        ${reasonCol}
                        ${extraCol}
                    </tr>
                `;
            });
        } else {
            console.log('Error response:', response.status);
            showAlert('Error loading leaves', 'danger');
        }
    } catch (error) {
        showAlert('Error loading leaves: ' + error.message, 'danger');
        console.error('Error loading leaves:', error);
    }
}

/**
 * Load user's leave balance
 */
async function loadLeaveBalance() {
    try {
        const response = await fetch(`${API_BASE}/leave-balance/`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.ok) {
            const balances = await response.json();
            const tbody = document.getElementById('leave-balance-tbody');
            tbody.innerHTML = '';

            if (!balances || balances.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="5" class="text-center text-muted py-4">No leave balance data</td>
                    </tr>
                `;
                return;
            }

            // Handle both array and paginated responses
            const balList = Array.isArray(balances) ? balances : (balances.results || []);
            balList.forEach(balance => {
                tbody.innerHTML += `
                    <tr>
                        <td><strong>${balance.leaveTypeName}</strong></td>
                        <td>${balance.totalLeaves}</td>
                        <td>${balance.usedLeaves}</td>
                        <td>${balance.remainingLeaves}</td>
                    </tr>
                `;
            });
        } else {
            const tbody = document.getElementById('leave-balance-tbody');
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-danger">Error loading leave balance</td>
                </tr>
            `;
        }
    } catch (error) {
        const tbody = document.getElementById('leave-balance-tbody');
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-danger">Error: ${error.message}</td>
            </tr>
        `;
    }
}

/**
 * Load pending leaves for manager
 */
async function loadPendingLeaves() {
    try {
        const response = await fetch(`${API_BASE}/pending-leaves/`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });

        console.log('Pending leaves response status:', response.status);

        if (response.ok) {
            const leaves = await response.json();
            const tbody = document.getElementById('pending-leaves-tbody');
            tbody.innerHTML = '';

            // Update pending count
            document.getElementById('pending-leaves-card').textContent = leaves.length;

            if (!leaves || leaves.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="8" class="text-center text-muted py-4">
                            <i class="bi bi-inbox" style="font-size: 30px; opacity: 0.5;"></i>
                            <p>No pending leave requests</p>
                        </td>
                    </tr>
                `;
                return;
            }

            leaves.forEach(leave => {
                const startDate = new Date(leave.startDate).toLocaleDateString();
                const endDate = new Date(leave.endDate).toLocaleDateString();
                const appliedDate = new Date(leave.appliedAt).toLocaleDateString();
                const days = Math.ceil((new Date(leave.endDate) - new Date(leave.startDate)) / (1000 * 60 * 60 * 24)) + 1;
                const reason = leave.reason ? leave.reason.substring(0, 30) : '';
                // const approvedBy=leave.approvedBy || '-';

                tbody.innerHTML += `
                    <tr>
                        <td><strong>${leave.employeeName}</strong></td>
                        <td>${leave.leaveTypeName || leave.leaveType}</td>
                        <td>${startDate}</td>
                        <td>${endDate}</td>
                        <td>${days}</td>
                        <td>${reason}...</td>
                        <td>${appliedDate}</td>
                            <td>
                            <button class="action-btn action-btn-approve" onclick="openApproveRejectModal(${leave.id}, '${leave.employeeName.replace(/'/g, "\\'")}', '${(leave.leaveTypeName || '').replace(/'/g, "\\'")}', '${startDate}', '${endDate}')">
                                <i class="bi bi-check-circle"></i> Action
                            </button>
                        </td>
                    </tr>
                `;
            });
        }
    } catch (error) {
        console.error('Error loading pending leaves:', error);
    }
}

/**
 * Load leave history for manager
 */
async function loadLeaveHistory() {
    try {
        const response = await fetch(`${API_BASE}/all-leave-request`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        if (response.ok) {
            const leaves = await response.json();
            const tbody = document.getElementById('leave-history-tbody');
            tbody.innerHTML = '';

            if (!leaves || leaves.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="8" class="text-center text-muted py-4">No leave history</td>
                    </tr>
                `;
                return;
            }

            leaves.forEach(leave => {
                const startDate = new Date(leave.startDate).toLocaleDateString();
                const endDate = new Date(leave.endDate).toLocaleDateString();
                const appliedDate = new Date(leave.appliedAt).toLocaleDateString();
                const days = Math.ceil((new Date(leave.endDate) - new Date(leave.startDate)) / (1000 * 60 * 60 * 24)) + 1;
                const statusBadge = `<span class="badge ${leave.status}">${leave.status}</span>`;

                tbody.innerHTML += `
                    <tr>
                        <td><strong>${leave.employeeName}</strong></td>
                        <td>${leave.leaveTypeName || leave.leaveType}</td>
                        <td>${startDate}</td>
                        <td>${endDate}</td>
                        <td>${days}</td>
                        <td>${statusBadge}</td>
                        <td>${leave.approvedBy || '-'}</td>
                        <td>${appliedDate}</td>
                    </tr>
                `;
            });
        } else {
            console.log('Error loading leave history:', response.status);
        }
    } catch (error) {
        console.error('Error loading leave history:', error);
    }
}