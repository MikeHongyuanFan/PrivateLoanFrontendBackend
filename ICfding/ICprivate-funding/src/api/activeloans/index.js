import sendRequest from '@/server/sendRequest'

// Active Loans API functions

// Get all active loans with filtering options
export function getActiveLoans(params = {}) {
    return sendRequest({
        url: '/api/applications/active-loans/',
        method: 'get',
        params: params
    })
}

// Get active loan by ID
export function getActiveLoan(id) {
    return sendRequest({
        url: `/api/applications/active-loans/${id}/`,
        method: 'get'
    })
}

// Get active loan by application ID
export function getActiveLoanByApplication(applicationId) {
    return sendRequest({
        url: `/api/applications/active-loans/application/${applicationId}/`,
        method: 'get'
    })
}

// Create new active loan
export function createActiveLoan(data) {
    return sendRequest({
        url: '/api/applications/active-loans/',
        method: 'post',
        data: data
    })
}

// Update active loan
export function updateActiveLoan(id, data) {
    return sendRequest({
        url: `/api/applications/active-loans/${id}/`,
        method: 'put',
        data: data
    })
}

// Patch active loan (partial update)
export function patchActiveLoan(id, data) {
    return sendRequest({
        url: `/api/applications/active-loans/${id}/`,
        method: 'patch',
        data: data
    })
}

// Delete active loan
export function deleteActiveLoan(id) {
    return sendRequest({
        url: `/api/applications/active-loans/${id}/`,
        method: 'delete'
    })
}

// Get active loans alerts (expiry and payment reminders)
export function getActiveLoanAlerts() {
    return sendRequest({
        url: '/api/applications/active-loans/alerts/',
        method: 'get'
    })
}

// Get active loans dashboard statistics
export function getActiveLoanDashboard() {
    return sendRequest({
        url: '/api/applications/active-loans/dashboard/',
        method: 'get'
    })
}

// Deactivate an active loan
export function deactivateActiveLoan(id) {
    return sendRequest({
        url: `/api/applications/active-loans/${id}/deactivate/`,
        method: 'post'
    })
}

// Reactivate an inactive loan
export function reactivateActiveLoan(id) {
    return sendRequest({
        url: `/api/applications/active-loans/${id}/reactivate/`,
        method: 'post'
    })
}

// Send manual alert for a loan
export function sendActiveLoanAlert(id, alertType = 'manual', message = null) {
    return sendRequest({
        url: `/api/applications/active-loans/${id}/send_alert/`,
        method: 'post',
        data: { 
            alert_type: alertType,
            message: message
        }
    })
}

// Active Loan Repayments API functions

// Get repayments for an active loan
export function getActiveLoanRepayments(activeLoanId) {
    return sendRequest({
        url: `/api/applications/active-loans/${activeLoanId}/repayments/`,
        method: 'get'
    })
}

// Add repayment to an active loan
export function addActiveLoanRepayment(activeLoanId, data) {
    return sendRequest({
        url: `/api/applications/active-loans/${activeLoanId}/repayments/`,
        method: 'post',
        data: data
    })
}

// Get all active loan repayments with filtering
export function getAllActiveLoanRepayments(params = {}) {
    return sendRequest({
        url: '/api/applications/active-loan-repayments/',
        method: 'get',
        params: params
    })
}

// Get specific repayment by ID
export function getActiveLoanRepayment(id) {
    return sendRequest({
        url: `/api/applications/active-loan-repayments/${id}/`,
        method: 'get'
    })
}

// Update repayment
export function updateActiveLoanRepayment(id, data) {
    return sendRequest({
        url: `/api/applications/active-loan-repayments/${id}/`,
        method: 'put',
        data: data
    })
}

// Patch repayment (partial update)
export function patchActiveLoanRepayment(id, data) {
    return sendRequest({
        url: `/api/applications/active-loan-repayments/${id}/`,
        method: 'patch',
        data: data
    })
}

// Delete repayment
export function deleteActiveLoanRepayment(id) {
    return sendRequest({
        url: `/api/applications/active-loan-repayments/${id}/`,
        method: 'delete'
    })
}

// Export all functions as API object
export const activeLoansApi = {
    // Active Loans
    getActiveLoans,
    getActiveLoan,
    getActiveLoanByApplication,
    createActiveLoan,
    updateActiveLoan,
    patchActiveLoan,
    deleteActiveLoan,
    getActiveLoanAlerts,
    getActiveLoanDashboard,
    deactivateActiveLoan,
    reactivateActiveLoan,
    sendActiveLoanAlert,
    
    // Repayments
    getActiveLoanRepayments,
    addActiveLoanRepayment,
    getAllActiveLoanRepayments,
    getActiveLoanRepayment,
    updateActiveLoanRepayment,
    patchActiveLoanRepayment,
    deleteActiveLoanRepayment,
} 