import sendRequest from '@/server/sendRequest'

// Get all fees with filtering options
export function getFees(params = {}) {
    return sendRequest({
        url: '/api/documents/fees/',
        method: 'get',
        params: params
    })
}

// Get fees by application ID
export function getFeesByApplication(applicationId, params = {}) {
    return sendRequest({
        url: '/api/documents/fees/',
        method: 'get',
        params: {
            application: applicationId,
            ...params
        }
    })
}

// Get a specific fee by ID
export function getFee(feeId) {
    return sendRequest({
        url: `/api/documents/fees/${feeId}/`,
        method: 'get'
    })
}

// Create a new fee
export function createFee(feeData) {
    return sendRequest({
        url: '/api/documents/fees/',
        method: 'post',
        data: feeData
    })
}

// Update an existing fee
export function updateFee(feeId, feeData) {
    return sendRequest({
        url: `/api/documents/fees/${feeId}/`,
        method: 'put',
        data: feeData
    })
}

// Partially update a fee
export function patchFee(feeId, feeData) {
    return sendRequest({
        url: `/api/documents/fees/${feeId}/`,
        method: 'patch',
        data: feeData
    })
}

// Delete a fee
export function deleteFee(feeId) {
    return sendRequest({
        url: `/api/documents/fees/${feeId}/`,
        method: 'delete'
    })
}

// Mark a fee as paid
export function markFeePaid(feeId, paymentData) {
    return sendRequest({
        url: `/api/documents/fees/${feeId}/mark-paid/`,
        method: 'post',
        data: paymentData
    })
}

export const feesApi = {
    getFees,
    getFeesByApplication,
    getFee,
    createFee,
    updateFee,
    patchFee,
    deleteFee,
    markFeePaid
} 