import sendRequest from '@/server/sendRequest';

export const guarantorApi = {
  // Create a new guarantor
  createGuarantor: async (data) => {
    return sendRequest({
      url: '/api/borrowers/guarantors/',
      method: 'post',
      data
    });
  },

  // Get list of guarantors with optional filters
  getGuarantors: async (params) => {
    return sendRequest({
      url: '/api/borrowers/guarantors/',
      method: 'get',
      params
    });
  },

  // Get a single guarantor by ID
  getGuarantor: async (id) => {
    return sendRequest({
      url: `/api/borrowers/guarantors/${id}/`,
      method: 'get'
    });
  },

  // Update a guarantor (PUT method - full update)
  updateGuarantor: async (id, data) => {
    return sendRequest({
      url: `/api/borrowers/guarantors/${id}/`,
      method: 'put',
      data
    });
  },

  // Partially update a guarantor (PATCH method)
  patchGuarantor: async (id, data) => {
    return sendRequest({
      url: `/api/borrowers/guarantors/${id}/`,
      method: 'patch',
      data
    });
  },

  // Delete a guarantor
  deleteGuarantor: async (id) => {
    return sendRequest({
      url: `/api/borrowers/guarantors/${id}/`,
      method: 'delete'
    });
  },

  // Get guarantor assets
  getGuarantorAssets: async (guarantorId, params) => {
    return sendRequest({
      url: `/api/borrowers/guarantors/${guarantorId}/assets/`,
      method: 'get',
      params
    });
  },

  // Create guarantor asset
  createGuarantorAsset: async (guarantorId, data) => {
    return sendRequest({
      url: `/api/borrowers/guarantors/${guarantorId}/assets/`,
      method: 'post',
      data
    });
  },

  // Get a single guarantor asset
  getGuarantorAsset: async (guarantorId, assetId) => {
    return sendRequest({
      url: `/api/borrowers/guarantors/${guarantorId}/assets/${assetId}/`,
      method: 'get'
    });
  },

  // Update guarantor asset
  updateGuarantorAsset: async (guarantorId, assetId, data) => {
    return sendRequest({
      url: `/api/borrowers/guarantors/${guarantorId}/assets/${assetId}/`,
      method: 'put',
      data
    });
  },

  // Delete guarantor asset
  deleteGuarantorAsset: async (guarantorId, assetId) => {
    return sendRequest({
      url: `/api/borrowers/guarantors/${guarantorId}/assets/${assetId}/`,
      method: 'delete'
    });
  }
};
