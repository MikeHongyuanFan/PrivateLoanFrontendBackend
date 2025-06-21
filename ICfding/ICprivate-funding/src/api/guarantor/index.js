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
  }

  // NOTE: Asset and liability management for guarantors is now handled 
  // through the unified Asset/Liability tables via the main application flow.
  // Individual guarantor assets/liabilities are created/updated as part of 
  // the guarantor creation/update process using the unified serializers.
  // 
  // For direct asset/liability operations, use the unified asset/liability APIs:
  // - /api/assets/ (for all assets regardless of owner type)
  // - /api/liabilities/ (for all liabilities regardless of owner type)
  // 
  // The assets and liabilities are automatically associated with the correct
  // guarantor through the foreign key relationships in the unified tables.
};
