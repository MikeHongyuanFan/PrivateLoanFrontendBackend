import sendRequest from '@/server/sendRequest';

// Create a new guarantor
export function createGuarantor(data) {
  return sendRequest({
    url: '/api/borrowers/guarantors/',
    method: 'post',
    data
  });
}

// Get list of guarantors with optional filters
export function getGuarantors(params) {
  return sendRequest({
    url: '/api/borrowers/guarantors/',
    method: 'get',
    params
  });
}

// Get a single guarantor by ID
export function getGuarantor(id) {
  return sendRequest({
    url: `/api/borrowers/guarantors/${id}/`,
    method: 'get'
  });
}

// Update a guarantor (PUT method - full update)
export function updateGuarantor(id, data) {
  return sendRequest({
    url: `/api/borrowers/guarantors/${id}/`,
    method: 'put',
    data
  });
}

// Partially update a guarantor (PATCH method)
export function patchGuarantor(id, data) {
  return sendRequest({
    url: `/api/borrowers/guarantors/${id}/`,
    method: 'patch',
    data
  });
}

// Delete a guarantor
export function deleteGuarantor(id) {
  return sendRequest({
    url: `/api/borrowers/guarantors/${id}/`,
    method: 'delete'
  });
}

// Get guarantor assets
export function getGuarantorAssets(guarantorId, params) {
  return sendRequest({
    url: `/api/borrowers/guarantors/${guarantorId}/assets/`,
    method: 'get',
    params
  });
}

// Create guarantor asset
export function createGuarantorAsset(guarantorId, data) {
  return sendRequest({
    url: `/api/borrowers/guarantors/${guarantorId}/assets/`,
    method: 'post',
    data
  });
}

// Get guarantor borrowers
export function getGuarantorBorrowers(guarantorId) {
  return sendRequest({
    url: `/api/borrowers/guarantors/${guarantorId}/borrowers/`,
    method: 'get'
  });
}

// Get guarantor applications
export function getGuarantorApplications(guarantorId) {
  return sendRequest({
    url: `/api/borrowers/guarantors/${guarantorId}/applications/`,
    method: 'get'
  });
}

export const guarantorApi = {
  createGuarantor,
  getGuarantors,
  getGuarantor,
  updateGuarantor,
  patchGuarantor,
  deleteGuarantor,
  getGuarantorAssets,
  createGuarantorAsset,
  getGuarantorBorrowers,
  getGuarantorApplications
};
