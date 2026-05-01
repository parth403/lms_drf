// ============================================
// Leave Approval Functions (Manager)
// ============================================

/**
 * Open approve/reject modal
 */
function openApproveRejectModal(leaveId, employeeName, leaveType, startDate, endDate) {
    document.getElementById('action-leave-id').value = leaveId;
    document.getElementById('leave-details').innerHTML = `
        <div class="alert alert-info">
            <strong>${employeeName}</strong> requested <strong>${leaveType}</strong> leave<br>
            From <strong>${startDate}</strong> to <strong>${endDate}</strong>
        </div>
    `;
    approveRejectModal.show();
}

/**
 * Approve leave request
 */
async function approveLeave() {
    const leaveId = document.getElementById('action-leave-id').value;
    console.log('Approving leave ID:', leaveId);

    if (!leaveId) {
        showAlert('Unable to approve leave: invalid request ID.', 'danger');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/leave-request-approve/${leaveId}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: 'approved' })
        });

        console.log('Approve response status:', response.status);

        if (response.ok) {
            const result = await response.json();
            console.log('Approve result:', result);
            showAlert('Leave approved successfully!', 'success');
            approveRejectModal.hide();
            loadPendingLeaves();
            loadLeaveHistory();
        } else {
            const error = await response.json();
            console.log('Approve error response:', error);
            showAlert('Error approving leave: ' + (error.detail || 'Unknown error'), 'danger');
        }
    } catch (error) {
        console.error('Error approving leave:', error);
        showAlert('Error approving leave', 'danger');
    }
}

/**
 * Reject leave request
 */
async function rejectLeave() {
    const leaveId = document.getElementById('action-leave-id').value;
    console.log('Rejecting leave ID:', leaveId);

    if (!leaveId) {
        showAlert('Unable to reject leave: invalid request ID.', 'danger');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/leave-request-approve/${leaveId}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: 'rejected' })
        });

        console.log('Reject response status:', response.status);

        if (response.ok) {
            const result = await response.json();
            console.log('Reject result:', result);
            showAlert('Leave rejected successfully!', 'success');
            approveRejectModal.hide();
            loadPendingLeaves();
            loadLeaveHistory();
        } else {
            const error = await response.json();
            console.log('Reject error response:', error);
            showAlert('Error rejecting leave: ' + (error.detail || 'Unknown error'), 'danger');
        }
    } catch (error) {
        console.error('Error rejecting leave:', error);
        showAlert('Error rejecting leave', 'danger');
    }
}