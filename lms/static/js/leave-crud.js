/**
 * Submit new leave request
 */
async function applyLeave(e) {
    e.preventDefault();

    const leaveType = document.getElementById('leave-type').value;
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const reason = document.getElementById('reason').value;
    const leaveTypeId = Number(leaveType);
    if (!leaveType || isNaN(leaveTypeId) || !startDate || !endDate || !reason) {
        showAlert('Please fill all fields correctly', 'danger');
        return;
    }

    // Validate dates
    if (new Date(startDate) > new Date(endDate)) {
        showAlert('Start date must be before end date', 'danger');
        return;
    }

    try {
        const payload = {
            leaveType: leaveTypeId,
            startDate: startDate,
            endDate: endDate,
            reason: reason
        };

        const response = await fetch(`${API_BASE}/leave-request-create/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const responseData = await response.json();

        if (response.status === 201) {
            showAlert('Leave request submitted successfully!', 'success');
            document.getElementById('apply-leave-form').reset();
            document.getElementById('leave-type').innerHTML = '<option value="">Select Leave Type</option>';
            loadLeaveTypes();
            setTimeout(() => {
                loadMyLeaves();
                switchSection('my-leaves');
            }, 1000);
        } else {
            // Handle validation errors properly
            let errorMessage = '';
            if (responseData.detail) {
                errorMessage = responseData.detail;
            } else if (typeof responseData === 'object') {
                // Handle field errors
                const errors = Object.entries(responseData);
                errorMessage = errors.map(([field, msgs]) => {
                    const message = Array.isArray(msgs) ? msgs[0] : msgs;
                    return `${field}: ${message}`;
                }).join(' | ');
            } else {
                errorMessage = JSON.stringify(responseData);
            }
            showAlert(errorMessage || 'Error submitting leave request', 'danger');
            console.error('Validation errors:', responseData);
        }
    } catch (error) {
        showAlert('Error submitting leave request: ' + error.message, 'danger');
        console.error('Error:', error);
    }
}

/**
 * Open edit leave modal
 */
function openEditModal(leaveId, startDate, endDate, reason) {
    document.getElementById('edit-leave-id').value = leaveId;
    document.getElementById('edit-start-date').value = startDate;
    document.getElementById('edit-end-date').value = endDate;
    document.getElementById('edit-reason').value = reason;
    editLeaveModal.show();
}

/**
 * Update existing leave request
 */
async function updateLeave(e) {
    e.preventDefault();

    const leaveId = document.getElementById('edit-leave-id').value;
    const startDate = document.getElementById('edit-start-date').value;
    const endDate = document.getElementById('edit-end-date').value;
    const reason = document.getElementById('edit-reason').value;
    try {
        const response = await fetch(`${API_BASE}/my-leaves/${leaveId}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                startDate: startDate,
                endDate: endDate,
                reason: reason
            })
        });
        if (response.ok) {
            const result = await response.json();
            showAlert('Leave request updated successfully!', 'success');
            editLeaveModal.hide();
            loadMyLeaves();
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Error updating leave', 'danger');
        }
    } catch (error) {
        showAlert('Error updating leave', 'danger');
    }
}

/**
 * Delete leave request
 */
async function deleteLeave(leaveId) {
    if (!confirm('Are you sure you want to delete this leave request?')) return;
    try {
        const response = await fetch(`${API_BASE}/my-leaves/${leaveId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        if (response.ok || response.status === 204) {
            const result = await response.text();
            showAlert('Leave request deleted successfully!', 'success');
            loadMyLeaves();
        } else {
            const error = await response.json();
            showAlert('Error deleting leave request', 'danger');
        }
    } catch (error) {
        showAlert('Error deleting leave', 'danger');
    }
}